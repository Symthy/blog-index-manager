# React ステート管理 (TypeScript コード例)

## ステート

ステート：コンポーネントの描画後に更新されるデータ

ステートの管理は上位コンポーネントで行う。下位コンポーネントの操作でステートを更新する場合は、 下位コンポーネントにステート更新用の関数を譲渡、それを実行することで更新を実現する。

```tsx
// 親
type StarRatingProps = {
  totalStars?: number
}

const StarRating: FC<StarRatingProps> = ({ totalStars = 5 }) => {
  const [selectedStars, setSelectedStars] = useState(0);
  return (
    <>
      {[...Array(totalStars)].map((n, i) => (
        <Star
          key={i}
          selected={selectedStars > i}
          onSelect={() => setSelectedStars(i + 1)} // ステート更新用関数譲渡
        />
      ))}
      <p>{selectedStars} of {totalStars} stars </p>
    </>
  )
}

// 子
type StarProps = {
  selected: boolean,
  onSelect: (event: React.MouseEvent<SVGElement, MouseEvent>) => void
}

const Star: VFC<StarProps> = ({ selected = false, onSelect = fn => fn }) => (
  <FaStar color={selected ? "red" : "grey"} onClick={onSelect} />  // 操作されたらステート更新
);
```

### フォーム

以下実現方法。制御されたコンポーネント推奨。

#### useRef (制御されていないコンポーネント)

- DOMノードに直接アクセスする方法
- 特徴：イミュータブルでもなければ宣言的でもない（）
- 用途：React以外のライブラリとデータをやり取りする場合（はDOMに直接アクセスが必要）

```tsx
type AddColorFormProps = {
  onNewColor: (title: string, color: string) => void
}

export const AddColorForm: VFC<AddColorFormProps> = ({
  onNewColor = fn => fn
}) => {
  const textTitle = useRef<HTMLInputElement>(null!);
  const hexColor = useRef<HTMLInputElement>(null!);

  const onSubmit: (event: React.FormEvent<HTMLFormElement>) => void = event => {
    event.preventDefault(); // デフォルト動作(submit:POST送信)抑止
    const title = textTitle.current.value;
    const color = hexColor.current.value;
    onNewColor(title, color);
    textTitle.current.value = "";
    hexColor.current.value = "";
  }

  return (
    <form onSubmit={onSubmit}>
      <input ref={textTitle} type="text" placeholder="input title..." required />
      <input ref={hexColor} type="color" required />
      <button>Add Color</button>
    </form>
  );
}
```

#### useState (制御されたコンポーネント)

- ステート経由でDOMにアクセスする

※制御されたコンポーネント内の描画関数内で重い処理の実行は避ける（パフォーマンス劣化に繋がる）

```tsx
type AddColorFormProps = {
  onNewColor: (title: string, color: string) => void
}

export const AddColorForm: VFC<AddColorFormProps> = ({
  onNewColor = fn => fn
}) => {
  const [title, setTitle] = useState("");
  const [color, setColor] = useState("#000000")

  const onSubmit: (event: React.FormEvent<HTMLFormElement>) => void = event => {
    event.preventDefault(); // デフォルト動作(submit:POST送信)抑止
    onNewColor(title, color);
    setTitle("");
    setColor("#000000");
  }
  const onChangeTitle: (event: React.ChangeEvent<HTMLInputElement>) => void = event => {
    setTitle(event.target.value)
  }
  const onChangeColor: (event: React.ChangeEvent<HTMLInputElement>) => void = event => {
    setColor(event.target.value)
  }

  return (
    <form onSubmit={onSubmit}>
      <input
        value={title} onChange={onChangeTitle}
        type="text" placeholder="input title..." required
      />
      <input
        value={color} onChange={onChangeColor}
        type="color" required
      />
      <button>Add Color</button>
    </form>
  );
}
```

### カスタムフック

制御されたコンポーネントから重複したコード切り出して抽象化できる

上記コードの以下が重複を変更

```
value={title} onChange={event => {setTitle(event.target.value)}
```

```tsx
interface useInputHook {
  (initValue: string): useInputReturns;
}

type useInputReturns = [
  {
    value: string,
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void
  },
  () => void
]

export const useInput: useInputHook = (initValue: string) => {
  const [value, setValue] = useState<string>(initValue);
  return [
    {
      value,
      onChange: event => setValue(event.target.value)
    },
    () => setValue(initValue)
  ]
}

```

```tsx
// コメント： カスタムフック変更前
type AddColorFormProps = {
  onNewColor: (title: string, color: string) => void
}

export const AddColorForm: VFC<AddColorFormProps> = ({
  onNewColor = fn => fn
}) => {
  // const [title, setTitle] = useState("");
  // const [color, setColor] = useState("#000000")
  const [titleProps, resetTitle] = useInput("");
  const [colorProps, resetColor] = useInput("#000000");

  const onSubmit: (event: React.FormEvent<HTMLFormElement>) => void = event => {
    event.preventDefault(); // デフォルト動作(submit:POST送信)抑止
    onNewColor(titleProps.value, colorProps.value);
    // setTitle("");
    // setColor("");
    resetTitle();
    resetColor();
  }
  // const onChangeTitle: (event: React.ChangeEvent<HTMLInputElement>) => void = event => {
  //   setTitle(event.target.value)
  // }
  // const onChangeColor: (event: React.ChangeEvent<HTMLInputElement>) => void = event => {
  //   setColor(event.target.value)
  // }

  return (
    <form onSubmit={onSubmit}>
      <input
        // value={title} onChange={onChangeTitle}
        {...titleProps}
        type="text" placeholder="input title..." required
      />
      <input
        // value={color} onChange={onChangeColor}
        {...colorProps}
        type="color" required
      />
      <button>Add Color</button>
    </form>
  );
}
```

### Reactコンテキスト

- コンテキスト：中継地を経由せずにステートを伝達する方法
- コンテキストプロバイダー：データを渡す方 (親要素側)
- コンテキストコンシューマー：データを読みだす方 (利用コンポーネント側)

メリット

- 導入と管理が容易 デメリット
- 複数Contextの利用時は煩雑化
    - 関数コンポーネントの場合以下のように無駄にネストが深くなる（以下の通り）
- レンダリングコスト：高
    - Contextの値が頻繁に変更される場合、Context.Provider内のコンポーネントの範囲が広い場合、（コンポーネント内の全DOM要素が再レンダリングされ）再レンダリングのコストは非常に大きくなる

```jsx
const Contents = () => {
  return (
    <ThemeContext.Consumer>
      {theme => (
        <UserContext.Consumer>
          {user => (
            <ProfilePage user={user} theme={theme} />
          )}
        </UserContext.Consumer>
      )}
    </ThemeContext.Consumer>
  );
}
```

ref:

- [【React in TypeScript】Contextの使い方とユースケースについて解説](https://marsquai.com/745ca65e-e38b-4a8e-8d59-55421be50f7e/f83dca4c-79db-4adf-b007-697c863b82a5/c20fc9a1-fc36-4ba8-80dd-115b0bbde79f/)

- [Context.Consumer vs useContext() to access values passed by Context.Provider](https://stackoverflow.com/questions/56816374/context-consumer-vs-usecontext-to-access-values-passed-by-context-provider)

※ 複数のプロバイダーがある場合、フックははるかにクリーンになる傾向がある

基本形

```tsx
const colors: ColorData[] = buildInitColors();
export const ColorContext = createContext<ColorData[]>([]);

ReactDOM.render(
  <React.StrictMode>
    <ColorContext.Provider value={colors}>
      <App />
    </ColorContext.Provider>
  </React.StrictMode>,
  document.getElementById('root')
);
```

```tsx
export const ColorList: VFC<ColorListProps> = () => {
  const colors = useContext(ColorContext);
  if (colors.length === 0) {
    return <div>No Colors. (Add Color)</div>
  }
  return (
    <div>
      {colors.map(color => (
        <Color key={color.id} {...color.toObj()} />
      ))}
    </div>
  );
}
```

#### カスタムプロバイダー

基本はコンテキスト＆カスタムフックを使う＝コンテキストへのアクセスがカスタムフック経由のみになり安全

##### コンテキスト＆ステート併用

コンテキストプロバイダーはデータ変更ができないため、データ変更を可能にする手段。

```tsx
type ColorProviderProps = {
  children: React.ReactNode
}

export const ColorContext = createContext(undefined!);

export const ColorProvider = (props: ColorProviderProps) => {
  const [colors, setColors] = useState<ColorData[]>(buildInitColors());
  
  const removeColor = (id: string) => {
    const excludeColor = (id: string) => colors.filter(c => c.id !== id);
    setColors(excludeColor(id));
  }
  const addColor = (title: string, color: string) => {
    const newColors = [...colors, new ColorData(title, color)];
    setColors(newColors);
  }

  return (
    <ColorContext.Provider value={{ colors, addColor, removeColor }}>
      {props.children}
    </ColorContext.Provider>
  );
}
```

※setColors を公開するとどんな操作でも可能になる＝バグが混入する可能性。必要な操作を行う関数のみを(value に設定して)公開する

```tsx
// プロバイダー側：index.tsx
ReactDOM.render(
  <React.StrictMode>
    <ColorProvider>
      <App />
    </ColorProvider>
  </React.StrictMode>,
  document.getElementById('root')
);
```

```tsx
// コンシューマー側
export const ColorList: VFC = () => {
  const { colors } = useContext(ColorContext);
  if (colors.length === 0) {
    return <div>No Colors. (Add Color)</div>
  }
  return (
    <div>
      {colors.map(color => (
        <Color key={color.id} {...color.toObj()} />
      ))}
    </div>
  );
}
```

##### コンテキスト＆カスタムフック

カスタムフックを導入することで、コンテキストをコンシューマーに一切公開することなくデータ共有可能

コンテキストの操作をカスタムフックで隠ぺいする

```tsx
type ColorContextValues = {
  colors: ColorData[],
  addColor: (title: string, color: string) => void,
  updateRateColor: (id: string, rating: number) => void,
  removeColor: (id: string) => void
}

const ColorContext = createContext<ColorContextValues>(undefined!);
export const useColors = () => useContext(ColorContext);

export const ColorProvider = (props: ColorProviderProps) => {
  // ... 同上のため省略
}
```

```tsx
export const ColorList: VFC = () => {
  const { colors } = useColors();
  if (colors.length === 0) {
    return <div>No Colors. (Add Color)</div>
  }
  return (
    <div>
      {colors.map(color => (
        <Color key={color.id} colorData={color} />
      ))}
    </div>
  );
}
```

ref:

- [TypeScript & Context APIのdefaultValueの書き方（use***がうまく機能しない時）](https://zenn.dev/hiro4hiro4/articles/a19d1f5c9b6eab)

ステートが更新される＝ColorProviderコンポーネント全体が再描画 -> コンポーネントツリー全体にデータ更新が反映

## まとめ

ロジックをフックに分離する -> 関心の分離 = UI と ロジックを別々に開発/テスト＆デプロイ可能

