# React スタイリング メモ

## React スタイリング 手段

手法は大きく２つに分かれていそう

- CSS Modules系：
    - CSS を分けて書く。（規約が定まる）
    - CSSのロードはJSと分かれるため、パフォーマンスは良い傾向（ビルド時に作成されたCSSファイルをロードする方がパフォーマンスがよいケースは多い）
    - CSS用のファイル分けるため、ファイルが増える/メンテしずらい等、開発者体験は悪くなる傾向

- CSS-in-JS系：
    - jsx/tsx に CSS も一緒に書く。CSSをコンポーネントレベル自体に抽象化できる。
    - jsからスタイルを動的生成するため、物や規模によっては部分的にパフォーマンスの問題が出てくる？（例：styled componentの初期ロードが重くなる可能性）
    - 1ファイル内で完結し、強いメリットもあるため、開発者体験は良い傾向。ただし、ロジック側との境界が曖昧になるし、難しい面もあるみたいなので、失敗すると大変なことになる

ダイナミックスタイルが必要になるなら、CSS-in-JS。ただしCSS-in-JSはライブラリ等への依存度高い上、CSSをそのまま移植はできない。CSS
Modulesで書くCSSは標準技術であり、CSSだけは結合度を低くできるから移植もしやすい。安定を取るならCSS Modules。

## 手段

- CSS Modules
    - パフォーマンスが良いが、1コンポーネントに1cssファイル必要→ファイルが膨大になり開発しづらくなる（css-loaderが非推奨）
- Vanilla-Extract (CSS Modules)
    - css.ts で cssは分けて書く。CSS Modules-in-TypeScriptと言えるフレームワーク

- Styled Component (CSS-in-JS)
    - 一度レンダリングしたあとは差分だけレンダリング。jsからスタイルを動的に生成するため、その一度のレンダリングコストが若干重い（＝初期ロードが重くなる可能性）

- emotion (CSS-in-JS)：メリットやデメリットはstyled-componentsとほぼ一緒


- Tailwind CSS (CSS フレームワーク)：
    - ユーティリティファーストのCSSフレームワークで非常にReactと相性がいい。
    - CSS Modulesにも@applyで組み合わせたり、CSS-in-JSにもtwin.macroというライブラリで組み合わせて使う事も可能で、汎用性が高い
    - ただし、複雑なスタイルはclassにたくさん書く必要が出てくるため分かりにくくなる（可読性が悪くなる）

- Material UI (UI ライブラリ)
    - マテリアルデザインを簡単に実現することができるデザインライブラリ（故にデザインがマテリアルデザイン固定になる）
    - ver5 から カスタマイズ性能を持ち合わせた
    - emotion か styled-components を使用するようになった（＝CSS-in-JSの特徴に当てはまる?）

- Chakra UI (UI ライブラリ)
    - スタイルを限られたパラメータから選んで指定するアプローチで、UIに一貫性を持たせやすくしたライブラリ
    - デフォルトのスタイルに癖がなく、ユーティリティファーストでプロップから簡単にカスタマイズできる。
    - emotion を利用している模様 (＝CSS-in-JSの特徴に当てはまる?)
    - ref: [ReactのUIコンポーネントライブラリ「Chakra UI」とは？ カスタマイズ性と生産性を両立しよう【前編】](https://codezine.jp/article/detail/14911)

非推奨：

- styleプロップ：パフォーマンスが悪い

## ref

- [Reactにおけるスタイリング手法まとめ](https://zenn.dev/chiji/articles/b0669fc3094ce3)
- [CSS in JSとしてVanilla-Extractを選んだ話と技術選定の記録の残し方](https://tech.plaid.co.jp/karte-blocks-vanilla-extract-adr)
- [CSS in JS メリット・デメリット](https://kk-web.link/blog/20210112)
- [ReactのCSSの選択肢を比較してみた](https://zenn.dev/irico/articles/d0b2d8160d8e63)
- [CSS2021 CSS-IN-JS ranking](https://2021.stateofcss.com/ja-JP/technologies/css-in-js/)
- [それでも私がTailwind CSSではなく、CSS Modulesを推す理由](https://qiita.com/70ki8suda/items/b95aeb4d4d3cab57a8fe)