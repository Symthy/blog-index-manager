# 某社フロントエンドコーディング試験を題材とした React 学習記（作成時の考慮事項まとめ）

※部分的に記載中。近日中に記載

## はじめに

何番煎じになっているか分からないフロントエンドはチョットダケワカル者が React 学習のために、[ゆめみ社様のフロントエンドコーディング試験](https://notion.yumemi.co.jp/0e9ef27b55704d7882aab55cc86c999d)を一から作ってみた

- 作成物：https://symthy.github.io/react-clone-yumemi-exam/

- コード：https://github.com/Symthy/react-clone-yumemi-exam

仕様にはない機能として以下を追加

- API Key 入力画面
- 都道府県別人口グラフでの統計項目選択

最初は先駆者の[ゆめみのフロントエンドコーディング試験の題材で React の勉強をしました](https://bufferings.hatenablog.com/entry/2022/06/11/232314) のコードをほぼ模倣して、一部書き換えるか機能追加するか程度に考えていたが、(批判等の意図は全くないのですが…) 個人的にはコードが読みにくいと感じた部分もあり、そう感じるなら自分ならどう作るか？を突き詰めようと考え、(多少リスペクトさせて頂いた部分はあるものの) 一から自身で方針等を考えて作り上げた。

2022/11/8 現在、予定しているテスト実装がやりきれていないなど完全ではないが一区切り付く所までは進めた。できていない部分や改善項目は、残課題として挙げる。

事前に色々調べるのと開発環境下準備に 1 ヶ月、開発に 7 末～ 8 頭＋ 10 ～ 11 頭の計 2 ケ月程かかった。

(技術要素は調べればいくらでも出てくるので割愛して) 本記事では、主に作成する上で考慮したことを記載する。

### React 学習経緯

フロントエンドはここ数年水面下で個人で学習をしてきた（最初は業務で活きる場面は来ないと思っていたが奇跡的に個人での学習が実を結び少しだけ実務経験を得ることができた）

この度、React を学習しようとした理由は大きく３つ。

- 業務で React を使用する機会がありそうだったこと。(残念ながらその機会は訪れず半分無駄となったが)
- フロントエンドの実務経験が、大規模レガシー SPA（jQuery ＋ HTML テンプレート）の改修/バグ修正 ＋ Graphana のカスタムプラグイン改修での HTML/CSS/JS 修正少々のみであること。フロントエンドが多少なりともできると言えるためには Vue/React/Angular/Svelte 等のライブラリ/フレームワークが使える必要があると思っており、そのレベルには到達しておきたかったため。
- 以下の点から、いずれは通らなければならない道であったこと。
  - 自身が個人で作ろうとしているプロダクトを開発する上で、かなりユーザビリティが良い GUI が必要であること
  - (CLI ツールはいくつか作ってきたが) GUI ツールを作れないと作れる物の幅が広がらないこと

元々 React の学習の優先順位は下げていたため１年位先の予定であったが、業務で必要になりそうだったために今回その優先順位を入れ替え前倒しで学習に取り組んだ。

※ React を選んだ理由は、過去個人で Vue を勉強したが肌に合わず挫折し、その後、某書で読んだ「HTML/CSS/JS (構造/見た目/動き) の分離は技術の分離であり関心の分離でない」といったような言葉(この通りであったかはうろ覚え)に衝撃を受けつつ激しく納得し、試しに React＆JSX に触れたらとても肌にあったこと。

## コーディング Tips

Todo：せっかくなので調べたことをまとめる

## フォルダ構成/コンポーネント構成

構成を考えるにあたり、以下などを参考にはした。

refs:

- [React ベストプラクティスの宝庫！「bulletproof-react」が勉強になりすぎる件](https://zenn.dev/meijin/articles/bulletproof-react-is-best-architecture)
- https://github.com/alan2207/bulletproof-react
- [SPA Component の推しディレクトリ構成について語る](https://zenn.dev/yoshiko/articles/99f8047555f700)
- [そのファイル、本当に hooks・utils に入れるんですか？React プロジェクトを蝕む「技術駆動パッケージング」](https://qiita.com/honey32/items/dbf3c5a5a71636374567)
- [俺流フロントエンドのディレクトリ構成と設計の考え方](https://baigie.me/engineerblog/?p=348) ※参考資料もためになる
- [React Folder Structure in 5 Steps [2022]](https://www.robinwieruch.de/react-folder-structure/)
- [Evolution of a React folder structure and why to group by features right away](https://profy.dev/article/react-folder-structure)

最近は features (機能) でまとめていくのがベストプラクティスなようである。ただ、始めは小規模ということもあり features フォルダを設けなくても良いだろうとの判断から以下のような構成にしていた。（参考元も記憶もロスト。atomic design ベース？ atomic design ベースの構成はアンチパターンらしいが小規模のため悪い面はそうでないだろうと判断して、やってみてダメだったら変えればいいとしたような気がする）

```
src/components
    |--elements
    |--models
    |   |--prefectures-selector         // 都道府県選択コンポーネント
    |   |   |--prefectures-selector.tsx
    |   |   |--usePrefectureQuery.ts
    |   |   |--useXxx.ts
    |   |   |--types.ts
    |   |--prefecture-population-graph  // 都道府県別人口グラフコンポーネント
    |       |--prefecture-population-graph.tsx
    |       |--usePopulationQuery.ts
    |       |--useXxx.tsx
    |       |--types.ts
    |--templates
    |--pages
        |--prefecture-statistical-graph-page  // 都道府県別人口グラフ表示ページ
            |--prefecture-statistical-graph-page.tsx
               // prefectures-selector と prefecture-population-graph を使用
```

が、上記の構成ではとある事に悩み、考えた結果 features を導入し、以下の通りの構成に変更した

```
src
|--components
|   |--elements
|   |--layouts
|   |--templates
|
|--features
    |--prefecture-statistical-graph
        |--api
        |   |--usePrefectureQuery.tsx
        |   |--usePopulationQuery.tsx
        |--components
        |   |--prefectures-selector.tsx  // 都道府県選択コンポーネント
        |   |--prefecture-population-graph.tsx  // 都道府県別人口グラフコンポーネント
        |--hooks
        |   |--usePrefectureState.tsx
        |   |--usePopulationState.tsx
        |--prefecture-statistical-graph.tsx 都道府県別人口グラフ表示ページ
        |--types.ts
```

### フォルダ構成の再検討

構成変更前は、以下のような違和感ありありの実装にしてしまっていた。

- 構成

```
src/components
    |--models
    |   |--prefectures-selector         // 都道府県選択コンポーネント
    |   |--prefecture-population-graph  // 都道府県別人口グラフコンポーネント
    |--pages
        |--prefecture-statistical-graph-page  // 都道府県別人口グラフ表示ページ
```

- prefecture-statistical-graph-page.tsx

```typescript
export const PrefectureStatisticalGraphPage = () => {
  const [prefectures, setPrefectures] = useState<Prefecture[]>([]);
  return (
    <>
      <PrefecturesSelector
        prefectures={prefectures}
        setPrefectures={setPrefectures}
      />
      <PrefecturePopulationGraph
        prefectures={prefectures.filter((pref) => pref.isSelected)}
      />
    </>
  );
};
```

- prefectures-selector.tsx

```typescript
export const PrefecturesSelector = ({ prefectures, setPrefectures }: PrefecturesSelectorProps) => {
  const updateSelectedPrefecture = useUpdateSelectedPrefecture(prefectures, setPrefectures);

  const { isLoading, prefectureResponseResult } = usePrefecturesQuery();  // api実行
  useSavePrefectures(prefectureResponseResult, setPrefectures); // 中にuseEffectを使用

  return (
    // 省略
  );
};
```

何故こうしたのか？

- prefectures (都道府県一覧) の state は、prefectures-selector と prefecture-population-graph の両方で必要になるため、その上位コンポーネントで管理する必要がある
- だが、prefectures-selector と prefecture-population-graph が必要とするロジックはそれぞれのコンポーネントと一緒に配置して知識の集約を図りたい

この 2 点満たそうとして気づけば上記のような実装にしてしまったが、setState (上記コードの setPrefectures) が剥き出しになるのは明らかに良くない（剥き出しになっている隙間で値の変更を許容してしまう）

何がいけなかったのか？ 恐らく機能の定義の仕方と変に分けてしまっていることが問題と考えた。

アプリが必要とする機能は「都道府県別人口グラフを表示する」機能であるため、この機能を構成するコンポーネントや hooks は部品と考えると、この機能を構成する３つのコンポーネント＆hooks をある意味バラけさせていたのが良くない。故に features フォルダを導入し、1 機能を構成する部品として 1 箇所に集約した。

そうすることで、当初の違和感を解消し、まとまりのある構成にすることができた。（ついてでに hooks も以下の通り、state と state を更新するロジックがひとまとまりになり、自然な形となった）

```typescript
export const PrefectureGraphPage = () => {
  const { prefectures, savePrefectures, updateSelectedPrefecture } =
    usePrefecturesState();

  return (
    <>
      <PrefecturesSelector
        prefectures={prefectures}
        savePrefectures={savePrefectures}
        updateSelectedPrefecture={updateSelectedPrefecture}
      />
      <PrefecturePopulationGraph
        prefectures={prefectures.filter((pref) => pref.isSelected)}
      />
    </>
  );
};
```

```typescript
export const PrefecturesSelector = ({
  prefectures,
  updateSelectedPrefecture,
  savePrefectures
}: PrefecturesSelectorProps) => {
  const { isLoading, prefectureResponseResult } = usePrefecturesQuery();

  const perfNamesKey = prefectureResponseResult?.map((result) => result.prefName).join('');
  useEffect(() => {
    savePrefectures(prefectureResponseResult);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [perfNamesKey]);

  return (
    // 省略
  );
};
```

※ useEffect をカスタムフックから外出ししたのは、1 コンポーネントに useEffect は 1 つ

ページコンポーネント(prefecture-statistical-graph-page)に presentation/container パターンを導入し、の presentation を pages 下に container と 部品を models に配置といったような手も選択肢として挙げることはできるかもしれないが、presentation/container パターンを導入する程の規模でもなく導入しても冗長かつ不要に複雑化を招く元になるため、今回は機能に関する物(知識)を 1 箇所に集約することを重視した。

## ステート管理

前提として、ステートには主に 3 種ある。

- サーバーデータのキャッシュ
  - SWR
  - React Query (Tanstack-Query)
- Global State
  - ページをまたいで保持し続ける必要のある State
    - Context
    - Redux
    - Recoil
    - Zustand
    - Jotai 等
- Local State
  - 各 Component 内で useState を使って管理
  - setState は直接露出させない

ref: [「3 種類」で管理する React の State 戦略](https://zenn.dev/yoshiko/articles/607ec0c9b0408d)

### サーバーデータのキャッシュ

API の仕様が変わることは(ほぼ)無い、レスポンスデータの更新も(恐らく)低頻度であることから、API を都度実行するよりキャッシュを利用するのが良いと判断

SWR よりは React-Query の方が 細かいところに手が届く感があり、先々機能追加をすること考えてもそう困らないと考えて採用

refs:

- [自分内 SWR vs React Query のメモ](https://zenn.dev/yoshiko/scraps/ff28fabafbc847)
- [React Query を使っていて気になった SWR とのいくつかの違い](https://dev.classmethod.jp/articles/react-query-or-swr/)

※ただし、いつレスポンスデータに更新が入っても早い段階で最新データが取れるように キャッシュの期限は 1 日に設定した

### Global State

Global State は大きく 2 種に分類できる

- React 外のストア
  - Redux (シングルステート)
  - Zustand (シングルステート、複数も可)
- React コンポーネントツリー内のストア
  - Recoil ※推測のため要確認 (複数可)
  - Jotai (複数可)
  - Context

(以下は推測) この２つの大きな違いは、以下ではないかと思っている

- React コンポーネントツリー内のストア： ステートの更新がコンポーネントの再レンダリングに直結する
- React 外のストア：React コンポーネントツリーから切り離されているため、裏側でステートの更新のみを行うことが可能なのではないか。例えば、(ユーザ操作や定期実行プロセスなどをトリガーに)画面表示とは非同期で行う処理（処理が終わればステートは更新するが画面表示は更新不要な処理等。まさに Redux のベースである Flux の仕組みが活きるような場面）

今回は、 React 外のストアは不要かつ、軽量なものでよいため、Jotai を選択した。

が、グローバルで管理するものが１つだけだったため、これも過剰で Context で十分だったように思う（改善項目）

※ Context を使用する上での工夫方法は以下が参考になる

refs:

- [本気で考える React のベストプラクティス！bulletproof-react2022](https://zenn.dev/t_keshi/articles/bulletproof-react-2022#%E7%8A%B6%E6%85%8B%E7%AE%A1%E7%90%86%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6)

- 不要な再レンダリングに対して、コンテキストを分割する方法：https://github.com/streamich/react-use/blob/master/docs/createReducerContext.md

- useContext の書き味が気に入らなければ、工夫次第で解決できる可能性がある：https://github.com/streamich/react-use/blob/master/src/factory/createStateContext.ts

## エラーハンドリング

React-Query でのエラーハンドリングに関しては以下が参考となった。

ref: [React Query Error Handling](https://tkdodo.eu/blog/react-query-error-handling#error-boundaries)

今回は、エラーケースを以下の通りに分類して実装をした。

- Client Error (400 番系)
  - 継続可能エラー として、Toast でエラーを表示するのみ（操作は引き続き可能）
- Server Error (500 番系) + その他予期せぬエラー(バグ)
  - 継続不能エラー として、エラー画面に遷移

API エラーレスポンスの振り分けは React-Query (Tanstack-Query) のオプションで実現した。

```typescript
export const errorBoundaryOption = {
  useErrorBoundary: (err: Error) => !(err instanceof ApiClientError),
  onError: (err: Error) => {
    if (err instanceof ApiClientError) {
      onCustomToaster(err); // Toast を表示
    }
  },
};
```

上記オプション利用側

```typescript
import { useQuery } from "@tanstack/react-query";

const queryResult = useQuery<
  PrefectureResponeseResult[],
  Error | ApiClientError
>(
  [PREFECTURES_QUERY_KEY],
  async () => apiClient.getPrefectures(),
  errorBoundaryOption
);
```

エラー画面の遷移には ErrorBoundary を利用して実現している。

※エラー画面には「トップに戻る」ボタンを用意しており、ボタン押下でトップ画面に戻った後は、ブラウザの戻るボタンを押しても、エラー画面には戻らないようにしている。不必要に(継続不能エラーが起きた時以外)エラー画面を開くことがないようにするためと考えて

## CSS

選択肢として以下を挙げた

- CSS modules
- CSS in JS
  - styled-component
  - emotion
- ※ゼロランタイム CSS in JS はまだ発展途上感がありそうだったため一旦見送り

CSS in JS は、移植性の観点から emotion > styled-component と速攻で判断。

CSS modules でも十分と思ったが以下の点から先を見据えて、かつパフォーマンスが CSS Modules > CSS in JS といえど今回の作成物では問題にならない程度と判断し emotion を使用することとした。

- (今後今回の作成物を実験台にしようと思っていることもあり) theme（ノーマルモード/ダークモード）の導入を行いたいと考えている (CSS Modules でもできなくはないが手間が大きいらしい)
- (実際にやってみて特に感じたことだが) 1 ファイルに HTML と CSS 両方ある方が開発しやすく、CSS Modules の場合命名規則をどうするかを悩んだがそこに悩むのも嫌であった (開発者体験を優先)
- CSS Modules を使用する上でフォーマット等に使用したい Stylelint がまだ ESM 未対応(2022/11/6 時点) ref: [stylelint: Move to ESM ](https://github.com/stylelint/stylelint/issues/5291)
  ※結局使用している別の何かが ESM 未対応のため、ESM に移行しきれていない

### styled components を使用する上で考慮したこと

多少参考にさせて頂いた物のコードを見ていると、styled components と そうでないコンポーネント(自前で作った React Component) の見分けがし辛く、可読性が悪いと感じた。

故に、styled components のメリット/デメリットを調べた。以下の通り。

ref: [The Pros and Cons of Using Styled Components in React](https://www.makeuseof.com/styled-components-react-pros-cons/)

- メリット
  - CSS の特異性の問題を解決（クラス名の衝突）
  - コンポーネント内に CSS を記述できる
    - コンポーネントのすべての機能を 1 つのファイルに格納できる
  - すぐに使えるテーマ設定をサポート
    - ダーク テーマやその他のテーマをアプリケーションに追加するのは難しく時間がかかるが、容易に実現できる
- デメリット
  - JS で CSS を書くと、将来的に 2 つを分離することが難しくなり、保守性が大幅に低下する（例：JavaScript フレームワークを切り替える場合、ほとんどのコードベースを書き直す必要がでてくる）※CSS モジュールや emotion のようなライブラリを使用すれば将来性は高まる
  - ★ 読みにくい場合がある
    - Styled Component と React Component を区別することは、特にアトミックデザインシステムの外では難しい場合がある
    - Styled Component のみをラッパーとして使用し、その中の要素にセマンティック HTML タグを使用することで、この問題を解決はできる。以下のように別ファイルに分けるとより明確にできる

```typescript
import * as styled from "./styled";
// use styled.components
<styled.Main>{code}</styled.Main>;
```

更に、デメリットとして、Styled Components は簡単すぎて、初歩の構造を隠蔽する事が挙げられるとのこと。

ref: [Styled Components を無闇に使わないで](https://zenn.dev/yhase_rqp/articles/db63567117c110)

```typescript
export const Button = styled.button<Props>`
  height: 40px;
  padding: 0 16px;
  border-radius: 4px;
  ${colorStyle}
`;

Button.displayName = "Button";
```

実態は以下

```typescript
// React.forwardRefでラップする構文を使い、refを受け取れるようにする
export const Button = React.forwardRef<Ref, Props>((props, ref) => {
  // classNameを追加でマージできるようにする (1)
  const { color, className, ...rest } = props;

  return (
    <button
      ref={ref}
      // classNameを追加でマージできるようにする (2)
      className={cx(styles.root, styles[`root__color_${color}`], className)}
      // button要素が持つpropsでclassName以外のものは、そのまま受け流す
      {...rest}
    />
  );
});
```

上記の通り、Styled Components の使用は無意識的に ref の多用に繋がるため実はあまりよくないのではないか？ カプセル化されているため実害はそうないように感じるかもしれないが、ref には DOM 情報が保持されるため、多用すればする程メモリを喰うのではないか？ ＝ 塵も積もればパフォーマンスに影響が出る可能性があるかもしれない（推測）。

### emotion を実際に使う上での方針

- (emotion の) styled components を使用する際

  - 以下のようにして、使用シーンを限定する
    > Styled Component のみをラッパーとして使用し、その中の要素にセマンティック HTML タグを使用することで、この問題を解決はできる
  - (とは言っても 1 HTML 要素 に 多くの CSS を設定する/それを再利用する場合には、利用したくなるように思うため)、コンポーネント名に 接頭辞 (例：Styled) を付けるなど、見分けやすくするための規約を定める
  - (見た目だけ加工したコンポーネントと、ロジックを伴うコンポーネントをパッと見で見分けにくいのが一番の問題と感じたため)presentation/container パターンを適用して、presentation コンポーネント側に隔離する

など、使用範囲の限定や見分けやすくすための規約が必要に思う。※今回は試したいがためにわざと一部に styled components を使用し、2 点目の方針を採用している。今回作成したものに関しては基本的に styled components を使用して旨味のある箇所がないためわざと使用した部分以外には使用していない。

また、わざと使用した部分に関しては margin や padding 等の余白調整をするためのスタイル(ユーティリティ層相当の物)は外側から注入できるようにしている。コンポーネントを使用したい場所の枠に応じて幅/余白等を調整できるようにするとコンポーネントの再利用性が増す。

外からスタイルを注入できるようにしようとすると、以下のようになる訳だが、毎度以下のように書くのは面倒なため

```typescript
export const StyledTitle = styled.h2(
  (props: StyledProps) =>
    css`
      margin: 0;
      ${props.css}
    `
);

export type StyledProps = {
  css?: SerializedStyles;
};
```

以下のようなちょっとした共通化の工夫は入れた。

```typescript
export const StyledTitle = styled.h2(
  cssMerger(css`
    margin: 0;
  `)
);

export const cssMerger = (styles: SerializedStyles) => (props: StyledProps) =>
  css`
    ${styles}
    ${props.css}
  `;
```

- theme について
  - 後々追加したいとは思っているが、現状使用しないため emotion の [theming](https://emotion.sh/docs/theming) の機能は利用していない
  - 理由は、公式 Doc のベストプラクティスにて [アプリが複数のテーマをサポートする (または最終的に複数のテーマをサポートする) 場合を除き、テーマを使用しないでください](https://emotion.sh/docs/best-practices#dont-use-a-theme-unless-your-app-supports-multiple-themes-or-will-eventually-support-multiple-themes) とあるため。「アプリのテーマが 1 つしかない場合は、色やその他のスタイル変数を JavaScript 定数として定義する方が簡単」なため、アプリのテーマカラー等の共通のスタイルは、グローバル定数として定義した。

将来利用する可能性があるとはいえ、必要になってから入れるとしても何ら問題はないため、利用する時になってから導入することとした。

- 各コンポーネントでの CSS の定義
  - 基本的に styled components は使わず、各コンポーネントに以下のように固めて定義している
  - ※CSS は、子要素のスタイルを設定するときに親要素のスタイルの内容も考慮する必要があるため、個人的には以下のように(コンポーネント内の全要素の)CSS が一か所まとまっている方が調整がしやすいと思っている

```typescript
const styles = {
  foundation: css`
    box-sizing: content-box;
  `,
  container: css`
    box-sizing: content-box;
    position: relative;
  `,
  border: css`
    border: 1px solid ${commonStyles.themeColor};
  `,
  title: css`
    background-color: white;
    padding: 1px 3px;
    margin: 0;
    position: absolute;
    top: 0;
    left: 0;
    transform: translateY(-50%) translateX(${10 / 16}rem);
  `,
  body: css`
    padding: 1rem;
  `,
};

export const TitleBodyLayout = ({
  title,
  children,
  existsBorder = false,
  additionalStyles,
}: TitleBodyLayoutProps) => {
  const containerStyles = existsBorder
    ? [styles.container, styles.border]
    : [styles.container];
  return (
    <div css={[styles.foundation, additionalStyles]}>
      <div css={containerStyles}>
        <p css={styles.title}>{title}</p>
        <div css={styles.body}>{children}</div>
      </div>
    </div>
  );
};
```

## テスト

Todo: 近日記載

現状ロジックのテストは入れている（Github Actions で実行）

## Github Pages

アプリは Github Pages にデプロイしたが、

react-router-dom の BrowserRouter を使用している場合は、以下の通り直接 URL を踏むを Github の 404 ページに遷移してしまうため、対応が必要である。

ref: [React で gh-pages にデプロイしたとき、直接 URL を踏むと 404 が返る問題への対応](https://qiita.com/takuya0206/items/f284b5e68f48f1ebefae)

- 原因：ブラウザーはその URL のサーバー (この場合は GitHub ページ サーバー) を要求するが、この時点でクライアント側のルーター (react-router) は、そのページをまだ読み込めていないため、アクションを実行できず、404 が出る。

- 対処：以下の 404.html と index.html の script をコピペする

[rafgraph/spa-github-pages](https://github.com/rafgraph/spa-github-pages)

Vite を使用している場合 そのままではリダイレクト先の URL が `https://username.github.io/?/repo-name/` になってしまうため 404.html 内の `var pathSegmentsToKeep` を 1 にする（ そうすれば URL が `https://username.github.io/repo-name/?/` になり正常に動く）

### Github Pages 時のみ専用スクリプトを取り込む

上記の対処で追加する 404.html と index.html の script は Github Pages デプロイ時以外は不要な物のため、Github Pages 用のビルド時のみ取り込むようにした。

404.html の取り込みは vite.config.ts の設定を以下のようにして実現した。

```typescript
export default defineConfig({
  build: {
    target: 'esnext',
    rollupOptions: {
      input: process.env.GITHUB_PAGES
        ? {
            index: `${__dirname}/index.html`,
            notfound: `${__dirname}/404.html`
          }
        : {
            index: `${__dirname}/index.html`
          }
    }
  },
```

また、index.html 内の script は 以下をヒントに、置換にて Github Pages デプロイ時のみスクリプトを取り込むようにした。

[Vite 環境で index.html から環境変数を参照する](https://dev.classmethod.jp/articles/vite-index-html-read-env-variables/)

```typescript
// ref: https://dev.classmethod.jp/articles/vite-index-html-read-env-variables/
// ref: https://vitejs.dev/guide/api-plugin.html#transformindexhtml
const htmlPlugin = () => {
  return {
    name: "html-transform",
    enforce: "pre" as const,
    transformIndexHtml(html: string) {
      return html.replace(
        /    %SCRIPT_FOR_GITHUB_PAGES%/g,
        process.env.GITHUB_PAGES
          ? fs.readFileSync("./ghpages/script.txt", "utf8")
          : ""
      );
    },
  };
};
```

（もっと良いやり方はありそう…）

## その他参考になりそうなもの

Todo: 近日記載

- [フロントエンドのデザインパターン](https://zenn.dev/morinokami/books/learning-patterns-1/viewer/introduction)

※ コードを置いてるリポジトリ（https://github.com/Symthy/react-clone-yumemi-exam）に作成するにあたって色々調べたことはほぼ memo_xxx.md に記載している。参考までに

## 残課題

Todo: 近日記載

改善タスク：

- テスト (コンポーネント単位のテスト、E2E テスト※主に画面遷移)
- Jotai → Context に変更
- エラー型付け ref: https://labs.septeni.co.jp/entry/2020/07/23/100000#%E3%81%BE%E3%81%A8%E3%82%81
- react-dev-tool warning 解消
- 開発環境改善 ref: https://qiita.com/kztmk_media_pep/items/11d063a155d414a102b1

Suspsense について

- useQueries の対応が完全ではない？ようなので導入見送り
  ref: [TanStack/query#1523](https://github.com/TanStack/query/issues/1523)
- そもそも Suspsense 導入できるコンポーネントが 1/3 のため導入するメリットも今はあまりない（必要になったらで良い）

## さいごに

Todo
