# React Drag & Drop メモ

主要ライブラリは３つ

- [React DnD](https://github.com/react-dnd/react-dnd)
- [react-beautiful-dnd](https://github.com/atlassian/react-beautiful-dnd)
- [React-Draggable](https://github.com/react-grid-layout/react-draggable)

※2022/5 末時：React18 で実現したければ React DnD を使うか自前で実装するかがよさそう

## 各ライブラリ所感

React DnD

- drag & drop 中の見た目：半透明になるのでよい
- シンプルなものであればこれで十分
- HTML5 の API setDragImage を利用して作られているためパフォーマンス面もよい
- 多少凝ったものを作ろうと思うと大変そう（例えばかんばんボードの複数のタスクが入っている枠の方を Drag できるようにする等。そもそもできるかまで調べられていない）

react-beautiful-dnd

- drag & drop の見た目：リッチ
- 2022/5 末、React18 には対応していない（React18 で動かしたければ React.StrictMode を消せば動くらしい？そんな状態では個人なら自己責任で済むが製品等には使えない）。対応は水面下？で進められてはいそうだが、まだ先になりそう (使いたければ React17 を使うしかない)
- 多少凝ったものでも容易に作れそう（かんばんボードの複数のタスクが入っている枠の方を Drag できるようにするのは容易にできる）

React-Draggable

- 最低限だけの可能性があるので、必要なものは自分で実装をする必要がありそうで大変そう（以下できるかまでは未確認）
  - サンプル見た限りは Drag & Drop しかできないため、上記２つだと自動でやってくれる位置調整等も必要なら地震で実装する必要があるかもしれない
  - 見た目は頑張ってカスタマイズする必要があるかもしれない

その他：自前で実装（OSS に依存したくなく腕があるなら）

- (参考)簡単な例：https://github.com/trananhtuat/react-draggable-list (2020 年、ちょっと古い)

## 参考(コードリーディング)

以下のコードを読んでみた

目的：React DnD 使用した場合の、よくあるかんばんボードの Todo、Done といった Group 間の Card 移動をどうやって実現してるのか確認したかったため

- [React DnD でかんばんボードを作ってみる](https://zenn.dev/mtblue81/articles/98ae1a40266317) ※ソースもデモも記事にリンクがある

※Group、Card という表現は適切ではないかもしれないが上記のコードと用語を合わせるために揃える

※以降、ディスる意図等は一切なく単純に思ったことを書き留めるだけのためご容赦を

- Group 間で Card は跨いで移動する = アプリ全体で参照するから ベースとなるコンポーネント：App.tsx で管理している → 分かる
- Card の一覧を 1 配列で管理、Group と属する Card を別オブジェクトで管理
  - Card 一覧の配列内は、Group 順に並べていて、Group コンポーネントに Card 一覧の配列内の各 Group の先頭インデックス(firstIndex) を渡すことで、Card 一覧の配列での管理を実現している -> これが分かりにくかった
    - map（key: Group 名、 value: Card の配列）で管理した方がいいのではないか？
    - もしくは、Group の情報を持つデータクラス？を用意した方がよいのではないか？（必要ならそれらを管理するクラスも）
    - firstIndex より Group 名等 各 Group を識別する一意な値を渡して制御するようにした方が分かりやすそう
    - ※リファクタして試せ
- 以下のコードの「forward」「backward」のコメント制御が最初分からなった（開発者ツールでデバッグしてやっと分かったレベル）
  - 以下の部分は Group 間の Card 移動を担当させている (だからこその `dragItem.group === groupType`。変数名から変数に格納されるデータを誤解して、コードだけ見てもこの役割が掴かみきれなかった)
    - targetIndex： targetGroupFirstIndex
    - items: itemsInGroup とかの方がまだ伝わる？
  - Draggable.tsx は Group 内の Card 移動にまかせている
  - Group 間移動は、Group.tsx で移動先の Group の末尾に放り込むだけ（目には見えないが）。あとは Draggable.tsx で Drag 時の位置を変えてる

useRef を使っているコンポーネントを重ねての制御ができている（Group と Draggable）ので、Group 自体を drag&drop できるようにすることはできるかもしれない（ただし少々大変そう）

```typescript
// Group.tsx
const [, ref] = useDrop({
  accept: ItemTypes,
  hover(dragItem: ItemWithIndex) {
    const dragIndex = dragItem.index;
    if (dragItem.group === groupType) return;
    const targetIndex =
      dragIndex < firstIndex
        ? // forward
          firstIndex + items.length - 1
        : // backward
          firstIndex + items.length;
    onMove(dragIndex, targetIndex, groupType);
    dragItem.index = targetIndex;
    dragItem.group = groupType;
  },
});

// data.ts
export type Item = {
  id: number;
  type: ItemType;
  group: GroupType;
  contents: Contents;
};
export type ItemWithIndex = Item & {
  index: number;
};
```

## refs

- [React drag and drop ライブラリ選定](https://zenn.dev/yuto_nakamoto/scraps/b9793f51c65bec)
- [React DnD を使ったので知見をまとめた](https://tech.hey.jp/entry/2021/03/09/131638)
- [React DnD でかんばんボードを作ってみる](https://zenn.dev/mtblue81/articles/98ae1a40266317)

ついでに面白そうなの見つけた(あまり更新されてないけど)

- [React Sortable Tree](https://github.com/frontend-collective/react-sortable-tree)
