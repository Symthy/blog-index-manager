# Golang Generics

## golang 1.18beta1導入

```go
go install golang.org/dl/go1.18beta1@latest
go1.18beta1 download
go1.18beta1 version
```

ベータ版を使用する場合は、go1.18beta1 コマンドを使用する

## そもそものGenerics

Genericsが効果を発揮する場面は以下

> 「高度に抽象化された振る舞い」が定義できる場合
> - GUI開発におけるViewの振る舞い
>
> 「羅列されたデータの中から1つ選択する」「テーブルとして表示する」の様な「振る舞い」を抽象化。扱うデータを型パラメータで指定、安全に取り扱う
> - データコンテナとしての振る舞い（Collection/Nullable/非同期）
>
> 振舞いを抽出して定義しつつ、ジェネリクスとして型パラメータを与える

> Goの場合は、データコンテナだけの話。以下のように対応しているらしい
>- Collection -> for文とif文
>- Nullable -> if文
>- 非同期 -> goroutineとchannel

ref:

- [Go言語でジェネリクスない理由の考察](https://nametake.github.io/posts/2019/12/31/go-no-generics/)
- [【Golang】ジェネリクスのメリデメを比較してみる【1.18】](https://hikyaru-suzuki.hatenablog.jp/entry/2021/12/20/180000)

---

Goに導入される Generics は Collection の部分を補うためと思われる。

現状、振舞いの抽象化の部分は各々コード生成で補っている。

コード生成では、生成した分コードが増える、メンテコストもかかる。

その点をジェネリクスを入れることで解消しようという感じと思われる。

ジェネリクスを使うとコンパイル時間は多少増えるが、その分コード生成分が減らせるので、

## GolangのGenericsは他言語のGenericsとは違う

クラスメソッドには使う事はできず、関数のみにしか使えない

> 多相が欲しいというニーズに Java は Generics で答えた。golang は Duck Type と type assertion で答えた

クラスの引数/戻り値に幅を持たせたいなら、Golangは以下のうようにできるようにしているから。

```go
type Numeric interface {
    Add(Numeric) Numeric
}

func sum(list []Numeric) Numeric {
    ret := list[0]
    for i := 1; i < len(list); i++ {
        ret = ret.Add(list[i])
    }
    return ret
}

type Int int

func (i Int) Add(n Numeric) Numeric {
    switch t := n.(type) {
    case Int:
        return i + t
    case Float:
        return i + Int(t)
    }
    panic("unknown type")
}

type Float float64

func (f Float) Add(n Numeric) Numeric {
    switch t := n.(type) {
    case Float:
        return f + t
    case Int:
        return f + Float(t)
    }
    panic("unknown type")
}

func main() {
    list := []Numeric {
        Float(5),
        Int(2),
        Int(3),
        Float(1),
        Int(4),
    }
    fmt.Println(sum(list))
}
```

ref:

- [golang と Generics と私](https://mattn.kaoriya.net/software/lang/go/20170309201506.htm)

## サンプル色々

- `func F[T any](v T){...}` で任意の型指定可
- どの型でも取れる値は `any` を使用可

foreach：

```go

type A struct {
    val string
}
func(a A) Print() {
    fmt.Printf("value: %s\n", a.val)
}

func ForEach[t1 any](li []t1, fn func(t1)) {
    for _, n := range li {
        fn(n)
    }
}

main() {
    // foreach
    ForEach(AList, func(a A) {a.Print()})
}
```

```go
type A struct {
    val string
}
func(a A) Print() {
    fmt.Printf("value: %s\n", a.val)
}

// 関数を引数に指定する際も使用可
func Map[t1, t2 any](li []t1, fn func(t1) t2) []t2 {
    dst := make([]t2, len(li), len(li))
    for i, n := range li {
        dst[i] = fn(n)
    }
    return dst

}

func main() {
    intList := []int{0, 1, 2, 3, 4, 5}
    strList := []string{"a", "hoge", "huga"}
    AList := []A{A{"a"}, A{"b"}}

    // map
    intListMap := Map(intList, func(i int) int {return i + 1 })
    strListMap := Map(strList, func(s string) string {return s + "foo"})
    AListMap := Map(AList, func(a A) A {return A{a.val + "A"}})
}
```

- 型パラメータリストが定義できる `type A[T any] []T`

Vector:

```go
type Vector[T any] []T

func (v *Vector[T]) Push(x T) {
    *v = append(*v, x)
}
```  

- 型制限が可能 `func F[T Constraint](t T){...}`

Map

```go
type Addable[t any] interface {
    Add(v1 t, v2 t) t
}
// implements Addable
type A struct {
    val string
}
func(a A) Add(v1 A, v2 A) A {
    return A{val: v1.val + v2.val}
}

func Sum[t Addable[t]](li []t) t {
    var sum t
    for _, v := range li {
        sum = v.Add(sum, v)
    }
    return sum
}

func main() {
    AList := []A{A{"a"}, A{"b"}}
    sum := Sum(AList)
    fmt.Printf("sum: %v, type: %T\n", sum, sum)
}
```

LinkedList:

```go
package list

type listNode[T any] struct {
   value T
   prev *listNode[T]
   next *listNode[T]
}

type LinkedList[T any] struct {
   head *listNode[T]
   last *listNode[T]
}

func NewList[T any]() *List[T] {
   return &List[T]{}
}

// Constraintなし
func (l *LinkedList[T]) AddLast(item T) {
   node := &listNode[T]{value: item}
   if l.head == nil {
      l.head = node
      l.last = node
      return
   }
   l.last.next = node
   node.prev = l.last
   l.last = node
}

func (l *LinkedList[T]) AddFirst(item T) { … }
func (l *LinkedList[T]) Print() { … }

func (l *LinkedList[T]) Filter(pred func(T) bool) *List[T] {
   dest := NewList[T]()
   for node := l.head; node != nil; node = node.next {
      if pred(node.value) {
         dest.AddLast(node.value)
      }
   }
   return dest
}

// メソッドに型パラーメータは指定不可
// func (l *LinkedList[T]) Map[U any](fn func(T) U) *LinkedList[U] { … }

func Map[T, U any](l *List[T], fn func(T) U) *List[U] {
   dest := NewList[U]()
   for node := l.head; node != nil; node = node.next {
      value := fn(node.value)
      dest.AddLast(value)
   }
   return dest
}

// 型を明示指定 Constraint
type Ordered interface {
   type int, int8, int16, int32, int64,
     uint, uint8, uint16, uint32, uint64, uintptr,
     float32, float64,
     string
}

func SumOrdered[T Ordered](l *LinkedList[T]) T {
   var sum T
   for node := l.head; node != nil; node = node.next {
      sum += node.value
   }
   return sum
}

// 挙動指定：Ordered にない型を指定


func main() {
  intList := list.NewList[int]()
  n := node[int]{value: 1}
  
  intList.AddFirst(66)
  intList.AddFirst(65)
  intList.AddLast(67)
  intList.Print()    // [65, 66, 67]
  
  filterIntList := intList.Filter(func(i int) bool {
    return i % 2 == 0
  })  // [66]
  
  intToString := list.Map(intList, func(i int) string {
    return string(rune(i))
  })  // [A, B, C]
  
  list.SumOrdered(intList)  // 198
}

// ------
// 挙動を指定： Ordered にない型に対応

type Point struct {
   X, Y int
}

// こういうケースはOrderedインターフェイスに型追加で対応できないので、インターフェース追加で対応要
type Summable[T any] interface {
   Add(t T) T
}

func Sum[T Summable[T]](l *LinkedList[T]) T {
   var sum T
   for node := l.head; node != nil; node = node.next {
      sum = sum.Add(node.value)
   }
   return sum
}

// implements Summable
func (p Point) Add(q Point) Point {
   return Point{
      X: p.X + q.X,
      Y: p.Y + q.Y,
   }
}

func main2() {
  pointList := list.NewList(Point)()
  pointList.AddLast(Point{1,1})
  pointList.AddLast(Point{2,2})
  pointList.AddLast(Point{3,3})
  pointList.Print() // [{1 1}, {2 2}, {3 3}]
  // list.SumOrdered(pointList) // コンパイルエラー

  list.Sum(pointList)
}
```

> 標準ライブラリにOrderedのようなConstraintsで基本型がだいたいカバーされる

ref:

- [goのジェネリクスで遊んでみた](https://qiita.com/gal1996/items/9a0da520c06fe55fdd36)

- [連結リストの実装でGo言語のジェネリクスのドラフトを触ってみる](https://medium.com/eureka-engineering/golang-generics-design-draft-linked-list-4d1174e2355d)

## 実践メモ

Gorm使用の基本的な処理を提供するリポジトリクラス

- ISchema: Gorm用に用意しているデータモデル用インターフェース
- IDomain: ドメイン用(ジェネリクスの型制限用)

都合により一部関数を外から与える。以下のようにすることで利用側も受け取る型が一意に定まる。

```go
package infrastructure

type ISchema[T IDomain] interface {
    ConvertToDomain() *T
}

// 型制限をかけるためだけのインターフェース ※他に良いものがあればそれで
type IDomain interface {
    Id() uint
}
```

```go
package database

type BaseRepository[TS infrastructure.ISchema[TD], TD infrastructure.IDomain] struct {
    db           *gorm.DB
    emptySchemaBuilder func() TS
    // Domainに実装すると双方向依存。感覚的にDomainに実装するのも違うため分離している
    toSchemaConverter    func(domain TD) TS
}

func (rep BaseRepository[TS, TD]) FindById(id uint) (*TD, error) {
    var schema = rep.emptySchemaBuilder()
    tx := rep.db.First(&schema, id)
    if tx.Error != nil {
        return nil, tx.Error
    }
    return schema.ConvertToDomain(), tx.Error
}

func (rep BaseRepository[TS, TD]) Create(model TD) (*TD, error) {
    schema := rep.schemaConverter(model)
    db := rep.dbClient.Db()
    tx := db.Create(&schema)
    if tx.Error != nil {
        return nil, tx.Error
    }
    return schema.ConvertToDomain(), nil
}

func (rep BaseRepository[TS, TD]) Update(model TD) (*TD, error) {
    _, err := rep.FindById(model.Id())
    if err != nil {
        return nil, err
    }
    schema := rep.toSchemaConverter(model)
    updated := rep.emptySchemaBuilder()
    tx := rep.db.Model(&updated).Updates(schema)
    if tx.Error != nil {
        return nil, tx.Error
    }
    return updated.ConvertToDomain(), nil
}

func (rep BaseRepository[TS, TD]) Delete(id uint) (*TD, error) {
    db := rep.dbClient.Db()
    schema := rep.emptySchemaBuilder()
    tx := db.Delete(&schema, id)
    if tx.Error != nil {
        return nil, tx.Error
    }
    return schema.ConvertToDomain(), nil
}

```

## Links

ref:

- [Go言語でジェネリクスない理由の考察](https://nametake.github.io/posts/2019/12/31/go-no-generics/)

- [【Golang】ジェネリクスのメリデメを比較してみる【1.18】](https://hikyaru-suzuki.hatenablog.jp/entry/2021/12/20/180000)

- [golang と Generics と私](https://mattn.kaoriya.net/software/lang/go/20170309201506.htm)

- [goのジェネリクスで遊んでみた](https://qiita.com/gal1996/items/9a0da520c06fe55fdd36)

- [連結リストの実装でGo言語のジェネリクスのドラフトを触ってみる](https://medium.com/eureka-engineering/golang-generics-design-draft-linked-list-4d1174e2355d)

Other:

- [go generics example (サンプル集)](https://github.com/mattn/go-generics-example)

- [GoのGenerics関連プロポーザル最新状況まとめと簡単な解説](https://zenn.dev/syumai/articles/c42hdg1e0085btnen5hg)

- [Goのジェネリクス先取り入門１ (2020/12)](https://medium.com/voicy-engineering/go%E3%81%AE%E3%82%B8%E3%82%A7%E3%83%8D%E3%83%AA%E3%82%AF%E3%82%B9%E5%85%88%E5%8F%96%E3%82%8A%E5%85%A5%E9%96%80%EF%BC%91-8fa9aa087c78)

- [Goのジェネリクス先取り入門２ (2020/12)](https://medium.com/voicy-engineering/go%E3%81%AE%E3%82%B8%E3%82%A7%E3%83%8D%E3%83%AA%E3%82%AF%E3%82%B9%E5%85%88%E5%8F%96%E3%82%8A%E5%85%A5%E9%96%80%EF%BC%92-3cb9b322f8a9)

---
公式

- [Tutorial: Getting started with generics](https://go.dev/doc/tutorial/generics)
- [Why Generics?](https://go.dev/blog/why-generics)
