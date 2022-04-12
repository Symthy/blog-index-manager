# React 副作用/メモ化/レデューサー (TypeScriptコード例付)

## 副作用/メモ化/レデューサー

副作用：描画の一部ではない処理。UI構築に関する以外の処理

- useEffect：Paint処理手前
    - コンポーネント描画と描画結果依存処理(ロジック)との関心分離？
- useLayoutEffect：Paint処理後
    - コンポーネント描画前処理（コンポーネントサイズ決定等）

レデューサー：同じ引数の場合、必ず同じ戻り値を返さなければならない

- useReducer：ステート更新ロジックの抽出、複雑なステート管理

メモ化

- useMemo：パフォーマンス改善のための計算結果をキャッシュ、値のメモ化値
    - 依存配列の値が変わった場合のみ渡された関数実行。
- useCallback：パフォーマンス改善、関数のメモ化
- memo: 関数コンポーネントのメモ化（コンポーネントのパフォーマンス改善）

※なんでもかんでもメモ化すればいい訳ではない。メモ化にもコストはかかる

Reactは初めからパフォーマンスを年頭に置いて設計されている。

- パフォーマンスチューニングを実施するにはゴール設定が重要
- 静的な方法ではなく、実際に実行し、描画がもたついたり止まったりする箇所が何に時間を要しているかを確認して対処

**再レンダリング戦略**

1. stateを持つ位置を工夫し、変更される範囲を限定する
2. memo等でレンダリングをおさえる

ref:

- [なんとなくでやらないReact.memo戦略](https://zenn.dev/bom_shibuya/articles/b07da034fc5686)
- [Before You memo()](https://overreacted.io/before-you-memo/)
- [React.memo を濫用していませんか？ 更新頻度で見直す Provider 設計](https://zenn.dev/takepepe/articles/react-context-rerender)
    - いずれも更新頻度が高いとマイクロHookパターンが最適。末端コンポーネントでmemo化が不要になる

### useEffect

```tsx
export const CheckBox: VFC = () => {
  const [checked, setChecked] = useState<boolean>(false);

  useEffect(() => {
    alert(`checked: ${checked.toString()}`);
  });

  // alert(`checked: ${checked.toString()}`); // OK押下されるまで↓の処理が実行されない

  return (
    <>
      <input
        type="checkbox" checked={checked}
        onChange={() => setChecked(checked => !checked)}
      />
      {checked ? "checked" : "non checked"}
    </>
  );
}
```

第二引数の配列：依存配列

#### 依存配列

副作用が実行される条件を指定（設定した値が更新された時に実行されるようになる）

- 依存配列：指定なし -> コンポーネント描画時は常時実行

```jsx
const [value, setValue] = useState("");

useEffect(() => {
  console.log(`typing ${value}`)
});
```

- 依存配列：空配列 -> コンポーネント初回描画のみ実行

```jsx
const [value, setValue] = useState("");

useEffect(() => {
  console.log(`typing ${value}`)
}, []);
```

- 依存配列：値有り -> 値更新時のみ実行（※）

```jsx
const [value, setValue] = useState("");

useEffect(() => {
  console.log(`typing ${value}`)
}, [value]);
```

（※）同一性チェックで値が同じか判定している

- プリミティブ値(string, number, boolean)：値が同じかどうかで評価
- 配列、オブジェクト、関数：参照同一性で評価するため常にfalseに

```js
const a = "test";
const b = "test";
console.log(a === b); // true

const arr1 = [1,2,3];
const arr2 = [1,2,3];
console.log(arr1 === arr2); // false
```

依存配列に、配列、オブジェクト、関数、を指定した場合は、コンポーネント再描画時に（これらのインスタンスは再生成され、非同一と判定されるため）useEffectが常時実行されてしまう。

それを防ぎ、かつ中身が変わった時のみ実行できる手段

- useMemo：配列、オブジェクト
- useCallback：関数

#### useMemo/useCallback

ref: [React.memo / useCallback / useMemo の使い方、使い所を理解してパフォーマンス最適化をする](https://qiita.com/soarflat/items/b9d3d17b8ab1f5dbfed2)

### useLayoutEffect

例：

- コンポーネントサイズの計算

```tsx
export const useWindowSize = () => {
  const [width, setWidth] = useState<number>();
  const [height, setHeight] = useState<number>();

  const resize = () => {
    setWidth(window.innerWidth);
    setHeight(window.innerHeight);
  }

  useLayoutEffect(() => {
    window.addEventListener("resize", resize);
    return () => window.removeEventListener("resize", resize);
  }, []);

  return [width, height];
}
```

- マウス座標の追跡

```tsx
export const useMousePosition = () => {
  const [x, setX] = useState<number>(0);
  const [y, setY] = useState<number>(0);

  type SetPositionInput = { x: number, y: number };
  const setPosition = ({ x, y }: SetPositionInput) => {
    setX(x);
    setY(y);
  }

  useLayoutEffect(() => {
    window.addEventListener("mousemove", setPosition)
    return () => window.removeEventListener("mousemove", setPosition);
  }, []);

  return [x, y]
}
```

### useReducer

ステート更新のロジックを抽象化可能

```tsx
export const CheckBox: VFC = () => {
  const [checked, toggle] = useReducer(checked => !checked, false);

  return (
    <>
      <input
        type="checkbox" checked={checked}
        onChange={toggle}
      />
      {checked ? "checked" : "non checked"}
    </>
  );
}
```

- 複数値を包含するステート値の部分更新

```tsx
const firstUser = {
  id: "",
  firstName: "SYM",
  lastName: "THY",
  city: "Tokyo",
  state: "Japan",
  admin: false,
}

type UserData = typeof firstUser;

export const User: VFC = () => {
  const [user, setUser] = useReducer((user: UserData, newDetails: Partial<UserData>) =>
    ({ ...user, ...newDetails }), firstUser);

  // Reducer を使わずにやろうとすると以下にする必要がでてくる
  //const onClick = () => setUser({ ...user, admin: true })
  const onClick = () => setUser({ admin: true });

  return (
    <div>
      <h1>{user.firstName}{user.lastName} - {user.admin ? "Admin" : "User"}</h1>
      <p>Location: {user.city}, {user.state}</p>
      <button onClick={onClick}>Make Admin</button>
    </div>
  );
}
```

### memo関数

メモ化したコンポーネントは、プロパティが変更されない限り再描画されない

- プロパティが関数の場合は（依存配列と同じ理屈で）毎回描画されてしまう。
- 第２引数に条件指定することで回避可能

第２引数がfalseの時のみ実行される

```js
const OnceRenderCat = memo(Cat, () => true); // 初回のみ描画
const AlwaysRenderCat = memo(Cat, () => false); // 毎回描画
```

```tsx
export const App = () => {
  const [cats, setCats] = useReducer(
    (cats: string[], newCats: string[]) => [...cats, ...newCats], hadCats
  );

  const onAddCat = (name: string) => {
    setCats(name ? [name] : []);
  };

  return (
    <>
      {cats.map((name, i) => {
        <PureCat key={i} name={name} meow={() => console.log(`${name} meowed`)} />
      })}
      <AddCatForm addCat={onAddCat} />
    </>
  );
}
```

```tsx
type CatProps = {
  name: string,
  meow: (name: string) => void
}

const Cat: VFC<CatProps> = ({ name, meow = fn => fn }) => {
  console.log(`rendering cat: ${name}`);
  return <p onClick={() => meow(name)}>cat: {name}</p>
};

export const PureCat = memo(
  Cat,
  (prevProps, nextProps) => prevProps.name === nextProps.name
);
```

```tsx
type AddCatFormProps = {
  addCat: (name: string) => void
}

export const AddCatForm: VFC<AddCatFormProps> = ({ addCat }) => {
  const [name, setName] = useState<string>("");

  const onSubmit: (event: React.FormEvent<HTMLFormElement>) => void = event => {
    event.preventDefault();
    addCat(name);
    setName("");
  }

  const onChange: (event: React.ChangeEvent<HTMLInputElement>) => void = event => {
    setName(event.target.value);
  }

  return (
    <form>
      <input
        value={name} onChange={onChange}
        type="text" placeholder="input name..." required
      />
      <button>Add Cat</button>
    </form>
  )
}
```
