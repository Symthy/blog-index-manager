# React Hooks

## Hooks とは

クラスコンポーネントを使わずとも、ファンクションコンポーネントで

- 状態管理やコールバックが使える
- かつ簡易に実装できる

### useState: 状態保持

- 状態１つ、変更前の値参照

```App.js
import React, { useState } from 'react';
import './App.css';

const App = () => {
  const [count, setCount] = useState(0)
  const increment = () => setCount(count+1)
  const decrement = () => setCount(count-1)
  const divide3 = () => setCount(previous => {
    return previous % 3 === 0 ? previous / 3 : previous
  })
  const reset = () => setCount(0)
  return (
    <>
      <div>count: {count}</div>
      <button onClick={increment}>+1</button>
      <button onClick={decrement}>-1</button>
      <button onClick={reset}>Reset</button>
      <button onClick={divide3}>divide3</button>
    </>
  );
}

export default App;
```

- 複数状態保持、テキストボックス入力値即時反映、defaultProps

```App.js
import React, { useState } from 'react';
import './App.css';

const App = props => {
  const [name, setName] = useState(props.name)
  const [price, setPrice] = useState(props.price)
  const reset = () => {
    setPrice(props.price)
    setName(props.name)
  }
  return (
    <>
      <p>{name}: {price}円</p>
      <button onClick={() => setPrice(price + 10)}>+10円</button>
      <button onClick={() => setPrice(price - 10)}>-10円</button>
      <button onClick={reset}>Reset</button>
      <input value={name} onChange={e => setName(e.target.value)}></input>
    </>
  );
}

App.defaultProps = {
  name: "",
  price: 100
}

export default App;
```

## refs

[React Hook Formを1年以上運用してきたちょっと良く使うためのTips in ログラス（と現状の課題）](https://zenn.dev/yuitosato/articles/292f13816993ef)