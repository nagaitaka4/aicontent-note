/* 投稿まえチェック：計算の中核（文字数・要注意表現・直近の重なり）
 *
 * ブラウザとNode（テスト）の両方で動く。画面のことは知らない。通信はしない。
 * 先に src/vendor/twitter-text-regex.js（変数 TT）を読み込んでおくこと。
 *
 * 元にしたもの：
 *   文字数      Xの公開ライブラリ twitter-text 3.1.0 の parseTweet（設定 v3）を、同じ手順で移したもの
 *   要注意表現  operations/x-hook.py（A＝1行目の報告型／C＝前提を知らないと通じない言い回し）
 *   重なり      operations/x-cannibal.py（3文字の重なり／数字つきの語／目印の語）
 *
 * 古いiPhoneでも止まらないよう、後ろ向き先読み（?<= ?<!）・?. ・?? は使わない。
 */
var PMC = (function () {
  'use strict';

  /* ========== 1. 文字数（twitter-text v3） ========== */

  var MAX_WEIGHT = 280;       // maxWeightedTweetLength
  var URL_WEIGHT = 23;        // transformedURLLength（URLは長さに関係なく一律23）
  var EMOJI_WEIGHT = 2;       // defaultWeight（emojiParsingEnabled: true）
  var DEFAULT_WEIGHT = 2;     // defaultWeight
  // 重み1の範囲（config/v3.json の ranges）。これ以外の文字は重み2
  var LIGHT_RANGES = [[0, 4351], [8192, 8205], [8208, 8223], [8242, 8247]];
  var MAX_URL_LENGTH = 4096;
  var MAX_TCO_SLUG_LENGTH = 40;

  function unitWeight(code) {
    for (var i = 0; i < LIGHT_RANGES.length; i++) {
      if (code >= LIGHT_RANGES[i][0] && code <= LIGHT_RANGES[i][1]) return 1;
    }
    return DEFAULT_WEIGHT;
  }

  function isHighSurrogateAt(text, i) {
    if (i < text.length - 1) {
      var c = text.charCodeAt(i), n = text.charCodeAt(i + 1);
      return c >= 0xd800 && c <= 0xdbff && n >= 0xdc00 && n <= 0xdfff;
    }
    return false;
  }

  // ドメインの妥当性（公式 idna.toAscii の移植）。ラベルが63字を超える・不正なpunycodeはURLと見なさない。
  // punycode の encode は punycode 1.4.1 (c) Mathias Bynens, MIT License の移植（長さを測るためだけに使う）
  function ucs2decode(string) {
    var output = [], counter = 0, length = string.length, value, extra;
    while (counter < length) {
      value = string.charCodeAt(counter++);
      if (value >= 0xD800 && value <= 0xDBFF && counter < length) {
        extra = string.charCodeAt(counter++);
        if ((extra & 0xFC00) === 0xDC00) {
          output.push(((value & 0x3FF) << 10) + (extra & 0x3FF) + 0x10000);
        } else {
          output.push(value);
          counter--;
        }
      } else {
        output.push(value);
      }
    }
    return output;
  }

  function punyAdapt(delta, numPoints, firstTime) {
    var k = 0;
    delta = firstTime ? Math.floor(delta / 700) : delta >> 1;
    delta += Math.floor(delta / numPoints);
    for (; delta > (35 * 26) >> 1; k += 36) delta = Math.floor(delta / 35);
    return Math.floor(k + 36 * delta / (delta + 38));
  }

  function punyDigit(d) { return String.fromCharCode(d + 22 + 75 * (d < 26 ? 1 : 0)); }

  function punyEncode(input) {
    var MAXINT = 2147483647, base = 36, tMin = 1, tMax = 26;
    var n = 128, delta = 0, bias = 72, output = [];
    var cps = ucs2decode(input);
    var len = cps.length, j, m, q, k, t;
    for (j = 0; j < len; ++j) if (cps[j] < 0x80) output.push(String.fromCharCode(cps[j]));
    var handled = output.length, basicLength = handled;
    if (basicLength) output.push('-');
    while (handled < len) {
      for (m = MAXINT, j = 0; j < len; ++j) if (cps[j] >= n && cps[j] < m) m = cps[j];
      var hp1 = handled + 1;
      if (m - n > Math.floor((MAXINT - delta) / hp1)) throw new Error('overflow');
      delta += (m - n) * hp1;
      n = m;
      for (j = 0; j < len; ++j) {
        if (cps[j] < n && ++delta > MAXINT) throw new Error('overflow');
        if (cps[j] === n) {
          for (q = delta, k = base; ; k += base) {
            t = k <= bias ? tMin : (k >= bias + tMax ? tMax : k - bias);
            if (q < t) break;
            output.push(punyDigit(t + (q - t) % (base - t)));
            q = Math.floor((q - t) / (base - t));
          }
          output.push(punyDigit(q));
          bias = punyAdapt(delta, hp1, handled === basicLength);
          delta = 0;
          ++handled;
        }
      }
      ++delta;
      ++n;
    }
    return output.join('');
  }

  // punycode.toASCII(label)：@の前はそのまま、. 。 ． ｡ で区切ってラベルごとに変換
  function punyToAscii(input) {
    var parts = input.split('@');
    var prefix = '';
    if (parts.length > 1) { prefix = parts[0] + '@'; input = parts[1]; }
    var labels = input.replace(/[\x2E。．｡]/g, '.').split('.');
    return prefix + labels.map(function (l) { return /[^\x20-\x7E]/.test(l) ? 'xn--' + punyEncode(l) : l; }).join('.');
  }

  function isValidDomain(domain) {
    if (domain.substring(0, 4) === 'xn--' && !new RegExp(TT.validAsciiDomain, 'i').test(domain)) return false;
    var labels = domain.split('.');
    try {
      for (var i = 0; i < labels.length; i++) {
        var e = punyToAscii(labels[i]);
        if (e.length < 1 || e.length > 63) return false;
      }
    } catch (err) { return false; }
    return labels.join('.').length > 0;
  }

  // 公式 extractUrlsWithIndices（extractUrlsWithoutProtocol: true）の移植。
  function extractUrls(text) {
    if (!text || !/\./.test(text)) return [];
    var re = new RegExp(TT.extractUrl, 'gi');
    var tcoRe = new RegExp(TT.validTcoUrl, 'i');
    var badPrefix = new RegExp(TT.invalidUrlWithoutProtocolPrecedingChars);
    var urls = [];
    var m;
    while ((m = re.exec(text)) !== null) {
      var before = m[2] || '';
      var url = m[3] || '';
      var protocol = m[4] || '';
      var domain = m[5] || '';
      var path = m[7] || '';
      var endPosition = re.lastIndex;
      var startPosition = endPosition - url.length;

      if (!isValidDomain(domain) || (protocol || 'https://').length + url.length > MAX_URL_LENGTH) continue;

      if (!protocol) {
        // スキームなし（example.com など）。直前が - _ . / なら URL にしない
        if (badPrefix.test(before)) continue;
        var lastUrl = null;
        var asciiEnd = 0;
        domain.replace(new RegExp(TT.validAsciiDomain, 'gi'), function (asciiDomain) {
          var asciiStart = domain.indexOf(asciiDomain, asciiEnd);
          asciiEnd = asciiStart + asciiDomain.length;
          lastUrl = { url: asciiDomain, start: startPosition + asciiStart, end: startPosition + asciiEnd };
          urls.push(lastUrl);
          return asciiDomain;
        });
        if (lastUrl === null) continue;
        if (path) {
          lastUrl.url = url.replace(domain, function () { return lastUrl.url; });
          lastUrl.end = endPosition;
        }
      } else {
        // t.co は後ろに余計な文字を続けさせない
        var tco = url.match(tcoRe);
        if (tco) {
          if (tco[1] && tco[1].length > MAX_TCO_SLUG_LENGTH) continue;
          url = tco[0];
          endPosition = startPosition + url.length;
        }
        urls.push({ url: url, start: startPosition, end: endPosition });
      }
    }
    return urls;
  }

  function extractEmoji(text) {
    var re = new RegExp(TT.emoji, 'g');
    var out = [];
    var m;
    while ((m = re.exec(text)) !== null) {
      if (m[0].length === 0) { re.lastIndex++; continue; }
      out.push({ text: m[0], start: m.index, end: re.lastIndex });
    }
    return out;
  }

  function weighCore(norm) {
    var urls = extractUrls(norm);
    var emojis = extractEmoji(norm);
    var urlAt = {}, emojiAt = {};
    urls.forEach(function (u) { urlAt[u.start] = u; });
    emojis.forEach(function (e) { emojiAt[e.start] = e; });

    var total = 0, light = 0, heavy = 0;
    for (var i = 0; i < norm.length; i++) {
      if (urlAt[i]) {
        total += URL_WEIGHT;
        i += urlAt[i].url.length - 1;
      } else if (emojiAt[i]) {
        total += EMOJI_WEIGHT;
        i += emojiAt[i].text.length - 1;
      } else {
        if (isHighSurrogateAt(norm, i)) i += 1;   // 公式と同じく、2つ目の半分で重みを決める（＝重み2）
        var w = unitWeight(norm.charCodeAt(i));
        total += w;
        if (w === 1) light++; else heavy++;
      }
    }
    return { total: total, light: light, heavy: heavy, urls: urls, emojis: emojis };
  }

  // 絵文字っぽい並び（ZWJ・異体字セレクタ・肌色・国旗・キーキャップを含む）。
  // 後ろ向き先読みではないが、\p{...} が使えない古い端末では検知だけ諦める（文字数の計算には影響しない）
  var EMOJI_RUN = null;
  try {
    EMOJI_RUN = new RegExp('[\\p{Extended_Pictographic}\\u200d\\ufe0f\\u20e3\\u{1F3FB}-\\u{1F3FF}\\u{1F1E6}-\\u{1F1FF}]+', 'gu');
  } catch (e) { EMOJI_RUN = null; }
  var EMOJI_SEQ_PART = /[‍️⃣]|\ud83c[\udffb-\udfff]|\ud83c[\udde6-\uddff]/;

  /**
   * 公式ライブラリが「1つの絵文字」と認識できず、部品ごとに数えた並びを探す。
   * 公式ライブラリの絵文字表は2020年版なので、新しい絵文字（❤️‍🔥 など）や、余分な異体字セレクタつきのもの（😐️）が当たる。
   * 実際のXがこれを2で数えるかは確認できていない。公式ライブラリどおりに数えると、2より多くなる（＝重めに見積もる）。
   * 戻り値：[{text, weight}]
   */
  function uncertainEmoji(norm, emojis, urls) {
    if (!EMOJI_RUN) return [];
    var covered = {};
    emojis.forEach(function (e) { for (var i = e.start; i < e.end; i++) covered[i] = true; });
    urls.forEach(function (u) { for (var i = u.start; i < u.end; i++) covered[i] = true; });
    var out = [];
    var r = new RegExp(EMOJI_RUN.source, 'gu');
    var m;
    while ((m = r.exec(norm)) !== null) {
      var run = m[0];
      if (!EMOJI_SEQ_PART.test(run)) continue;            // 並びの特徴が無い（ふつうの記号や単独の絵文字）は対象外
      var all = true;
      for (var i = m.index; i < m.index + run.length; i++) { if (!covered[i]) { all = false; break; } }
      // 公式の表は、単独の異体字セレクタ(U+FE0F)も「絵文字1つ」として2で数える（😐️ が 4 になる）。これも部品ごとの数え方
      // 直前の絵文字にくっついた単独の肌色（🤝🏻 など）も同じ
      var stray = emojis.some(function (e) {
        if (e.start < m.index || e.end > m.index + run.length) return false;
        if (e.text === '\ufe0f') return true;
        if (/^\ud83c[\udffb-\udfff]$/.test(e.text) && e.start > 0 && covered[e.start - 1] === true) return true;
        // 国旗になれなかった地域指示文字の並び（🇨🇶 など）
        if (/^\ud83c[\udde6-\uddff]$/.test(e.text)) {
          var prev = norm.substring(e.start - 2, e.start), next = norm.substring(e.end, e.end + 2);
          return /^\ud83c[\udde6-\uddff]$/.test(prev) || /^\ud83c[\udde6-\uddff]$/.test(next);
        }
        return false;
      });
      if (!all || stray) out.push({ text: run, weight: weighCore(run).total });
    }
    return out;
  }

  /**
   * 投稿の重みを数える。公式 parseTweet と同じ結果になるように作ってある。
   * 戻り値：
   *   weight 重み合計／max 上限／remaining 残り（負なら超過）／over 超過しているか
   *   invalid 投稿できない文字を含むか／chars 素の文字数（コードポイント）
   *   urls  URLとして23で数えたもの [{url,start,end}]
   *   emojis 絵文字として2で数えたもの [{text,start,end}]
   *   light 重み1で数えた文字数／heavy 重み2で数えた文字数（URL・絵文字を除く）
   *   uncertain 部品ごとに数えた絵文字の並び [{text, weight}]（重めの見積もり）
   */
  function weigh(text) {
    text = text || '';
    var norm = typeof text.normalize === 'function' ? text.normalize() : text;
    var c = weighCore(norm);
    var invalid = new RegExp(TT.invalidChars).test(norm);
    return {
      weight: c.total,
      max: MAX_WEIGHT,
      remaining: MAX_WEIGHT - c.total,
      over: c.total > MAX_WEIGHT,
      invalid: invalid,
      chars: Array.from(text).length,
      urls: c.urls,
      emojis: c.emojis,
      light: c.light,
      heavy: c.heavy,
      uncertain: uncertainEmoji(norm, c.emojis, c.urls)
    };
  }

  /* ========== 2. 要注意表現（x-hook.py の A・C ＋ 1行目の指示語） ========== */

  // C：前を知らないと通じない言い回し（x-hook.py CONTEXT_LEAK）
  var CONTEXT_LEAK = [
    /(?:一昨日|昨日|先日|前回|この前|さっき|先週)の/g,
    /例の/g,
    /前の投稿/g,
    /[0-9０-９]{1,2}\/[0-9０-９]{1,2}に「/g
  ];

  // A：1行目の報告型の語尾（x-hook.py REPORT_TAIL）。この順に見て、最初に当たったものを返す
  var REPORT_TAIL = [
    'できました', 'できるようになりました', 'になりました', 'なりました',
    '書きました', '調べました', '並べました', '作りました', 'まとめました',
    '出ました', '始まりました', '追加されました', '公開されました',
    'しました', 'ました'
  ];
  // A：同じ行にあれば「フックが立っている」と見なす語（落差・逆説・断定）
  var HOOK_SIGNALS = [
    'でも', 'ただ', 'じゃなくて', 'ではなく', 'なのに', 'のに', '逆に',
    'だけ', 'しか', 'ません', 'ないです', 'より', 'はずが', 'と思ったら'
  ];
  // A：告白の語（報告ではなく告白なので通す）
  var CONFESSION = [
    'と思ってました', 'と思ってた', 'と思いこんで', 'と思い込んで',
    '知りませんでした', '知らなかった', '気づきませんでした', '気づいてませんでした',
    'てませんでした', 'ていませんでした', 'できませんでした', 'のままでした',
    '見てませんでした', 'やってませんでした', '読んでませんでした'
  ];

  // 1行目の指示語（これ／それ／あれ）。「これから」「それぞれ」など指す物がない語は除く。
  // 先にその除外語を食べさせ、残った「これ／それ／あれ」だけを拾う
  var DEIXIS = /(?:あれこれ|これから|これまで|それぞれ|それから|それでも|それなり)|(これ|それ|あれ)/g;

  function normalizeNewlines(text) {
    return String(text || '').replace(/\r\n?/g, '\n');
  }

  // 最初の空でない行と、その行が全文の何文字目から始まるか
  function firstLineInfo(text) {
    var t = normalizeNewlines(text);
    var pos = 0;
    var lines = t.split('\n');
    for (var i = 0; i < lines.length; i++) {
      if (lines[i].trim() !== '') return { line: lines[i], start: pos };
      pos += lines[i].length + 1;
    }
    return { line: '', start: 0 };
  }

  // 「。！!？?」の直後で文に分ける（後ろ向き先読みを使わない書き方）
  function sentences(line) {
    var out = [];
    var cur = '';
    for (var i = 0; i < line.length; i++) {
      cur += line.charAt(i);
      if ('。！!？?'.indexOf(line.charAt(i)) >= 0) { out.push(cur); cur = ''; }
    }
    if (cur) out.push(cur);
    return out.filter(function (s) { return s.trim() !== ''; });
  }

  function hasDigit(s) { return /[0-9０-９]/.test(s); }

  /**
   * 要注意表現を拾う。NGとは言わず「確認してほしい所」として返す。
   * enabled で項目ごとにON/OFF（leak・report・deixis）。
   * 戻り値：{ first: 1行目, items: [{kind, match, index, length, sentence?}] }
   *   kind: 'leak' 前提語／'report' 1行目の報告型／'deixis' 1行目の指示語
   *   index は全文の中での位置（該当箇所の切り出し用）
   */
  function checkPhrases(text, enabled) {
    enabled = enabled || { leak: true, report: true, deixis: true };
    var t = normalizeNewlines(text);
    var fl = firstLineInfo(t);
    var items = [];

    if (enabled.leak) {
      CONTEXT_LEAK.forEach(function (re) {
        var r = new RegExp(re.source, 'g');
        var m;
        while ((m = r.exec(t)) !== null) {
          items.push({ kind: 'leak', match: m[0], index: m.index, length: m[0].length });
        }
      });
    }

    if (fl.line !== '') {
      if (enabled.report) {
        var tail = null, tailSentence = null;
        var sents = sentences(fl.line);
        for (var i = 0; i < sents.length && !tail; i++) {
          var s = sents[i].trim();
          for (var k = 0; k < REPORT_TAIL.length; k++) {
            if (new RegExp(REPORT_TAIL[k] + '[。！!]?$').test(s)) {
              tail = REPORT_TAIL[k];
              tailSentence = s;
              break;
            }
          }
        }
        var signals = HOOK_SIGNALS.filter(function (w) { return fl.line.indexOf(w) >= 0; })
          .concat(CONFESSION.filter(function (w) { return fl.line.indexOf(w) >= 0; }));
        if (tail && signals.length === 0 && !hasDigit(fl.line)) {
          var idx = fl.start + fl.line.indexOf(tailSentence);
          items.push({ kind: 'report', match: tail, index: idx, length: tailSentence.length, sentence: tailSentence });
        }
      }
      if (enabled.deixis) {
        var dr = new RegExp(DEIXIS.source, 'g');
        var dm;
        while ((dm = dr.exec(fl.line)) !== null) {
          if (dm[1]) items.push({ kind: 'deixis', match: dm[1], index: fl.start + dm.index, length: dm[1].length });
        }
      }
    }
    items.sort(function (a, b) { return a.index - b.index; });
    return { first: fl.line, items: items };
  }

  /* ========== 3. 直近の重なり（x-cannibal.py） ========== */

  var JACCARD = 0.18;
  // どの投稿にも出る名前は目印にしない（x-cannibal.py COMMON と同じ。画面で変えられる）
  var DEFAULT_COMMON = ['AI', 'X', 'Claude', 'ChatGPT', 'Claude Code', 'OpenAI', 'GPT', 'Anthropic', 'Google', 'Gemini'];

  var MARK = /[0-9０-９][0-9０-９,，.]*\s*(?:ドル|円|字|本|件|倍|%|％|時間|分|日|か月|ヶ月|人|回)|[A-Za-z][A-Za-z0-9.\- ]{1,20}[A-Za-z0-9]/g;

  function compact(s) { return String(s).replace(/\s+/g, ''); }
  function commonKey(s) { return compact(s).toLowerCase(); }

  // 文字3グラム（空白を除き、コードポイント単位）
  function grams(t, n) {
    n = n || 3;
    var cs = Array.from(compact(t));
    var set = {};
    var count = 0;
    for (var i = 0; i + n <= cs.length; i++) {
      var g = cs.slice(i, i + n).join('');
      if (!set[g]) { set[g] = true; count++; }
    }
    return { set: set, size: count };
  }

  function jaccard(a, b) {
    var inter = 0;
    for (var k in a.set) { if (Object.prototype.hasOwnProperty.call(a.set, k) && b.set[k]) inter++; }
    var union = a.size + b.size - inter;
    return inter / Math.max(1, union);
  }

  // 目印の語：数字つきの語（「100ドル」「8,300字」）と、製品名などの英字の並び
  function marks(t, commonSet) {
    var out = [];
    var seen = {};
    var r = new RegExp(MARK.source, 'g');
    var m;
    while ((m = r.exec(t)) !== null) {
      var s = compact(m[0]);
      if (commonSet[s.toLowerCase()]) continue;
      if (/^[0-9０-９]/.test(s) && /^[1１](?:件|本|回|人|日|つ)$/.test(s)) continue;   // 「1件」のような小さい数は目印にしない
      if (!seen[s]) { seen[s] = true; out.push(s); }
    }
    return out;
  }

  function makeCommonSet(list) {
    var set = {};
    (list || DEFAULT_COMMON).forEach(function (w) { var k = commonKey(w); if (k) set[k] = true; });
    return set;
  }

  /**
   * 下書き text と、保存してある投稿 posts（[{id, date, text}]）の重なりを見る。
   * どれかに当たれば要確認：
   *   3文字の重なり(Jaccard) 0.18以上／数字つきの語を1つでも共有／目印の語を2つ以上共有
   * 戻り値：[{post, jaccard, shared, nums}]（重なりの大きい順）
   */
  function findOverlaps(text, posts, options) {
    options = options || {};
    var commonSet = makeCommonSet(options.common);
    var g = grams(text);
    var mk = marks(text, commonSet);
    var mkSet = {};
    mk.forEach(function (s) { mkSet[s] = true; });
    var selfKey = compact(text);
    var hits = [];
    (posts || []).forEach(function (p) {
      if (compact(p.text) === selfKey) return;   // 同じ下書き自身は比べない
      var jac = jaccard(g, grams(p.text));
      var shared = marks(p.text, commonSet).filter(function (s) { return mkSet[s]; }).sort();
      var nums = shared.filter(function (s) { return /^[0-9０-９]/.test(s); });
      if (jac >= JACCARD || nums.length > 0 || shared.length >= 2) {
        hits.push({ post: p, jaccard: jac, shared: shared, nums: nums });
      }
    });
    hits.sort(function (a, b) {
      if (b.jaccard !== a.jaccard) return b.jaccard - a.jaccard;
      return a.post.date < b.post.date ? 1 : (a.post.date > b.post.date ? -1 : 0);
    });
    return hits;
  }

  /* ========== 4. 保存した投稿まわり ========== */

  function pad2(n) { return (n < 10 ? '0' : '') + n; }

  function dateToString(d) {
    return d.getFullYear() + '-' + pad2(d.getMonth() + 1) + '-' + pad2(d.getDate());
  }

  function parseDate(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || '');
    if (!m) return null;
    var y = +m[1], mo = +m[2], d = +m[3];
    var dt = new Date(Date.UTC(y, mo - 1, d));
    if (dt.getUTCFullYear() !== y || dt.getUTCMonth() !== mo - 1 || dt.getUTCDate() !== d) return null;
    return dt;
  }

  // 今日から days 日前（その日を含む）以降の投稿だけ残す（x-cannibal.py recent_posts と同じ：date >= 今日 - days）
  function recentPosts(posts, days, today) {
    var t = parseDate(today);
    if (!t) return posts.slice();
    var since = t.getTime() - days * 86400000;
    return posts.filter(function (p) {
      var d = parseDate(p.date);
      return d && d.getTime() >= since;
    });
  }

  /**
   * まとめて追加の文字列を分ける。区切りは「---」だけの行。
   * 各ブロックの最初の行が「2026-09-28」のような日付だけなら、そのブロックの日付にする。
   */
  function parseBulk(text, defaultDate) {
    var blocks = [];
    var cur = [];
    normalizeNewlines(text).split('\n').forEach(function (line) {
      if (/^\s*-{3,}\s*$/.test(line)) { blocks.push(cur); cur = []; } else { cur.push(line); }
    });
    blocks.push(cur);
    var out = [];
    blocks.forEach(function (lines) {
      var i = 0;
      while (i < lines.length && lines[i].trim() === '') i++;
      var date = defaultDate;
      if (i < lines.length) {
        var dm = /^\s*(?:日付[:：]\s*)?(\d{4}-\d{2}-\d{2})\s*$/.exec(lines[i]);
        if (dm && parseDate(dm[1])) { date = dm[1]; i++; }
      }
      var body = lines.slice(i).join('\n').replace(/^\s+|\s+$/g, '');
      if (body) out.push({ date: date, text: body });
    });
    return out;
  }

  return {
    SPEC: { maxWeight: MAX_WEIGHT, urlWeight: URL_WEIGHT, emojiWeight: EMOJI_WEIGHT, lightRanges: LIGHT_RANGES, versions: TT.versions },
    weigh: weigh,
    extractUrls: extractUrls,
    extractEmoji: extractEmoji,
    checkPhrases: checkPhrases,
    firstLineInfo: firstLineInfo,
    findOverlaps: findOverlaps,
    grams: grams,
    marks: marks,
    makeCommonSet: makeCommonSet,
    DEFAULT_COMMON: DEFAULT_COMMON,
    JACCARD: JACCARD,
    recentPosts: recentPosts,
    parseBulk: parseBulk,
    parseDate: parseDate,
    dateToString: dateToString
  };
})();

if (typeof module === 'object' && module && module.exports) module.exports = PMC;
