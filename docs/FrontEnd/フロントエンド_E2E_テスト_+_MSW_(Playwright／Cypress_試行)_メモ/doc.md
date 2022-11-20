# フロントエンド E2E テスト + MSW (Playwright/Cypress 試行) メモ

## E2E テストフレームワーク

色々あるが、本記事で触れるのは Playwright と Cypress

以下４つの比較がある。 ref:[E2E テストツール Autify を使うまでの話](https://teamspirit.hatenablog.com/entry/2020/04/17/150000)

- TestCafe
- WebDriverIO
- Cypress.io
- Autify (有料)

以下３つの比較がある。 ref: [E2E テストフレームワークはどれを選べばいいんじゃい！](https://zenn.dev/taiga533/articles/f6e1ef07a8676e)

- Cypress
- Playwright
- CodeceptJS

## Playwright

- 自動生成機能が強力
- VRT(Visual Regression Test)も可能。スナップショットの一致精度の調整も可能(薄く始めることもできそう。React へ移行時に使用した例： [Playwright & Vite ではじめる脱レガシー向け軽量 Visual Regression Test](https://blog.cybozu.io/entry/2022/03/18/100000)
- クロスブラウザテスト（Chromium, Firefox, WebKit）が可能（割と速い）

導入：

```
npm i -D @playwright/test msw
npx playwright install
```

コード自動生成（画面操作によってコードが自動的に作られる）※playwright-cli が統合された

```
npx playwright codegen https://yahoo.co.jp
```

参考：

- [react+vite を playwright+msw で自動テストする](https://zenn.dev/dyoshikawa/articles/07ab82a5cbcde0)
- [PlayWright を使って E2E テストを書いてみた](https://www.cresco.co.jp/blog/entry/14335/)

## Cypress

テスト時に特定の要素を取得する際は、`data-*`属性を追加し、アプリ側の変更でテストへ影響が及びにくくする。

ref: [Best Practice](https://docs.cypress.io/guides/references/best-practices#Selecting-Elements)

e2e テスト時にしか使用しない属性であれば、本番環境で余分になるものを含めないように、e2e テスト時のみ追加するような工夫をするのが良い（はず）。

```typescript
export const makeAttrForTest = (label: string) => {
  if (process.env.VITE_E2E_MODE) {
    return { "data-test": label };
  }
  return {};
};
```

※Vite を使用していてコードに import.meta.env.VITE_XXXX での分岐を入れているとうまくいかないので、以下で置き換えを行う必要があった（置換ライブラリはいくつかあるが何が最適化分からないため archive されていなかった以下をひとまず使用）

```typescript
// vite.config.ts
import env from "vite-plugin-env-compatible";
// ref: https://github.com/IndexXuan/vite-plugin-env-compatible

export default defineConfig({
  plugins: [env({ prefix: "VITE", mountedPath: "process.env" })],
});
```

その他参考

- 導入：
  - [Typescript Deep Dive - Cypress (導入)](https://typescript-jp.gitbook.io/deep-dive/intro-1/cypress)
  - [Cypress を TypeScript でセットアップする際のメモ](https://zenn.dev/himorishige/scraps/12952f7af8f80e)
- コマンド化もできる
  - [Future Tech Blog - Cypress - 設定編](https://future-architect.github.io/articles/20210428b/)
- 公式 Doc：
  - [Cypress Doc - Testing Your App](https://docs.cypress.io/guides/end-to-end-testing/testing-your-app#What-you-ll-learn)
  - [Cypress Doc - Configuration](https://docs.cypress.io/guides/references/configuration#Configuration-File)

## MSW のレスポンス上書き設定

window オブジェクトに msw を挿入することでテストコードから操作できるようになる

refs:

- Cypress での例: [MSW - use - One-time Override](https://mswjs.io/docs/api/setup-worker/use#one-time-override)
- [Github - mswjs](https://github.com/mswjs/msw/blob/ec57fbf1a8642e08d25a759bf86ea7885e5d5de5/test/msw-api/setup-worker/use.mocks.ts#L12-L17)

上記だけではうまくいかなかった。アプリ側での MSW の起動を e2e テスト側で待つ必要がある

ref: [Cypress issues when using window.msw](https://github.com/mswjs/msw/issues/1052)

```typescript
beforeEach(() => {
  cy.visit("/");
  // Wait for MSW server to start
  cy.window().should("have.property", "appReady", true);
});
```

※ Playwright でも、window オブジェクトに msw を挿入するだけではうまくいかなかった。上記と同じように待ち合わせが必要かもしれない。Playwright の場合は以下も参考になるかも

[playwright-msw](https://github.com/valendres/playwright-msw/blob/main/packages/example/tests/playwright/specs/rest.spec.ts)

## mswjs/data

- 仮想 DB をブラウザ（インメモリ）に展開する、データモデリング・リレーションライブラリ
- ORM 風な API を提供
- UI のみをテストしたいのであれば MSW 単体で十分。mswjs/data が活きるのは、画面を横断する E2E テストケース（別画面操作による更新内容/状態を引き継げる）

採用モチベーション：

- 実際の DB・バックエンドが揃う前に、アプリケーション E2E テスト実施可能
- 従来のテストインフラ整備と比較し、軽量・手軽に E2E テストが実施可能

ref: [mswjs/data で広がるテスト戦略](https://zenn.dev/takepepe/articles/msw-data-userflow-testing)

## Github Actions (Cypress)

以下がとても参考になった。

- [GitHub actions に Cypress の CI を実装してみた話](https://zenn.dev/convers39/articles/e1531d487ac448)

実際にやってみた。

https://github.com/Symthy/react-clone-yumemi-exam

公式ドキュメント:

- [Cypress Doc - GitHub Actions](https://docs.cypress.io/guides/continuous-integration/github-actions#Explicit-Version-Number)

## さいごに

簡単な E2E テスト（MSW を利用した正常系と異常系）を実装してみた

https://github.com/Symthy/react-clone-yumemi-exam

個人的には Playwright の方が開発者体験が良く（テストコードが実際に画面を操作して自動で生成される）、こちらを使用したかったが

MSW の設定上書きがうまくいかず（window オブジェクトに msw の注入がうまくいかず）

MSW の公式ドキュメントに Cypress の例があるため、Cypress なら確実にできるだろうと考え、Cypress を使用して事なきを得た。

今回のように小規模のテストであれば、Cypress でも苦はないが、テストの内容が大きくかつ複雑化してくると、多くのコードを書く必要が出てくるため、やはり苦しくなりそうである。
