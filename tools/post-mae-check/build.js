// ソースを1つのHTMLに束ねる（node build.js）
//   dist/wp-block.txt        WordPressの投稿編集画面 →「⋮」→「コードエディター」に貼る用（カスタムHTMLブロック）
//   dist/post-mae-check.html 単独で開ける版（動作確認・別ページ用）
// 束ねるのは vendor（公式の正規表現）→ core.js → style.css → app.js。esbuild で1行に圧縮する。
const fs = require('fs');
const path = require('path');
const esbuild = require('esbuild');

const read = (p) => fs.readFileSync(path.join(__dirname, 'src', p), 'utf8');
const vendor = read('vendor/twitter-text-regex.js');
const core = read('core.js');
const app = read('app.js');
const css = esbuild.transformSync(read('style.css'), { loader: 'css', minify: true }).code.trim();

// --- 検査1：通信・外部読み込みにつながる書き方が、自前のコードに無いこと ---
const forbidden = [
  [/\bfetch\s*\(/, 'fetch('], [/XMLHttpRequest/, 'XMLHttpRequest'], [/sendBeacon/, 'sendBeacon'],
  [/WebSocket/, 'WebSocket'], [/EventSource/, 'EventSource'], [/importScripts/, 'importScripts'],
  [/\bimport\s*\(/, 'import('], [/\beval\s*\(/, 'eval('], [/new\s+Function/, 'new Function'],
  [/document\.cookie/, 'document.cookie'], [/\.src\s*=/, '.src ='], [/\.href\s*=/, '.href ='],
  // 何も保存しない（2026-10-05〜。プライバシーポリシーに「保存しません」と書いている）
  [/localStorage/, 'localStorage'], [/sessionStorage/, 'sessionStorage'], [/indexedDB/i, 'indexedDB'], [/caches\./, 'Cache API'],
  [/createElement\(\s*['"](?:script|img|link|iframe|object|embed)['"]/, '外部を読む要素の生成'],
  [/el\(\s*['"](?:script|img|link|iframe|object|embed)['"]/, '外部を読む要素の生成'],
  [/<\s*(?:script|img|link|iframe|object|embed)\b/i, 'HTMLに外部要素'], [/url\(/i, 'CSSのurl('], [/@import/i, 'CSSの@import'],
];
// コメントを除いた自前のコード（core.js + app.js）だけを検査する。vendor（公式の正規表現の文字列）は対象外
const own = esbuild.transformSync(core + '\n' + app, { minify: true, target: 'es2017', charset: 'utf8' }).code;
for (const [re, name] of forbidden) {
  if (re.test(own) || re.test(css)) throw new Error('外部通信につながる書き方が入っています: ' + name);
}
// 後ろ向き先読み（古いiPhoneで、ツール全体が動かなくなる）
if (/\(\?<[=!]/.test(own + vendor)) throw new Error('後ろ向き先読み (?<= / (?<! が入っています');
// 新しめの構文（古い端末で構文エラーになる）。esbuild の target で ?. ?? は下げられるので、ここでは元のソースに書いていないかを見る
if (/\?\.[A-Za-z_$(\[]|\?\?/.test((core + app).replace(/\/\*[\s\S]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '').replace(/'(?:[^'\\\n]|\\.)*'/g, "''"))) throw new Error('?. か ?? が入っています');

const banner = '(function(){"use strict";\n';
let js = esbuild.transformSync(
  banner + vendor + '\n' + core + '\nvar PMC_CSS=' + JSON.stringify(css) + ';\n' + app + '\n})();',
  { minify: true, target: 'es2017', charset: 'utf8' }
).code.trim();

// --- 日本語以外の非ASCII文字は \uXXXX に戻す（ライセンス告知のコメントより後ろ＝コードだけ） ---
// charset:'utf8' は '️' のようなエスケープも生の文字にする。WordPressは保存時に絵文字の部品（U+FE0F など）を
// &#xfe0f; に置き換え、<script> の中ではそれが文字に戻らない（2026-10-05 固定ページ1094で発生）。
// 非ASCIIはコード中では文字列・正規表現の中にしか無いので、エスケープしても意味は変わらない
const SAFE = /[^\x00-\x7e　-ヿ一-鿿＀-￯]/g;
const noticeEnd = js.indexOf('*/') + 2;
js = js.slice(0, noticeEnd) + js.slice(noticeEnd).replace(SAFE, (c) => '\\u' + c.charCodeAt(0).toString(16).padStart(4, '0'));
if (SAFE.test(js.slice(noticeEnd))) throw new Error('日本語以外の非ASCII文字がscriptに残っています（WordPressが書き換える）');

// --- 検査2：<script> の中に置くと壊れる並びが無いこと ---
for (const bad of ['</script', '<!--', '<script', '-->']) {
  if (js.toLowerCase().includes(bad)) throw new Error('script内に置けない文字列: ' + bad);
}
if (/\n\s*\n/.test(js)) throw new Error('空行が入っている（WordPressの自動整形で崩れる）');

const fallback = '<p>「投稿まえチェック」を表示するには、ブラウザのJavaScriptが必要です。しばらく待っても表示されない場合は、ページを読み込み直してください。</p>';
// scriptの中身を <!-- と //--> で包む。WordPressは表示時の整形（wptexturize）で、コード中の `<=1&&a>` のような並びを
// タグと誤認し、&& を &#038;&#038; に変える（2026-10-05 固定ページ1094のプレビューで53か所・ツールが動かなかった）。
// HTMLコメントの中は整形されない。ブラウザは <!-- を1行コメントとして読むので、コードの意味は変わらない
const snippet = '<div id="pmc-host">' + fallback + '</div>\n<script><!--\n' + js + '\n//--></script>';

const dist = path.join(__dirname, 'dist');
fs.mkdirSync(dist, { recursive: true });
fs.writeFileSync(path.join(dist, 'wp-block.txt'), '<!-- wp:html -->\n' + snippet + '\n<!-- /wp:html -->\n');
fs.writeFileSync(path.join(dist, 'post-mae-check.html'), [
  '<!doctype html>',
  '<html lang="ja"><head><meta charset="utf-8">',
  '<meta name="viewport" content="width=device-width, initial-scale=1">',
  '<title>投稿まえチェック</title>',
  '<style>body{margin:0;padding:16px;background:#f5f7f9;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Kaku Gothic ProN","Hiragino Sans","Noto Sans JP",Meiryo,sans-serif;color:#1f2933}</style>',
  '</head><body>',
  snippet,
  '</body></html>',
  '',
].join('\n'));

const kb = (f) => (fs.statSync(path.join(dist, f)).size / 1024).toFixed(1) + ' KB';
console.log('書き出し: dist/wp-block.txt', kb('wp-block.txt'), '／ dist/post-mae-check.html', kb('post-mae-check.html'));
