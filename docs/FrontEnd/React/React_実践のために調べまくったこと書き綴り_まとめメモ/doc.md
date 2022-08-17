# React 実践のために調べまくったこと書き綴り まとめメモ

React のド基礎を押さえただけで React ができるとは言えないので、実践のために以下を行ってみる

- [フロントエンドコーディング試験](https://notion.yumemi.co.jp/0e9ef27b55704d7882aab55cc86c999d)
- [ゆめみのフロントエンドコーディング試験の題材で React の勉強をしました](https://bufferings.hatenablog.com/entry/2022/06/11/232314)

そのために調べまくったことを書きなぐった結果故に、偏りがあるのはご容赦を。

## フォルダ構成

大事なのは、

- １機能を構成する要素(hooks/provider/context 等)は１パッケージにまとめて格納すること（hooks/provider 毎での分散配置はアンチパターン）
- 横断的関心事（共通コンポ/関数や定数等）と機能(features)で閉じる物を明確に分ける
- 機能(features)で閉じて、依存関係を「機能(features) -> 横断的関心事」とする。このように全体で依存関係が入り乱れないようにする

### サンプル

大規模向け。components の下に色々置くでは見通しが悪くなるので、機能ごとに分け、さらに構成要素毎にフォルダを切る。

- [React ベストプラクティスの宝庫！「bulletproof-react」が勉強になりすぎる件](https://zenn.dev/meijin/articles/bulletproof-react-is-best-architecture)

```
src
|
+-- assets      # イメージ、フォントなどのすべての静的ファイルを格納
|
+-- components  # 共有コンポーネント
|
+-- config      # グローバル構成、env変数など
|
+-- features    # 機能ベースモジュール ★
|    +--<featureName>
|        +-- api         # エクスポートされたAPIリクエスト宣言と特定機能に関連するAPIフック
|        |
|        +-- components  # 特定機能にスコープした構成部品
|        |
|        +-- hooks       # 特定機能にスコープしたhooks
|        |
|        +-- routes      # 特定機能にスコープしたrouteコンポーネント # イメージ的にはpage兼routingのイメージ
|        |
|        +-- stores      # 特定機能にスコープした状態ストア
|        |
|        +-- types       # 特定機能のドメインの型
|        |
|        +-- utils       # 特定機能のUtility関数
|        |
|        +-- index.ts    # 機能のエントリポイントの場合は、特定の機能のパブリックAPIとして機能し、機能の外部で使用する必要があるすべてのものをエクスポートする。
|
+-- hooks       # 共有フック
|
+-- lib         # 外部ライブラリの再エクスポート
|
+-- providers   # all of the application providers
|
+-- routes      # routes configuration
|
+-- stores      # global state stores
|
+-- test        # test utilities and mock server
|
+-- types       # アプリケーション全体で使用する基本型
|
+-- utils       # 共有Utility関数
```

小規模～中規模なら、components の下にフォルダを切って格納していく形でもよさそう

小規模で済むなら、公式のような構成でも良さそうだし

- [React 公式 Doc ファイル構成](https://ja.reactjs.org/docs/faq-structure.html)

多少大きくなるようなら以下のように components を分けるのが良さそう

- [SPA Component の推しディレクトリ構成について語る](https://zenn.dev/yoshiko/articles/99f8047555f700)

```
src
+-- components
|    +-- page  # 1ページを表すコンポーネント (Next.js 使用時)
|    |    +-- top
|    +-- model
|    |    +-- user  # ステート＆ロジック？機能？
|    +-- ui
|    ~    +-- button  # ステートを持たないような表示のみのコンポーネント
|    +-- functional
+-- pages  # Next.js使用時 こちらはルーティングのみにする
```

- ★ [そのファイル、本当に hooks・utils に入れるんですか？React プロジェクトを蝕む「技術駆動パッケージング」](https://qiita.com/honey32/items/dbf3c5a5a71636374567)

```
src/
  ├ components/ ... 汎用的なコンポーネント
  ├ consts/     ... 中央管理したい定数群
  ├ hooks/      ... 汎用的なカスタムフック
  ├ features/
  │   ├ users/  ... ユーザー関連の機能
  │   └ posts/  ... 投稿関連の機能
  └ concerns/       ... 全体を横断して使われる、技術者視点で抜き出した個々の機能
      ├ auth/   ... ページや操作の許可・不許可
      └ toast/  ... トースト関連
          ├ Toast.tsx
          ├ toastContext.tsx
          ├ ToastProvider.tsx
          └ useToast.ts
```

- ※ Toast コンポーネントの Props と、状態管理の型を別々に切り離し、Toast.tsx だけ components/ 以下に移動するのもありかもらしい

規模に合わせて、段階的に？フォルダ構成を変えるのが良い？。以下も大規模になった際は、features フォルダを導入している。

refs:

- [React Folder Structure in 5 Steps [2022]](https://www.robinwieruch.de/react-folder-structure/)

- [Evolution of a React folder structure and why to group by features right away](https://profy.dev/article/react-folder-structure)

その他

- フォルダはパスカルケース
  > コンポーネントベースの UI ライブラリを使用するフロントエンドでは、コンポーネントを含むフォルダー/ファイルの場合、この名前付け規則が PascalCase に変更されました。
- pages フォルダは 複数ページ構成なら設けた方が良さそう（pages は Next.js での慣習）

### まとめ

上記の総括。src 直下は以下のように分けていくのが良い？（あくまで個人の見解）

この分け方がベストというわけではない。大事なのは、適切に責務/関心等の分離/分類がしやすい形に小さく分ける。管理と把握と拡張をしやすく保つこと。

以下の図のイメージが素晴らしい。

- ★ [そのファイル、本当に hooks・utils に入れるんですか？React プロジェクトを蝕む「技術駆動パッケージング」：２．責務に従ったパッケージングで解決](https://qiita.com/honey32/items/dbf3c5a5a71636374567#%EF%BC%92%E8%B2%AC%E5%8B%99%E3%81%AB%E5%BE%93%E3%81%A3%E3%81%9F%E3%83%91%E3%83%83%E3%82%B1%E3%83%BC%E3%82%B8%E3%83%B3%E3%82%B0%E3%81%A7%E8%A7%A3%E6%B1%BA)

features と components/models の明確な境界がイメージしきれてない（実践してみないと恐らく見えてこない）。悩む＆小規模なら統合しても良いかも

```
src/
  ├ components/          # 共通コンポーネント（特定のfeatureに関係なくまたいで利用されるようなコンポーネント）
  |  ├ pages/              # ページコンポーネント ※features内に入れるべきか不明。個人的にはひとまとめにする場所が欲しい
  |  ├ ui/ or view/        # Viewの部品。見た目に関するコンポーネント
  |  └ models/             # その他。モデルに関するコンポーネント（domain/entityに近いイメージ）
  ├ consts/              # (中央管理したい)共通定数群
  ├ configs/             # グローバル構成、env変数など (constsと一緒でもいいかも)
  ├ hooks/               # 共通カスタムフック
  ├ features/            # 機能ベースコンポーネント群（機能毎でフォルダを割った方がいいなら割る）
  |  └ <FeatureName>/    # ※以下は大規模でなければ分けずにファイル名管理でも十分ならそれで良いと考える
  |    ├ api/              # APIフック
  |    ├ components/
  |    ├ hooks/
  |    ├ routes/ or pages/
  |    ├ stores/ or contexts/
  |    ├ types/
  |    ├ test/
  |    ├ utils/
  |    └ index.js or index.ts
  ├ concerns/            # 横断的に使用する機能コンポーネント群
  ├ providers/           # アプリケーション（全体にかかわる）プロバイダー
  ├ routes/              # ルーティング設定
  ├ stores/ or contexts/ # グローバルストア (Reactのcontextのみならcontextの方が良いかも？)
  ├ libs/ or external/   # 外部ライブラリをラップしたもの
  ├ utils/ or services/  # 共通Utility関数群（functinalでも良いかも？ ここは人/組織で命名がブレる）
  ├ types/               # 全体で共有する型定義
  └ test                 # test utilities and mock server
```

## ベストプラクティス（コーディング）

ref: [React ベストプラクティスの宝庫！「bulletproof-react」が勉強になりすぎる件](https://zenn.dev/meijin/articles/bulletproof-react-is-best-architecture)

- アプリケーション内に複数のレンダリング関数を追加しない。（これはすぐに制御できなくなる）
- ユニットと見なすことができる UI の一部とみなせるなら、それを別のコンポーネントに抽出。

Bad

```javascript
// this is very difficult to maintain as soon as the component starts growing
function Component() {
  function renderItems() {
    return <ul>...</ul>;
  }
  return <div>{renderItems()}</div>;
}
```

Good

```javascript
function Items() {
  return <ul>...</ul>;
}

function Component() {
  return (
    <div>
      <Items />
    </div>
  );
}
```

- コンポーネントが受け入れているプロップが多すぎる場合は、複数のコンポーネントに分割するか、子またはスロットを介して合成手法を使用することを検討する。

[example code](https://github.com/alan2207/bulletproof-react/blob/master/src/components/Elements/ConfirmationDialog/ConfirmationDialog.tsx)

```typescript
import { Dialog, DialogTitle } from '@/components/Elements/Dialog';
// :

export type ConfirmationDialogProps = {
  triggerButton: React.ReactElement;
  confirmButton: React.ReactElement;
  // :
}
export const ConfirmationDialog = ({
  triggerButton,
  confirmButton,
  // :
}: (ConfirmationDialogProps) => {
  // :
  const trigger = React.cloneElement(triggerButton, {
    onClick: open,
  });
  return (
    <>
       {trigger}
       // :
       <div>
         {confirmButton}
       </div>
    </>
  );
}
```

- 共有コンポーネントをコンポーネントライブラリに抽象化する

大規模なプロジェクトでは、すべての共有コンポーネントを抽象化することを推奨。これにより、アプリケーションの一貫性が向上し、保守が容易になる。

- その他

refs:

- [【React/Vue.js】コンポーネント設計の（個人的）ベストプラクティス | Offers Tech Blog](https://zenn.dev/offers/articles/20220523-component-design-best-practice)
- [クリーンな React プロジェクトの 21 のベストプラクティス](https://qiita.com/baby-degu/items/ea4eede60bbe9c63a348)
- [React のベストプラクティスとコード削減パターン - パート 1](https://blog.microcms.io/react-best-practices-part1/)
- [React のベストプラクティスとコード削減パターン - パート 2](https://blog.microcms.io/react-best-practices-part2/)
- [React のベストプラクティスとコード削減パターン - パート 3](https://blog.microcms.io/react-best-practices-part3/)

## CSS (Style)

命名は BEM で書くより rscss の方が良い（コンポーネントでクローズドにできるため BEM は冗長）

refs:

- [React CSS で悩む全ての人へ【2022 年版】](https://ramble.impl.co.jp/1414/)
- [短いクラス名で運用できる CSS 設計 rscss を CSS Modules 向けにアレンジしてみた](https://zenn.dev/lollipop_onl/articles/eoz-rscss-in-css-modules)

styled-components vs emotion

- 可読性に関して、emotion > styled-components は同意。
- 速度も emotion 優位らしい。
- emotion は特定のフレームワークにロックインされない。
- emotion なら Object Style で書ける。
- emotion の欠点は SSR 環境への導入はややこしいらしい。

refs:

- [Vite+React+TypeScript で、CSS スタイルについて調べて、Emotion に流れ着いた](https://zenn.dev/longbridge/articles/78b5018315c876)
- [CSS-in-JS のライブラリとして「emotion」を選択している理由](https://qiita.com/__sakito__/items/d240840eef7123f62acf)
- [emotion - フレームワークに依存しない洗練された CSS-in-JS](https://blog.recruit.co.jp/rmp/front-end/post-17543/)
- [Sass から CSS Modules、そして styled-components に乗り換えた話](https://note.com/tabelog_frontend/n/n2541778b81e3)
- [CSS in JS として Vanilla-Extract を選んだ話と技術選定の記録の残し方 (emotion vs Vanilla-Extract)](https://tech.plaid.co.jp/karte-blocks-vanilla-extract-adr)

CSS Modules & CSS-in-JS 特徴

- パフォーマンスが重要なアプリケーションの場合は CSS Modules の方が適している。
- CSS-in-JS は、コードの可読性を最大化し、開発者の生産性と開発エクスペリエンスを向上させる。
- ※パフォーマンス面で CSS-in-JS が最適でないのを解消しようとしているのが ゼロランタイム CSS-in-JS。

ref:

- [CSS solutions Battle: Compile time CSS-in-JS vs CSS-in-JS vs CSS Modules vs SASS](https://dev.to/fyapy/sass-vs-css-modules-vs-css-in-js-vs-compile-time-css-in-js-who-wins-4cl)
- [CSS in JS とは](https://zenn.dev/takuyakikuchi/articles/b1b20f65d4f9cf)

個人の見解

- 動的に style 変える必要ないのなら、CSS in JS の使用はオーバースペックに思う
- webpack の css-loader が deprecated にしたため CSS Modules は下火になりつつある？
- 2022 の結果が出ないと分からないが、満足度：CSS Modules > CSS in JS (Vanilla-Extract 除く) にも関わらず早々消えるとは思えない
  - [CSS-in-JS Rankings](https://2021.stateofcss.com/en-US/technologies/css-in-js/)
- コンポーネントのソースファイルに CSS の Style の定義が入ってると可読性が良くないように感じる（色々な物が１ファイルに書かれていると何が何かパッと見見づらい）
  - 故に分けたいため、CSS Modules と Vanilla-Extract が個人的には好み（ただ Vanilla-Extract はまだマイナーなのが気になる）
  - だが、ビューとアプリケーションロジックを分ける container/presentation パターン で実装するなら CSS-in-JS でも気にならない
    - ビュー（HTML/CSS メイン）と ロジック(JS の実装ゴリゴリ) で分けれるなら、そちらの方が関心の分離になるため(可読性や責務的にも)良い
- webpack で CSS Modules が非推奨というだけで、Vite では非推奨になっていない(デフォルトで使用可能)なため、Vite で CSS Modules 使う分には直近問題にはならない

結論（Vite を使用する前提で）

- 小規模で動的に style 変える必要もないなら CSS Modules で十分
- 中～大規模で、ビューとアプリケーションロジックを分けてコンポーネントを作ることを徹底するなら CSS-in-JS の方が良いように思う（CSS-in-JS の方が対応の幅が効くというのはありそうなので、先を見据えて CSS-in-JS 採用はありと思う）
- CSS-is-JS で個人的に使用するなら emotion (ただし、求められるパフォーマンスがシビアでなければ。)

### emotion

参考:

- [Emotion Doc: Best Practices](https://emotion.sh/docs/best-practices)
- [@emotion/react でコンポーネントの外部からスタイルを受け取る方法](https://zenn.dev/hatchinee/articles/a235edb225fb39)
- [CSS in JS ライブラリ「emotion」のすすめ](https://zenn.dev/itomise/articles/e6386441cac697)
- [Emotion を使いこなす](https://qiita.com/282Haniwa/items/7248bed02a1b5b66579f)
- [Emotion はいいぞ](https://qiita.com/282Haniwa/items/93edc81a884add528593)
- [【お遊び？】Emotion で Utility First してみた](https://qiita.com/honey32/items/c7d4117bbc46c15a273b)
  - 以下のような指定もできるし、配列指定で合成も可能 ⇒ 一部 style を共通化して使用することも可能

```javascript
<div
  css={[
    css`color: white;`,
    // 1) テーマを引数に取る指定も含められる
    (theme) => css`background-color: ${theme.colors.primary};`,
    // 2) && etc. による条件付き指定も可
    selected && css`background-color: red;`,
  ]}
>
```

#### theme の モードチェンジ

refs:

- [Implementing dark mode in next.js with emotion - Topcoder](https://www.topcoder.com/thrive/articles/implementing-dark-mode-in-next-js-with-emotion)
- [Adding Dark Mode to Your React App with Emotion CSS-in-JS](https://levelup.gitconnected.com/adding-dark-mode-to-your-react-app-with-emotion-css-in-js-fc5c0f926838)
- [[React + Typescript] emotion の Theming 機能を使って複数の Theme 切り替えを実装してみた](https://dev.classmethod.jp/articles/react-typescript-emotion-theming/)
- [emotion 公式 Doc：複数 theme サポートしないならば theme は使用すべきでない](https://emotion.sh/docs/best-practices#define-colors-and-other-style-constants-as-javascript-variables)

※ sass で実現する方法もある。ちょっと面倒そう

[React で CSS variables でダークモードとライトモードを手軽に切り替える](https://zenn.dev/bom_shibuya/articles/f0a6d7daddfa6f)

## storybook

ref: [Vite + React + TypeScript に Vite 用 Storybook を導入する。Storybook は必要だぞ](https://zenn.dev/longbridge/articles/13e65ef71455e4)

### CSF v3.0

refs:

- [Component Story Format 3.0](https://storybook.js.org/blog/component-story-format-3-0/)
- [Storybook CSF3.0 時代のテストに備える](https://zenn.dev/takepepe/scraps/6f8fb0c9bd6fa9)
- [TypeScript + Storybook CSF3.0 の書き方とユニットテストへの応用](https://zenn.dev/yukishinonome/articles/6bc6e33d579276)

- 書き方の変更

Template.bind ではなく Object で定義できるようになった

CSF2.0

```typescript
import { Story, Meta } from "@storybook/react/types-6-0";
import SimpleFrom, { Props } from "./SimpleForm"; // 対象コンポーネント
export default {
  title: "Atoms/SimpleFrom", // CSF3.0では省略可能
  component: SimpleFrom,
} as Meta<Props>;

const Template: Story<Props> = (args) => <SimpleFrom {...args} />;

export const Index = Template.bind({});
Index.args = {
  title: "お名前フォーム",
};
```

CSF3.0

```typescript
import { ComponentMeta, ComponentStoryObj } from "@storybook/react";
import SimpleForm from "./SimpleForm"; // 対象コンポーネント
export default { component: SimpleForm } as ComponentMeta<typeof SimpleForm>;

export const Index: ComponentStoryObj<typeof SimpleForm> = {
  args: {
    title: "お名前フォーム",
  },
};
```

- play 関数によりインタラクティブストーリーが記載可能

```typescript
import userEvent from '@testing-library/user-event';

export default { component: AccountForm }

export const Empty = {};

export const EmptyError = {
  ...Empty,
  play: () => userEvent.click(screen.getByText('Submit'));
}

export const Filled = {
  ...Empty,
  play: () => {
    userEvent.type(screen.getById('user'), 'shilman@example.com');
    userEvent.type(screen.getById('password'), 'blahblahblah');
  }
}

export const FilledSuccess = {
  ...Filled,  // 再利用も可能
  play: () => {
    Filled.play();
    EmptyError.play();
  }
}
```

### Interaction test

refs:

- [Storybook Doc: Interaction tests](https://storybook.js.org/docs/react/writing-tests/interaction-testing)
- [Interaction Testing with Storybook](https://storybook.js.org/blog/interaction-testing-with-storybook/)
- [Storybook 単体でインタラクションテストを実施する](https://zenn.dev/azukiazusa/articles/storybook-interaction-testing)

以下を導入すれば、再生と巻き戻しも可能

```
npm i -D @storybook/addon-interactions
```

.storybook/main.js

```javascript
  addons: [
    // 他のアドオン,
    '@storybook/addon-interactions'
  ],
  features: {
    interactionsDebugger: true
  },
```

- play で実行
- useEvent で コンポーネントとの相互作用をシミュレート
- Jest で Dom Structure を検証

```
// テスト実行
npm run test-storybook
```

## React 諸々

※公式ドキュメントを見ろ。目に入ったものだけを書き留めておく。

ref: [React 18 に備えるにはどうすればいいの？ 5 分で理解する](https://qiita.com/uhyo/items/bbc22022fe846fd2b763)

### Suspense

コンポーネントを「ローディング中なのでまだレンダリングできない」という状態にすることができる

- [React の Suspense 対応非同期処理を手書きするハンズオン](https://zenn.dev/uhyo/books/react-concurrent-handson/viewer/what-is-suspense)

### カスタム hooks

- カスタムフック＝ロジックの外だし
- カスタムフックによるある種のカプセル化が可能な点（現代ではコンポーネントのロジックがほとんどカスタムフックに書かれる）
- 関数のスコープやモジュールレベルのスコープを活用した多様なカプセル化ができる点が優れている

代表例は、API の実行＆レスポンスんの解析 => カスタムフック

refs:

- [【React】カスタムフックと本気で向き合ってみた](https://qiita.com/cheez921/items/af5878b0c6db376dbaf0)
- [React Doc: 独自フックの作成](https://ja.reactjs.org/docs/hooks-custom.html)

### Lazy

ref: [React のベストプラクティスとコード削減パターン - パート 1： 4.コードの分割](https://blog.microcms.io/react-best-practices-part1/)

- React.lazy を使うことでコンポーネントを非同期で読み込むことができる
- （アクセスしたコンポーネントのみをロードするため）無駄なコンポーネントの読み込みを避けることができる

```javascript
const Home = React.lazy(() => import("./Home"));
const About = React.lazy(() => import("./About"));
function MyComponent() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <Route path="/home" component={Home} />
      <Route path="/about" component={About} />
    </Suspense>
  );
}
```

ref: [named imports for React.lazy](https://github.com/facebook/react/issues/14603#issuecomment-726551598)

```typescript
function lazyImport<
  T extends React.ComponentType<any>,
  I extends { [K2 in K]: T },
  K extends keyof I
>(factory: () => Promise<I>, name: K): I {
  return Object.create({
    [name]: React.lazy(() =>
      factory().then((module) => ({ default: module[name] }))
    ),
  });
}

// Usage
const { Home } = lazyImport(() => import("./Home.component.tsx"), "Home");
```

以下 router と組み合わせて使う

## React Router

```
npm i react-router-dom
npm i -D @types/react-router-dom
```

[React Router Doc: Quick Start](https://reactrouter.com/docs/en/v6/getting-started/overview)

Router の種類（一部のみ。ドキュメント見るべし）

ref: [ルーティングライブラリ、React Router(v5)入門](https://zenn.dev/h_yoshikawa0724/articles/2020-09-22-react-router)

- BrowserRouter：HTML の History API（pushState、replaceState、popstate イベント）を使用して UI を URL と同期させるルーター
- HashRouter：URL のハッシュ部分（window.location.hash）を使用して UI を URL と同期させるルーター
- StaticRouter：location を変更しないルーター
- MemoryRouter
  - URL の履歴をメモリに保持するルーター（アドレスバーの読み取りまたは書き込みは行わない）
  - ブラウザーで URL を変更しないようにするユースケースの時は出番。ルートの履歴はユーザに公開されない
    - ref:[React-Router — MemoryRouter; a how to guide](https://mrsamczynski.medium.com/react-router-memoryrouter-a-how-to-guide-a496318bf981)

以下のように、コンポーネント化も可能（v6 ～？）

ref: https://github.com/alan2207/bulletproof-react/tree/master/src/routes

```typescript
export const publicRoutes = [
  {
    path: "/auth/*",
    element: <AuthRoutes />,
  },
];

export const protectedRoutes = [
  {
    path: "/app",
    element: <App />,
    children: [
      { path: "/discussions/*", element: <DiscussionsRoutes /> },
      { path: "/users", element: <Users /> },
      { path: "/profile", element: <Profile /> },
      { path: "/", element: <Dashboard /> },
      { path: "*", element: <Navigate to="." /> },
    ],
  },
];

export const AppRoutes = () => {
  const auth = useAuth();
  const commonRoutes = [{ path: "/", element: <Landing /> }];
  const routes = auth.user ? protectedRoutes : publicRoutes;
  const element = useRoutes([...routes, ...commonRoutes]);
  return <>{element}</>;
};
```

### State 戦略

ref:

- [「3 種類」で管理する React の State 戦略](https://zenn.dev/yoshiko/articles/607ec0c9b0408d)

3 種

- サーバーデータのキャッシュ
- Global State
  - ページをまたいで保持し続ける必要のある State ⇒ Redux や Recoil で管理
- Local State
  - 各 Component 内で useState を使って管理

### デザインパターン

[フロントエンドのデザインパターン](https://zenn.dev/morinokami/books/learning-patterns-1)

### その他やって得そうなこと

ref:

- [振り返って、やっておけばよかったこと](https://zenn.dev/yoshiko/articles/99f8047555f700#%E6%8C%AF%E3%82%8A%E8%BF%94%E3%81%A3%E3%81%A6%E3%80%81%E3%82%84%E3%81%A3%E3%81%A6%E3%81%8A%E3%81%91%E3%81%B0%E3%82%88%E3%81%8B%E3%81%A3%E3%81%9F%E3%81%93%E3%81%A8)

以下

- hooks 抜き出し
- useMemo/useCallback の適用
  - 「React は Immutability を前提に考えられている世界なので、意味合い的にはメモ化して内容が変化したときにだけ参照も更新されるようにしておいたほうが正しい」
  - 「いざ重くなったときにひとつひとつメモ化からやっていくのは大変だしデグレが怖い」とのこと ⇒ たしかに…。最初からそれなりにやっていった方が良さそう
- container/presenter の分離
  - storybook でのテストのカバレッジ向上目的
  - 別の解決の手はあるらしい： [「3 種類」で管理する React の State 戦略: Local State](https://zenn.dev/yoshiko/articles/607ec0c9b0408d#3.-local-state)

ref:

- [フロントエンドのデザインパターン：コンテナ・プレゼンテーションパターン](https://zenn.dev/morinokami/books/learning-patterns-1/viewer/presentational-container-pattern)

ビューをアプリケーションロジックから分離（関心の分離を促進）

- プレゼンテーションコンポーネント
  - 役割：props を通じてデータを受け取り、受け取ったデータを変更することなく、スタイルも含めて意図通りに表示すること
  - プレゼンテーションコンポーネントは（UI のためにステートが必要な場合を除き）ステートを持たない
- コンテナコンポーネント
  - 自身が含むプレゼンテーションコンポーネントにデータを受け渡すこと

Pros:

- プレゼンテーションコンポーネントは
  - UI を担当する純粋関数（＝テストが容易）
  - 再利用が容易（アプリケーション全体で異なる目的のために再利用可能＝全体での一貫性を保てる）
  - (デザイナーとの) 分業化容易
    Cons:
- 小規模なアプリケーションでは過剰＝複雑化

多くの場合、コンテナ・プレゼンテーションパターンは React のフックに置き換えることができる（コンテナ＝カスタムフック）

### テスト

[React Doc: テストのレシピ集](https://ja.reactjs.org/docs/testing-recipes.html)

## Redux/Recoil

共通点：パフォーマンス上の課題を解決するもの

refs:

- [Recoil vs Redux](https://www.imaginarycloud.com/blog/recoil-vs-redux/)
- [Facebook 製の新しいステート管理ライブラリ「Recoil」を最速で理解する](https://blog.uhy.ooo/entry/2020-05-16/recoil-first-impression/)

React 単体での共通ステート管理の限界

- コンテキストで、Redux っぽく「全てのステートを詰め込んだオブジェクトでステートを管理し、一つのコンテキストにそのオブジェクトを流す」ように、一つのコンテキストに全ての情報を入れてしまう場合はそれに依存する全てのコンポーネントが再レンダリングされ、パフォーマンス劣化に繋がるため、パフォーマンスを重視する場合に問題となる。

Redux

- ステートの宣言が中央集権的
- アプリケーションの状態とロジックを一元化したストアを提供する。
- コンポーネントが必要なデータに直接アクセスできるようにし、クライアントサーバー環境とネイティブ環境で一貫して動作する JavaScript アプリの作成を支援するように設計された予測可能な状態コンテナー
- アプリケーション全体でデータの一貫性を提供することにより、複雑なアプリケーションの構築を容易にすることができる
- 開発者のベストプラクティスを実施するのに優れており、従うべき単純なパターンを提供するため、機能を構築するときにあまり多くの実装決定を行う必要がない
- API リクエストをアクションに抽象化して、すべてを 1 か所にまとめることもできる
- Redux Devtools を使用して、アプリケーションの状態がいつ、どこで、なぜ、どのように変化するかを追跡可能
- React アプリケーションの状態を処理するために提案された 「アーキテクチャ」 である Flux も実装している。（Flux：https://facebook.github.io/flux/）

Recoil

- Recoil はステートの宣言が局所的
- 大きなメリットは、 React の Suspense との統合
- フックとの相性がよい（Recoil が提供する各種のフックは、カスタムフックに組み込みやすいように作られている）
- セレクターで非同期リクエストを作成して、API リクエストから状態を開始することができる
- (Recoil は React の最新モードと統合されているため)、Suspense を使用してロード状態を処理し、ErrorBoundary を使用してエラーを処理することで、より宣言的な方法でアプリケーションを構築することができる。
- 開発者エクスペリエンスとユーザーエクスペリエンスの両方に関しては Redux より適している

## その他

### PLOP

PLOP：テンプレートからファイル生成に使える

- [【PLOP CLI】新しいファイルをテンプレートから生成する CLI](https://zenn.dev/anozon/articles/gatsby-plop-newpost)

- [PLOP 公式 Doc](https://plopjs.com/documentation/)

以下でも利用している。参考になるはず

[github: bulletproof-react](https://github.com/alan2207/bulletproof-react)

### eslint での 依存関係チェック

[依存関係のチェック（strict-dependencies）](https://zenn.dev/yoshiko/articles/0994f518015c04#%E4%BE%9D%E5%AD%98%E9%96%A2%E4%BF%82%E3%81%AE%E3%83%81%E3%82%A7%E3%83%83%E3%82%AF%EF%BC%88strict-dependencies%EF%BC%89)
