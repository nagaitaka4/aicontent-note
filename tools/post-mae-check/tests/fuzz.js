// 乱数で作る文章（公式ライブラリとの突き合わせ用）。run.js（JS版）と xcount.py（Python版）の両方が使う。
// 日本語・英数・記号・絵文字・URLっぽい文字列・ファイル名・空白・正規化が絡む文字を、境界なしで連結する。
const chars = (s) => Array.from(s);
function rng(seed) { return () => { seed |= 0; seed = (seed + 0x6D2B79F5) | 0; let t = Math.imul(seed ^ (seed >>> 15), 1 | seed); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
const pools = [
  chars('あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞっゃゅょー'),
  chars('日本語文字数検証投稿記事運用実測確認公式仕様読者前提昨日今日'),
  chars('アイウエオカキクケコサシスセソタチツテトナニヌネノ'),
  chars('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'),
  chars(' .,:;!?-_/()@#$%&*+=~|\'"<>[]{}'),
  chars('→←↑↓…・※①②③★☆♪♫✅❤❗‼⁉™©®℃°±×÷—–―‐“”‘’「」『』（）【】〜～、。，．'),
  ['😀', '😷', '👾', '🔥', '💩', '🙋🏽', '👨‍🎤', '👨‍👩‍👧‍👦', '🇯🇵', '🇺🇸', '🏴󠁧󠁢󠁥󠁮󠁧󠁿', '❤️', '❤', '✅', '1️⃣', '#️⃣', '*️⃣', '0️⃣', '©️', '®️', '™️', '☺️', '☺', '🧑‍🦰', '🫶', '🐦‍🔥', '🤝🏻', '👍', '👍🏿', '🎉', '⭐', '✨', '⚠️', '⚠', '▶️', '▶', '🅰️', '🈁', '🧑‍💻', '👩‍🔬', '🏃‍♀️', '🤷‍♂️'],
  ['https://example.com', 'http://t.co/abc123', 'https://t.co/abc123?x=1', 'example.com/path', 'foo.tokyo', 'README.md', 'index.js', 'main.py', 'a.b', 'v2.1.283', '1.5.0', 'x.com/aicontent_note', 'claude.ai', 'user@example.com', 'https://example.com/日本語/パス?q=1#frag', 'www.google.co.jp', 'github.com/nagaitaka4/aicontent-note', 'bit.ly/3xYz', 'localhost:3000', '192.168.0.1', 'ftp://x.com', 'https://例え.jp/テスト', 'foo.bar.baz.com', 'Node.js', 'pages.dev', 'example.com:8080/a', '(https://example.com/a_(b))', 'https://example.com/a.', 'xn--eckwd4c7c.jp', 'test.co.jp。', 'ABC.COM', 'ai.tools'],
  [' ', ' ', '\n', '\n\n', '　', '\u200d', '\ufe0f', '\u200b', ' ', '\t', '﻿', '‪'],
  ['が', 'é', 'ｱｲｳ', 'ｶﾞ', '㌔', 'ﬁ', 'Ⅳ', '①', ' '],
];
function makeRandText(seed) {
  const rand = rng(seed);
  const pick = (a) => a[Math.floor(rand() * a.length)];
  return function rndText() {
    const n = 1 + Math.floor(rand() * 14);
    let s = '';
    for (let i = 0; i < n; i++) {
      s += pick(pick(pools));
      if (rand() < 0.15) s += ' ';
    }
    return s;
  };
}
module.exports = { makeRandText, pools };
