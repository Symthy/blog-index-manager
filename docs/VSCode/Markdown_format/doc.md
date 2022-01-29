# Markdown format

## remark

Prettierでは、余分な半角スペースが入る -> remark を使えば解消できる

Prettier を併用するなら以下で対象外に

```
 "prettier.disableLanguages": [
     "markdown",
 ],
```

VSCodeのsettings.jsonに追加

```
"remark.format": {
    "rules": {
        "rule": "-", // 区切りに使用するマーカー
        "ruleSpaces": false, // 区切りの後にスペースを入れない
        "listItemIndent": 1, // リストアイテムのインデント数
        "fences": true // フェンスで囲まれたコードを常に使用するか
    }
},
```

[VSCodeでMarkdownの自動フォーマット＆整形ルールを自由に設定](https://qiita.com/the_red/items/e121cbb659c52a60bca6)

- [remark 設定項目](https://github.com/remarkjs/remark/tree/main/packages/remark-stringify#api)

ペースト時に末尾に改行がはいるようになった。 以下でひとまず回避

```
"editor.formatOnPaste": false,
```

## ref

- [VS CodeをMarkdownエディタとして使う](https://isshi-hasegawa.hatenablog.com/entry/2021/05/03/VS_Code%E3%82%92Markdown%E3%82%A8%E3%83%87%E3%82%A3%E3%82%BF%E3%81%A8%E3%81%97%E3%81%A6%E4%BD%BF%E3%81%86)

-[remark(Github)](https://github.com/remarkjs/remark)

Parser に手を入れたい場合は以下が参考になる

- [Remark で広げる Markdown の世界](https://vivliostyle.github.io/vivliostyle_doc/ja/vivliostyle-user-group-vol2/spring-raining/index.html)
