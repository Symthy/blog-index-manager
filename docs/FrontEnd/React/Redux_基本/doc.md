# Redux 基本

ひとまず、storybook のチュートリアルに載っていた範囲＋ α のみ

## Redux とは

Flux ベースの state（状態）を容易に管理をするためのフレームワーク

refs:

- https://qiita.com/knhr__/items/5fec7571dab80e2dcd92
- https://future-architect.github.io/articles/20200429/

## Redux ストア

```typescript
import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {},
});
```

```typescript
import { store } from "./app/store";
import { Provider } from "react-redux";

ReactDOM.render(
  <Provider store={store}>
    <App />
  </Provider>,
  document.getElementById("root")
);
```

configureStore を使用する場合、追加の入力は必要ないが、必要に応じて、RootState 型と Dispatch 型を抽出する必要がある。

ストア自体からこれらの型を推測することは、state slices を追加したりミドルウェア設定を変更したりすると、正しく更新されることを意味する。

アプリケーションで使用する際は、以下フックの作成推奨

- useDispatch フック

useSelector の場合、毎回`(state:RootState)`と入力する必要はない。

- useSelector フック

useDispatch の場合、既定の Dispatch 型は thunks を認識しません。正しく thunks を dispatch するには、thunk middleware types を含むストアから特定のカスタマイズされた AppDispatch 型を使用し、それを useDispatch と共に使用する必要がある。事前に型指定された useDispatch フックを追加すると、必要な場所に AppDispatch をインポートすることを忘れずに済む。

- createSlice

初期状態、reducer 関数のオブジェクト、および 「スライス名」 を受け取り、reducer と状態に対応するアクションクリエーターとアクションタイプを自動的に生成する関数。

```typescript
// app/sotre.ts
import { configureStore } from "@reduxjs/toolkit";
import { useDispatch, useSelector } from "react-redux";
import type { TypedUseSelectorHook } from "react-redux";
import type { RootState, AppDispatch } from "./store";

const TasksSlice = createSlice({
  name: "taskbox",
  initialState: TaskBoxData,
  reducers: {
    updateTaskState: (state, action) => {
      const { id, newTaskState } = action.payload;
      const task = state.tasks.findIndex((task) => task.id === id);
      if (task >= 0) {
        state.tasks[task].state = newTaskState;
      }
    },
  },
});

// Redux ストア
export const store = configureStore({
  reducer: {
    taskbox: TasksSlice.reducer,
  },
});

// ストア自体から`RootState`型と`AppDispatch`型を推測する
export type RootState = ReturnType<typeof store.getState>;
// 推定型: {posts: PostsState, comments: CommentsState, users: UsersState}
export type AppDispatch = typeof store.dispatch;

// 単純な`useDispatch`と`useSelector`の代わりにアプリ全体で使用する
export const useAppDispatch: () => AppDispatch = useDispatch;
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;
```

```typescript
// 発行
const pinTask = (value) => {
  dispatch(updateTaskState({ id: value, newTaskState: "TASK_PINNED" }));
};
```

- createAsyncThunk

Redux アクションタイプ文字列と promise を返すコールバック関数を受け取る関数。渡されたアクションタイププレフィックスに基づいて promise ライフサイクルアクションタイプを生成し、promise コールバックを実行し、返された promise に基づいてライフサイクルアクションをディスパッチする thunk アクションクリエーターを返す。

これにより、非同期要求ライフサイクルを処理するための標準的な推奨アプローチが抽象化されます。

```typescript
import { userAPI } from "./userAPI";

const fetchUserById = createAsyncThunk(
  "users/fetchByIdStatus",
  async (userId: number, thunkAPI) => {
    const response = await userAPI.fetchById(userId);
    return response.data;
  }
);

const usersSlice = createSlice({
  name: "users",
  initialState,
  reducers: {
    // ry
  },
  extraReducers: (builder) => {
    // ここに追加のアクションタイプのレジューサを追加し、必要に応じてロード状態を処理します
    builder.addCase(fetchUserById.fulfilled, (state, action) => {
      state.entities.push(action.payload);
    });
  },
});

// Later, dispatch the thunk as needed in the app
dispatch(fetchUserById(123));
```
