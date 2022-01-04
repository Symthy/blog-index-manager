# memo

## hatena blog API (Atom)

https://kanaxx.hatenablog.jp/entry/hatena-entry-update

- <updated>のタグを入れないと、更新日がスクリプト実行日に変わってしまう。作成日も一緒に変わってしまう。
- <category>を送らないとカテゴリーがクリアされてしまう。

### 実装参考

JS: https://github.com/sfpgmr/node-hatena-blog-api2/blob/master/src/blog.js

## JS

JSでの作成は中止

### JS テンプレートエンジン

2021/12/30時点

- EJS 6Kstar
- Edge.js 401star
- Nunjucks 7.6Kstar：jinja2 inspired
- JsRender 2.6Kstar
- Handlebars.js 16.4Kstar ※Mustacheテンプレートとほぼ互換性あり
- Mustache.js 15.1Kstar
- Marko 10.8Kstar
- Pug 20.6Kstar ※HTML特化っぽい

https://anken-hyouban.com/blog/2021/06/01/template-engine/

他言語互換を考えてMustache採用 → ロジックが必要なのでHandlebars.js

MustacheかHandlebarsか

- https://codechord.com/2013/07/javascript_template_engine-mustache-handlebars-microtemplating/

### Handlebars

プリコンパイル

https://handlebarsjs.com/installation/precompilation.html#getting-started

```
handlebars example.handlebars -f example.precompiled.js
```

```js
const template = Handlebars.templates.example;
document.getElementById('output').innerHTML = template({doesWhat: 'rocks!'})
```

## python

### reference

[はてなサービスにおけるWSSE認証](http://developer.hatena.ne.jp/ja/documents/auth/apis/wsse)

[pythonでwsse認証を用いて、はてなブログにエントリーを投稿する](https://qiita.com/hirohuntexp/items/26ea150a531fbc9da722)

[はてなブログ、フォトライフのAPIを使って投稿を自動化する](https://swfz.hatenablog.com/entry/2019/09/01/040939)

[WordPressの記事をはてなブログに自動で連携【AtomPubを使う】](https://www.wegirls.tech/entry/2017/02/03/211023)

[【Python】XMLのデータを読み取り・書き込みする(ElementTree)](https://pg-chain.com/python-xml-read-write)

[PythonでのXMLファイル操作例](https://qiita.com/sino20023/items/0314438d397240e56576)

[Pythonで日付文字列からのdatetime変換やタイムゾーンの変更などをいい加減覚えたい](https://www.soudegesu.com/python/python-datetime)

[Python日付型](https://qiita.com/motoki1990/items/8275dbe02d5fd5fa6d2d)

[Pythonで辞書のキー・値の存在を確認、取得（検索）](https://note.nkmk.me/python-dict-in-values-items/)

[Pythonでリストをソートするsortとsortedの違い](https://note.nkmk.me/python-list-sort-sorted/)

[python](https://note.nkmk.me/python/)

[Pythonでクラスの引数や戻り値の型アノテーションに自己のクラスを指定する](https://qiita.com/MtDeity/items/fa6cfc4fff8f58140caa)

```python
# これのみでいけた
from __future__ import annotations
```

[[Python] フォルダやファイルのコピー、移動、削除（shutilモジュール）](https://hibiki-press.tech/python/shutil_copy_move_rmtree/1305#toc4)

[Pythonでファイル・ディレクトリを削除するos.remove, shutil.rmtreeなど](https://note.nkmk.me/python-os-remove-rmdir-removedirs-shutil-rmtree/)

```python
import shutil

# フォルダ丸ごとコピー (既にフォルダがあると失敗)
shutil.copytree('./sample', './sample_backup')
# フォルダ丸ごと削除
shutil.rmtree()
```

[Pythonで文字列を置換（replace, translate, re.sub, re.subn）](https://note.nkmk.me/python-str-replace-translate-re-sub/)

```python
# 複数の文字を指定して置換
s = 'one two one two one'
print(s.translate(str.maketrans({'o': 'XXX', 't': None})))
# XXXne wXXX XXXne wXXX XXXne
```

[Pythonで文字列の先頭と末尾から空白や文字列を削除する：strip()](https://uxmilk.jp/12804)

```python
# 先頭/末尾削除
"Hello World World Hello".strip('Hello')  # " World World "
# 先頭/末尾の空白/改行削除
s = "  Hello World\n".strip()  # "Hello World"
# 先頭のみ削除
s = "  Hello World\n".lstrip()  # "Hello World\n"
# 末尾のみ削除
s = "  Hello World\n".rstrip()  # "  Hello World"
```

[【Python】 フォルダ内の特定のファイルを取得する](https://ni4muraano.hatenablog.com/entry/2017/01/30/184606)

```python
# フォルダ内の特定ファイル名のみ取得
import os

files = os.listdir('Folder\\')
extension = '.txt'
text_files = [file for file in files if extension in file]
for file_name in text_files:
    print(file_name)
```

```python
# フォルダ内の特定ファイルフルパス取得
import glob

extension = '.txt'
text_files = glob.glob('Folder\\*' + extension)
for file_path in text_files:
    print(file_path)
```

[Pythonで辞書を作成するdict()と波括弧、辞書内包表記](https://note.nkmk.me/python-dict-create/)

```python
# 辞書内包表記
l = ['Alice', 'Bob', 'Charlie']
d = {s: len(s) for s in l}
```

[ArgumentParserを使ってpythonのコマンドライン引数をとことん使ってみた](https://qiita.com/mimitaro/items/a845b45df35b39a59c95)

## GitBook

[Gitbook 環境 マイ・ベスト](https://qiita.com/HeRo/items/f9ef391fa005b5fa100c)

[GitBookによるドキュメント作成](https://zenn.dev/mebiusbox/articles/703e934c78fa20)

[Gitbook の環境を Dockerで作った](https://hero.hatenablog.jp/entry/2018/11/04/184650)

