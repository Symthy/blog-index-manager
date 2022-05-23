# shell 1行目のおまじない shebang（シバン）

bash を使用するか sh を使用するかの指定＋α

- `#!/bin/bash` : 固有の機能が使える。移植性等考えなくていいならこちらを使うと便利
- `#!/bin/sh` : 環境に拘らず使える。（ただしUbuntuの場合はdashという物が使われるらしい）

オプションの意味

`#!/bin/bash -eu` → オプション指定は set -eu と同じ

# refs

[「sh」と「bash」の使い分け](https://teratail.com/questions/149113)

[シェルスクリプトの1行目に書くおまじないで使える便利オプション集](https://qiita.com/yn-misaki/items/6fcfab082dd664f10d4e)

[シェルスクリプトの冒頭でbashを明示する（提案）](https://qiita.com/jkr_2255/items/84366f677be3365331cd)

指定できるオプション -e と -u についてわかる<br>
→ [bash スクリプトの先頭によく書く記述のおさらい](https://moneyforward.com/engineers_blog/2015/05/21/bash-script-tips/)

参考：/bin と /usr/bin の違い<br>
→ [Linuxのディレクトリ構造](https://blog.goo.ne.jp/goosyun/e/a4615eaacbbc8aa459a7e16dee34124a)
