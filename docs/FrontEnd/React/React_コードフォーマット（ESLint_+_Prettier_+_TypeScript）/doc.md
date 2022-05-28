# React コードフォーマット（ESLint + Prettier + TypeScript）

XXXX 番煎じ。3 年前に webpack で一から設定したことがあるが年月経っている上、React でやるのは初めてなので残す

## Code Format

- Prettier : コードスタイルのフォーマッタ。 ESLint とは異なり、コードスタイルのみをフォーマット
- ESLint : 問題や構文エラーを検索し、コードスタイルをよりきれいにする

※max-len、no-mixed-spaces-and-tabs、keyword-spacing、カンマスタイルなどのルールは、Prettier でよく使われているフォーマットルール。

※no-unused-vars、no-extra-bind、no-implicit-globals、prefer-promise-reject-errors などのルールは ESLint の一般的なルール。

ref: [ESLint + Prettier + Typescript and React in 2022](https://blog.devgenius.io/eslint-prettier-typescript-and-react-in-2022-e5021ebca2b1) ※eslint-plugin-prettier 使ってるので良い手順か怪しい

以下 `npx create-react-app task-mgmt-app-clone --template=typescript` を行ったあとの手順

### ESLint インストール

```
npm install eslint --save-dev
npx eslint --init

Need to install the following packages:
  @eslint/create-config
Ok to proceed? (y) y

? How would you like to use ESLint? ...
  To check syntax only
  To check syntax and find problems
> To check syntax, find problems, and enforce code style

√ How would you like to use ESLint? · style
? What type of modules does your project use? ...
> JavaScript modules (import/export)
  CommonJS (require/exports)
  None of these

? Which framework does your project use? ...
> React
  Vue.js
  None of these

? Does your project use TypeScript? » No / Yes

? Where does your code run? ...  (Press <space> to select, <a> to toggle all, <i> to invert selection)
√ Browser
√ Node

? How would you like to define a style for your project? ...
> Use a popular style guide
  Answer questions about your style

? Which style guide do you want to follow? ...
> Airbnb: https://github.com/airbnb/javascript
  Standard: https://github.com/standard/standard
  Google: https://github.com/google/eslint-config-google
  XO: https://github.com/xojs/eslint-config-xo

? What format do you want your config file to be in? ...
> JavaScript
  YAML
  JSON

? Would you like to install them now? » No / Yes

? Which package manager do you want to use? ...
> npm
  yarn
  pnpm
```

↓ 必要なものを入れる

```
npm install -D eslint-plugin-react@latest @typescript-eslint/eslint-plugin@latest @typescript-eslint/parser@latest
npm install -D eslint-plugin-import @typescript-eslint/parser eslint-import-resolver-typescript
npm i --save-dev eslint-plugin-unused-imports
npm i --save-dev eslint-config-airbnb-typescript
npm i -D eslint-plugin-import
// npx install-peerdeps --dev eslint-config-airbnb
```

### Prettier インストール & ESLint 設定

```
npm i -D prettier eslint-config-prettier
```

eslintrc.js 編集。

```javascript
module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    'plugin:react/recommended',
    'airbnb',
+   'airbnb-typescript'
+   'airbnb/hooks',
+   'plugin:@typescript-eslint/recommended',
+   'plugin:@typescript-eslint/recommended-requiring-type-checking',
+   'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
+    tsconfigRootDir: __dirname,
+    project: ['./tsconfig.json'],
  },
  plugins: [
    'react',
    '@typescript-eslint',
+   'unused-imports', // 使っていないimportを自動で削除用
  ],
+ "ignorePatterns": [
+   ".eslintrc.js"
+ ],
  rules: {
+   'no-use-before-define': 'off', // 関数や変数が定義される前に使われているとエラーになるデフォルトの機能off
+   '@typescript-eslint/no-use-before-define': 'off',
+   'import/prefer-default-export': 'off', // named exportがエラーになるので使えるようにoff
+   '@typescript-eslint/no-unused-vars': 'off', // unused-importsを使うため削除
+   'unused-imports/no-unused-imports': 'error', // 不要なimportの削除
+   'unused-imports/no-unused-vars': [ // unused-importsでno-unused-varsのルールを再定義
+     'warn',
+     { vars: 'all', varsIgnorePattern: '^_', args: 'after-used', argsIgnorePattern: '^_' },
+   ],
+   "react/function-component-definition": [ // アロー関数以外受け付けない設定
+     2,
+     {
+       namedComponents: "arrow-function",
+       unnamedComponents: "arrow-function",
+     },
+   ],
+   'no-param-reassign': [ // パラメーターのプロパティ変更を許可
+     2,
+     { props: false }
+   ],
+   'import/extensions': [ // importのときに以下の拡張子を記述しなくてもエラーにしない
+     'error',
+     {
+       js: 'never',
+       jsx: 'never',
+       ts: 'never',
+       tsx: 'never',
+     },
+   ],
+   'react/jsx-filename-extension': [ // jsx形式のファイル拡張子をjsxもしくはtsxに限定
+     'error',
+     {
+       extensions: ['.jsx', '.tsx'],
+     },
+   ],
+   'react/react-in-jsx-scope': 'off', // import React from 'react'が無くてもエラーを無くす
+   'react/prop-types': 'off', // TypeScriptでチェックしているから不要。offにする
+   'no-void': [ // void演算子の許可
+     'error',
+     {
+       allowAsStatement: true,
+     },
+   ],
+ },
+ settings: {
+   'import/resolver': {
+     node: {
+       paths: ['src'],
+       extensions: ['.js', '.jsx', '.ts', '.tsx']
+     },
+   },
+  },
};
```

補足

1. アロー関数

以下を設定しないと

```javascript
"react/function-component-definition": [ // アロー関数以外受け付けない設定
  2,
  {
    namedComponents: "arrow-function",
    unnamedComponents: "arrow-function",
  },
],
```

以下の書き方ができない（ESLint に function App() の形にフォーマットされる）

```javascript
export const App = () => (
  <div className="App">
    <header className="App-header" />
  </div>
);
```

ref: https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/function-component-definition.md

2. 不要 import

plugings に 'unused-imports' を入れ忘れると、import 文で `unused-imports/no-unused-imports` のエラーが出る

```javascript
plugins: [
  'react',
  '@typescript-eslint',
  'unused-imports' // 使っていないimportを自動で削除用
],
```

3. import 整列

### refs

- ★[【VSCode】React と TypeScript、ESLint、Prettier、Airbnb で環境構築する手順](https://yumegori.com/vscode_react_typescript_eslint_prettier)

- [React+TypeScript+ESLint+Prettier をまとめて環境構築](https://zenn.dev/jpn_asane/articles/d7f44682b74fdc)

- [Airbnb vs Standard – ESLint のスタイルは何を選ぶべきか？](https://delicateprogrammer.com/airbnb-vs-standard/)

  - Airbnb: セミコロン省略しない。チェックして欲しいもの大体見てくれる
  - Standard: セミコロン省略する。緩い

- [いつのまにか eslint-plugin-prettier が推奨されないものになってた](https://knote.dev/post/2020-08-29/duprecated-eslint-plugin-prettier/)

  - とっくの昔（2020 年位）に非推奨になっている（忘れないように）

- [react/function-component-definition](https://github.com/jsx-eslint/eslint-plugin-react/blob/master/docs/rules/function-component-definition.md)

import の整列をしたいときは以下参照。（自身のプロジェクトのフォルダ構成に合わせて好きな順になるよう pathGroups を指定することになる）

- [React + TypeScript import 順をキレイにしたい](https://chaika.hatenablog.com/entry/2022/01/17/083000)

- [ESLint で import の整列・追加・削除を自動化する](https://qiita.com/yukiji/items/5ba9e065ac6ed57d05a4)

- [eslint-plugin-import](https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules/order.md)
