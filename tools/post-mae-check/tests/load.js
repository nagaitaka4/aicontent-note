// core.js を Node で読み込む（ブラウザ用の書き方なので、vendor と一緒に評価する）
const fs = require('fs');
const path = require('path');
const src = path.join(__dirname, '..', 'src');
const code = fs.readFileSync(path.join(src, 'vendor', 'twitter-text-regex.js'), 'utf8') +
  '\n' + fs.readFileSync(path.join(src, 'core.js'), 'utf8') + '\nreturn PMC;';
module.exports = new Function(code)();
