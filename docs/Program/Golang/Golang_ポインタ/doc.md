# Golang ポインタ

## 注意事項

- 自明：文字列、インターフェイス、チャネル、マップ、スライス等はそもそもポインタ

これらにポインタを使うとすれば、やむなく値無し(nil) の表現が必要な時だけ

例えば jsonデータ。存在しえないフィールドはnil代入を許容する

```go
type JsonData struct {
  id string `json:"id"`
  nickname *string `json:"nickname,omitempty"`
}
```

ポインタでむやみに値無しを表現するのは良くないのではないかと。
そうした場合、ポインタの表現する意味が本来のポインタの意味と値無しの2つの役割を持ってしまう。値オブジェクトにしてそのオブジェクトで値無しを表現する用にした方が良いのではないか？

- (スライスではなく) 配列の場合は値渡し

```go
var array = [3]string{"japanese", "math", "english"}
var array2 = array  // 値渡し

var array3 = array[:]  // 参照渡し
```

- ポインタレシーバーでないと更新できない

setNameの中にあるpersonは、それを呼び出したインスタンスのコピー

そもそも struct がポインタ型でない場合、プロパティにアクセスするメソッドでも、インスタンスのコピーをわざわざ作り出している

```go
type Person struct {
    name string
}
func (person Person) sayName() {
    fmt.Println(person.name)
}
func (person Person) setName(name string) {
    person.name = name
}

var hoge = Person{"Hoge"}
hoge.sayName() // Hoge  // インスタンスのコピー
hoge.setName("Fuge")  // インスタンスのコピーに対してsetするため反映されず
hoge.sayName() // Hoge
```

- interface 実装 struct のポインタ

以下はエラー (`Person does not implement Greeter (Greet method has pointer receiver)`) になる。struct
にポインタレシーバーを使用する時は、生成する際もポインタの使用必須（ポインタはポインタで合わせろと）

```go
type Greeter interface {
    Greet()
}
type Person struct {
    name string
}
func (p *Person) Greet() {
    println("Hi! I'm ", p.name)
}
func NewGreeter(name string) Greeter {
    return Person{name}  // return &Person{name} である必要がある
}
func main() {
    p := NewGreeter("SYM")
    p.Greet() 
}
```

- 再帰的な処理は深さに注意

深ければ深いほど、性能劣化に繋がる

> Goでは再帰の深さが極端に処理性能が落ちる要因になります。 深さの数だけスタックを浪費する実装になっていますのでGoに慣れた人は自然と深い再帰処理はループ処理に書き換えます。（フォルダツリーのような有限な深さであることがわかっているような処理は再帰で書いても問題はありません）

[Goの良さをまとめてみた](https://zenn.dev/nobonobo/articles/e651c66a15aaed657d6e)

- 使いすぎると性能劣化に繋がる

ポインタはアドレスを渡すだけのため効率的だが、使いすぎるとガベージコレクションに負荷がかかってしまい、多くのCPU時間を消費するようになる可能性がある

恐らくポインタでメモリを占有し続ける状態を作るとGC時に毎回見に行きコストがかかると思われる（string, map ,slice 等での定数宣言も同じことが言えるのでは？）

ref:[Go のGCのオーバーヘッドが高くなるケースと、その回避策](https://qiita.com/imoty/items/c1017099e63cd4630946)

## ポインタの使い所

前提： レシーバ = メソッドの `(s Square)` の部分

- ポインタを使うべきでない時
    - レシーバが map、func、チャネルの場合
    - レシーバがスライスで、メソッドがスライスを作りなおさない場合
- ポインタを使う時
    - メソッドで値を変更する必要がある場合
    - レシーバが sync.Mutex か、似たような同期するフィールドを持つ構造体の場合、コピーを避けたいデータを扱う場合
    - レシーバが大きな構造体や配列の場合
    - 大きな構造体をスライスに持たせる場合

## ref

[Golangのポインタで詰まったので備忘録](https://qiita.com/2san/items/0faa3939d55f8594393a)

[Go言語でinterfaceをimpleしてるつもりが「does not implement (method has pointer receiver)」って叱られる【golang】【pointer】【ダックタイピング】](https://otiai10.hatenablog.com/entry/2014/05/27/223556)

[go Code Review Comments 日本語翻訳](https://gist.github.com/knsh14/0507b98c6b62959011ba9e4c310cd15d#receiver-type)

[Goにおけるポインタの使いどころ](https://zenn.dev/uji/articles/f6ab9a06320294146733)

[【Go言語】構造体におけるポインタメソッドの使いどころ](https://nishinatoshiharu.com/go-structure-pointermethod)
