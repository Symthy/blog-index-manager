# memo

## 実装参考

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

## GitBook

[Gitbook 環境 マイ・ベスト](https://qiita.com/HeRo/items/f9ef391fa005b5fa100c)

[GitBookによるドキュメント作成](https://zenn.dev/mebiusbox/articles/703e934c78fa20)

[Gitbook の環境を Dockerで作った](https://hero.hatenablog.jp/entry/2018/11/04/184650)

