# React 基本メモ

## コンセプト

- Declarative（宣言的）
    - 宣言的プログラミング：出力の性質やあるべき状態を記述してプログラムを構成する。関数型プログラミング含む。
- Component-Based（コンポーネントベース）

- Just The UI（UI にしか関知しない）

- Virtual DOM（仮想DOM）

- One-Way Dataflow（単方向データフロー）
    - 双方向データバインディングはシンプルなアプリケーションでは直感的であっても、多くの 状態を持つ大規模のアプリケーションでは複雑化(アンチパターン)
    - React における単方向データフローとは、データがコンポーネントツリーを親から子コンポーネントの方向のみに props という形で渡る。子から親に逆流しない
    - 単方向データフローは関数型プログラミングとすごく相性がいい
- Learn Once, Write Anywhere（ひとたび習得すれば、あらゆるプラットフォームで開発できる）

### stateのリストアップ

子に親のstateを更新する関数を譲渡、子の変更＝直接親のstate更新。(子→親の向けなので)リフトアップ

例：フォームを実装

- 前提：親コンポーネントは、フォームの各パーツを子コンポーネントを持つ
- 親コンポーネントでフォームデータを自身の state（状態）として持ち
- その state を変更する関数を、子コンポーネントに props として渡す。
- 子コンポーネントに渡した関数を、フォームパーツにセット、操作の際にその関数を実行

## コンポーネントとprops

props = properties。`{ 属性名: 属性値 }` の形式。

- コンポーネントにとっての最大の関心事は props と state。断然propsの方が重要
    - state は極力コンポーネントに持たせるべきではない。state を持つコンポーネントの数もコンポーネントが持つstate の数も最小限にするべき
    - 関数型プログラミングによってアプリケーションの UI を宣言的に記述するというReact
      の思想を具現化するためには、stateは副作用の原因となる（コンポーネントを純粋関数ですべて表現できれば、アプリケーション全体における副作用を完全に排除できる）

関数コンポーネント推奨。

### コンポーネントライフサイクル

1. Mounting フェーズ： コンポーネント初期化、仮想DOMにマウントされるまでのフェーズ。このフェーズで初めてコンポーネントがレンダリングされる
2. Updating フェーズ： 差分検出処理エンジンが変更を検知してコンポーネントが再レンダリングされるフェーズ
3. Unmounting フェーズ： コンポーネントが仮想DOMから削除されるフェーズ
4. Error Handling フェーズ： 子孫コンポーネントのエラーを検知、捕捉するフェーズ

[コンポーネントライフサイクル図](https://projects.wojtekmaj.pl/react-lifecycle-methods-diagram/)

## <記載中>

## 実装（基本）

[チュートリアル](https://ja.reactjs.org/tutorial/tutorial.html)

## サンプル

create-react-app すると以下ができるイメージ

```
.
|--package.json
|--package-lock.json
|--public
|  |--index.htm
|--src
|  |--App.js
|  |--index.js
|  |--styles.css
```

```js
// index.js
import { StrictMode } from "react";
import ReactDOM from "react-dom";
import App from "./App";

const rootElement = document.getElementById("root");
ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  rootElement
);
```

```js
// App.js
import "./styles.css";

export default function App() {
  return (
    <div className="App">
      <h1>Hello CodeSandbox</h1>
      <h2>Start editing to see some magic happen!</h2>
    </div>
  );
}
```

### JSX

#### HTML記述

返却するHTML要素は、1タグで囲われていなければならない

- 単一

```js
import React from 'react';
import ReactDom from "react-dom";

const App = () => {
  return <h1>Hello</h1>;
}

ReactDom.render(<App />, document.getElementById("root"));
```

- 複数

`<div>`で囲うと余計な要素がレンダリングされる。その時は`<React.Fragment>`で囲う。

`<React.Fragment>`は`<>～</>`で省略可

```js
import React from 'react';
import ReactDom from "react-dom";

const App = () => {
  return (
    <>
      <h1>Hello</h1>
      <p>topic</p>
    </>
  );
}

ReactDom.render(<App />, document.getElementById("root"));
```

#### コンポーネント

コンポーネント名は必ず先頭を大文字。推奨：パスカルケース

```jsx
// App.jsx
import React from 'react';

const App = () => {
  return (
    <>
      <h1>Hello</h1>
      <p>topic</p>
    </>
  );
}

export App;
```

```js
// index.js
import React from 'react';
import ReactDom from "react-dom";
import App from "./App";

ReactDom.render(<App />, document.getElementById("root"));
```

#### イベント実装

```jsx
import React from 'react';

const App = () => {
  const onClickHandler = () => alert();
  return (
    <>
      <h1>Hello</h1>
      <button onClick={onClickHandler}></button>
    </>
  );
}

export App;
```

#### スタイル実装

CSSのプロパティ名もキャメルケースで書く

```jsx
// App.jsx
import React from 'react';

const App = () => {
  const textStyle = {
    color: 'blue',
    fontSize: '16px'
  };
  return (
    <>
      <h1 style={{ color: 'red' }}>Hello</h1>
      <p style={textStyle}>topic</p>
    </>
  );
}

export App;
```

### props

- コンポーネントに渡す引数のようなもの。
- props で条件などを渡して表示を切り替える。

```jsx
// components/Message.jsx  受け取る側
import React from 'react';

const Message = (props) => {
  const textStyle = {
    color: props.color,
    fontSize: '16px'
  };
  return (
    <p style={textStyle}>{props.message}</p>
  );
}

export Message;
```

```jsx
// App.jsx  渡す側
import React from 'react';
import Message from './components/Message';

const App = () => {
  const onClickHandler = () => alert();
  return (
    <>
      <h1 style={{ color: 'red' }}>Hello</h1>
      <Message color="blue" message="topic" />
      <button onClick={onClickHandler}></button>
    </>
  );
}

export default App;
```

- コンポーネントタグで囲った値は props.children で渡る
- propsには分割代入を使うべし

```jsx
// components/MessageTwo.jsx  受け取る側
import React from 'react';

const MessageTwo = (props) => {
  const { color, children } = props;
  const textStyle = {
    color,  // プロパティ名と変数名同じなら省略可
    fontSize: '16px'
  };
  return (
    <p style={textStyle}>{children}</p>
  );
}

export default MessageTwo;
```

```jsx
// App.jsx  渡す側
import React from 'react';
import MessageTwo from './components/MessageTwo';

const App = () => {
  const onClickHandler = () => alert();
  return (
    <>
      <h1 style={{ color: 'red' }}>Hello</h1>
      <MessageTwo color="green">topic2</MessageTwo>
      <button onClick={onClickHandler}></button>
    </>
  );
}

export App;
```

### State (useState)

コンポーネントの状態。状態が変わると再レンダリングされる。

- useState()： State(値)とセッターを取得する

例：カウントアップ

```jsx
// App.jsx  渡す側
import React, { useState } from 'react';

const App = () => {
  const [num, setNum] = useState(0);
  const onClickCountUp = () => {
    setNum(num + 1);
  };
  return (
    <>
      <h1 style={{ color: 'red' }}>Hello</h1>
      <button onClick={onClickCountUp}>count up</button>
    </>
  );
}

export App;
```

### 再レンダリングと抑止 (useEffect)

コンポーネントが再レンダリングされる条件

- Stateが変更された時
- propsで受け取る値が変わった時
- 親コンポーネントが再レンダリングされた時

#### バグる例

以下をベースに

```jsx
// App.jsx  渡す側
import React, { useState } from 'react';

const App = () => {
  const [isShow, setShowFlag] = useState(true);
  const onClickCountUp = () => {
    setNum(num + 1);
  };
  const onClickChange = () => {
    setShowFlag(!isShow);
  };
  return (
    <>
      <h1 style={{ color: 'red' }}>Hello</h1>
      <button onClick={onClickChange}>on/off</button>
      {isShow && <p>★★★</p>}
    </>
  );
}

export App;
```

機能追加する：3の倍数の時に表示（Too many re-renders.)

- 以下では、再レンダリングした際に、stateの値が変更されるので無限再レンダリングされる

```jsx
// App.jsx  渡す側
import React, { useState } from 'react';

const App = () => {
  const [isShow, setShowFlag] = useState(true);
  const onClickCountUp = () => {
    setNum(num + 1);
  };
  const onClickChange = () => {
    setShowFlag(!isShow);
  };

  if (num % 3 === 0) { // stateの値が変わるので無限再レンダリング
    setShowFlag(true);
  } else {
    setShowFlag(false);
  }

  return (
    <>
      <h1 style={{ color: 'red' }}>Hello</h1>
      <button onClick={onClickCountUp}>count up</button>
      <br />
      <button onClick={onClickChange}>on/off</button>
      {isShow && <p>★★★</p>}
    </>
  );
}

export App;
```

- 対策後 (true -> true, false -> false の無駄な上書きしないようにする)
    - だが、on/off が利かなくなる

```jsx
// App.jsx  渡す側
import React, { useState } from 'react';

const App = () => {
  const [isShow, setShowFlag] = useState(true);
  const onClickChange = () => {
    setShowFlag(!isShow);
  };

  if (num > 0) {  // 対策後
    if (num % 3 === 0) {
      isShow || setShowFlag(true);
    } else {
      isShow && setShowFlag(false);
    }
  }

  return (
    <>
      <h1 style={{ color: 'red' }}>Hello</h1>
      <button onClick={onClickCountUp}>count up</button>
      <br>
      <button onClick={onClickChange}>on/off</button>
      {isShow && <p>★★★</p>}  // ボタン押下 → 再レンダリング. isShowはnumに応じて決まるため機能しない
    </>
  );
}

export App;
```

別の機能が影響してバグる（num表示とon/off機能）。その場合はuseEffectを使って関心を分離する必要がある。

#### useEffect で関心を分離

- 最初の一回のみ実行（第二引数を空配列にする）

```jsx
useEffect(() => {
  // ここに書いた処理は最初の一回しか実行されない
}, []);
```

- stateの値が変わった時のみ実行

```jsx
const [num, setNum] = useState(0);

useEffect(() => {
  // num が変わった時だけ処理実行
}, [num]);
```

```jsx
// App.jsx  渡す側
import React, { useState } from 'react';

const App = () => {
  const [isShow, setShowFlag] = useState(true);
  const onClickChange = () => {
    setShowFlag(!isShow);
  };

  useEffect(() => {
    if (num > 0) {
      if (num % 3 === 0) {
        isShow || setShowFlag(true);
      } else {
        isShow && setShowFlag(false);
      }
    }
  }, [num]);

  return (
    <>
      <h1 style={{ color: 'red' }}>Hello</h1>
      <button onClick={onClickCountUp}>count up</button>
      <br>
      <button onClick={onClickChange}>on/off</button>
      {isShow && <p>★★★</p>}
    </>
  );
}

export App;
```

※上記だと、Eslint で以下エラーになる
`/* eslint react-hooks/exhaustive-deps */`

## クラスコンポーネントと関数コンポーネント

- 昔はStateを扱えるのはクラスコンポーネントのみ
- react-hooksの登場で関数コンポーネントでもStateが扱えるように
- 新規なら関数コンポーネントが使われる

## 実践メモ

### input の入力値をstateに即時反映

```jsx
const App = () => {
  const [inputTodoText, setInputTodoText] = useState("");
  
  const onChangeTodoText = (event) => setInputTodoText(event.target.value);

  return (
    <input id="js-add-text" value={inputTodoText} onChange={onChangeTodoText} className="ul-brd ul-pad-6-16" type="text" placeholder="Todo入力" />
  );
}
```

### イベントハンドラに渡すのは関数

onClick={onClickDelete(index)} としてしまうと即時実行される

```jsx
<ul>
  {incompleteTodos.map((todo, index) => {
    <button className="ul-brd" onClick={() => onClickDelete(index)}>削除</button>
  })}
</ul>
```

# default export と export

export推奨

- default export

使う側で名前付けするので、タイポに気付きにくい

```js
import Sample from './components/SampleComp';
```

- export

使用時は分割代入必須かつ定義された名前以外はエラーになる＝タイポ防止

```js
import { SampleComp } from './components/SampleComp';
```
