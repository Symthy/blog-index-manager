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

[【Python】XMLのデータを読み取り・書き込みする(ElementTree)](https://pg-chain.com/python-xml-read-write)

[PythonでのXMLファイル操作例](https://qiita.com/sino20023/items/0314438d397240e56576)

[Pythonで日付文字列からのdatetime変換やタイムゾーンの変更などをいい加減覚えたい](https://www.soudegesu.com/python/python-datetime)

[Python日付型](https://qiita.com/motoki1990/items/8275dbe02d5fd5fa6d2d)

[Pythonで辞書のキー・値の存在を確認、取得（検索）](https://note.nkmk.me/python-dict-in-values-items/)

[Pythonでリストをソートするsortとsortedの違い](https://note.nkmk.me/python-list-sort-sorted/)

[python](https://note.nkmk.me/python/)