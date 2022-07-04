# go-ini では セミコロンが省略される

## 前置き

Windows の 環境変数の区切り文字は、`;`
= 設定ファイル(内容：<Key>=<Value> の形式)で、Windows の環境変数を設定する必要がある場合は `;` を使用

しかし、`;` がある設定ファイルを go-ini で読み込んだら、`;` が欠けて読み込まれた。

## 理由

go-ini では、`;` はコメントのシンボル。

ソースを見ると、コメントシンボルとして扱っている箇所があることが分かる

https://github.com/go-ini/ini/blob/14e9811b1643cf01ea36277e44dffef4f119fa31/parser.go#L432

go-ini の issues にも本件に関するものがある

https://github.com/go-ini/ini/issues/169

上記 issue にある通り、以下に回避方法が書いてある。

https://ini.unknwon.io/docs/howto/work_with_comments
