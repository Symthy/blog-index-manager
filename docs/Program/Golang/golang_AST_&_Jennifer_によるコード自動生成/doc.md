# golang AST & Jennifer によるコード自動生成

モチベーション：以下と似ている

ref: [entity からコード自動生成した話](https://tech.mfkessai.co.jp/2019/09/ebgen/)

ベースとなるソースファイルから AST 取得し必要情報抽出 ⇒ jennifer にてソース自動生成

- その他自動生成参考になりそうなもの
  - [コードの自動生成は高いレバレッジを達成できる手段 Go におけるコマンド、モデル、テンプレートを組み合わせた実装](https://logmi.jp/tech/articles/326270#s4)
  - [go 言語の AST の全てのコメントは、\*ast.File 以下の子孫ノードから集める事はできないという話](https://pod.hatenablog.com/entry/2018/03/06/104109)
- ※template を使用する場合は、以下が参考になる
  - [Go でひたすら運用を楽にするためのコード生成をする](https://medium.com/eureka-engineering/advent-calendar-2020-vim-go-generate-1a2a11cf0cef)
  - https://github.com/kaneshin/go-generate-sample

template を使わない理由

- template と埋め込むコードの２つを管理するのが手間なため（コードのみで済むのは１つの利点に思う）
- 特殊ケース等あり、無理に共通化しようとすると煩雑化しやすいし、template 分けるにしても物がどんどん増えて、大変になりそうなイメージがあるため (物が増えてくるとこの辺のバランスとるのが大変になりそう。コードのみで済むなら１ケース１ソースにし共通化できる部分は外出しして管理しやすいと思われる)

## AST（抽象構文木） 取得/解析コード

ソースファイルの情報を取得可能

```golang
import (
	"fmt"
	"go/ast"
	"go/parser"
	"go/token"
)

func Parse(filename string) error {
	fset := token.NewFileSet()
	f, err := parser.ParseFile(fset, filename, nil, parser.Mode(0))
	if err != nil {
		return err
	}
	// for _, d := range f.Decls {  // 1ファイルの全情報表示
	// 	ast.Print(fset, d)
	// 	fmt.Println()
	// }

	fieldNames := []string{}
	ast.Inspect(f, func(node ast.Node) bool {
		t, ok := node.(*ast.TypeSpec)
		if !ok {
			return true
		}

		st, ok := t.Type.(*ast.StructType)
		if !ok {
			return true
		}
		for _, field := range st.Fields.List {
			ast.Print(fset, field)
			fmt.Println()

			for _, nameNode := range field.Names {  // フィールド名取得
				fieldNames = append(fieldNames, nameNode.Name)
			}
		}
		return true
	})
	fmt.Print(fieldNames)
	return nil
}
```

## 解析結果

以下サンプルを解析した結果

```golang
type Move struct {
    id                 identifier.MoveId
    name               string
	description        *string  // *stringとするのはBatだがサンプルとして試す
    effects            *battles.Effects
	usedMember         []*Member
    leanableCharacters []Character
	leanablePokemons   []*identifier.PokemonId
    mixin.UpdateTimes
}
```

AST 上では

- 1 フィールドの情報は、\*ast.Field に格納されている
  - \*ast.Field は Names と Type を持つ
  - `a, b string` のように 1 フィールドに複数変数定義した場合は全て Names に格納される
- 各フィールドの型(Type)情報はそれぞれ以下の構造体で表現されている
  - 外部パッケージの型（例：identifier.MoveId）： \*ast.SelectorExpr
  - ポインタ型 (例：\*string)： \*ast.StarExpr
  - 配列/スライス (例：[]Character)：　\*ast.ArrayType
  - 末端の要素 (string、identifier、MoveId 等)： \*ast.Ident
  - 複合パターンも上記の組み合わせで表現： []\*identifier.PokemonId の場合 \*ast.ArrayType -> \*ast.StarExpr -> \*ast.SelectorExpr
  - 埋め込みの場合は、Names がないだけで Type は構造に変わりなし

### 実際の結果

- id identifier.MoveId

```
0  *ast.Field {
1  .  Names: []*ast.Ident (len = 1) {
2  .  .  0: *ast.Ident {
3  .  .  .  NamePos: <full path>\move.go:12:2
4  .  .  .  Name: "id"
5  .  .  .  Obj: *ast.Object {
6  .  .  .  .  Kind: var
7  .  .  .  .  Name: "id"
8  .  .  .  .  Decl: *(obj @ 0)
9  .  .  .  }
10  .  .  }
11  .  }
12  .  Type: *ast.SelectorExpr {
13  .  .  X: *ast.Ident {
14  .  .  .  NamePos: <full path>\move.go:12:16
15  .  .  .  Name: "identifier"
16  .  .  }
17  .  .  Sel: *ast.Ident {
18  .  .  .  NamePos: <full path>\move.go:12:27
19  .  .  .  Name: "HeldItemId"
20  .  .  }
21  .  }
22  }
```

- name string

```
0  *ast.Field {
1  .  Names: []*ast.Ident (len = 1) {
2  .  .  0: *ast.Ident {
3  .  .  .  NamePos: <full path>\move.go:13:2
4  .  .  .  Name: "name"
5  .  .  .  Obj: *ast.Object {
6  .  .  .  .  Kind: var
7  .  .  .  .  Name: "name"
8  .  .  .  .  Decl: *(obj @ 0)
9  .  .  .  }
10  .  .  }
11  .  }
12  .  Type: *ast.Ident {
13  .  .  NamePos: <full path>\move.go:13:16
14  .  .  Name: "string"
15  .  }
16  }
```

- description \*string

```
     0  *ast.Field {
     1  .  Names: []*ast.Ident (len = 1) {
     2  .  .  0: *ast.Ident {
     3  .  .  .  NamePos: <full path>/move.go:14:2
     4  .  .  .  Name: "description"
     5  .  .  .  Obj: *ast.Object {
     6  .  .  .  .  Kind: var
     7  .  .  .  .  Name: "description"
     8  .  .  .  .  Decl: *(obj @ 0)
     9  .  .  .  }
    10  .  .  }
    11  .  }
    12  .  Type: *ast.StarExpr {
    13  .  .  Star: <full path>/move.go:14:14
    14  .  .  X: *ast.Ident {
    15  .  .  .  NamePos: <full path>/move.go:14:15
    16  .  .  .  Name: "string"
    17  .  .  }
    18  .  }
    19  }
```

- effects \*battles.Effects

```
0  *ast.Field {
1  .  Names: []*ast.Ident (len = 1) {
2  .  .  0: *ast.Ident {
3  .  .  .  NamePos: <full path>\move.go:15:2
4  .  .  .  Name: "battleEffects"
5  .  .  .  Obj: *ast.Object {
6  .  .  .  .  Kind: var
7  .  .  .  .  Name: "battleEffects"
8  .  .  .  .  Decl: *(obj @ 0)
9  .  .  .  }
10  .  .  }
11  .  }
12  .  Type: *ast.StarExpr {
13  .  .  Star: <full path>\move.go:15:16
14  .  .  X: *ast.SelectorExpr {
15  .  .  .  X: *ast.Ident {
16  .  .  .  .  NamePos: <full path>\move.go:15:17
17  .  .  .  .  Name: "battles"
18  .  .  .  }
19  .  .  .  Sel: *ast.Ident {
20  .  .  .  .  NamePos: <full paht>\move.go:15:25
21  .  .  .  .  Name: "BattleEffects"
22  .  .  .  }
23  .  .  }
24  .  }
25  }
```

- ポインタ配列 usedMember []\*Member

```
0  *ast.Field {
1  .  Names: []*ast.Ident (len = 1) {
2  .  .  0: *ast.Ident {
3  .  .  .  NamePos: <full path>\move.go:4:2
4  .  .  .  Name: "items"
5  .  .  .  Obj: *ast.Object {
6  .  .  .  .  Kind: var
7  .  .  .  .  Name: "items"
8  .  .  .  .  Decl: *(obj @ 0)
9  .  .  .  }
10  .  .  }
11  .  }
12  .  Type: *ast.ArrayType {
13  .  .  Lbrack: <full path>\move.go:4:8
14  .  .  Elt: *ast.StarExpr {
15  .  .  .  Star: <full path>\move.go:4:10
16  .  .  .  X: *ast.Ident {
17  .  .  .  .  NamePos: <full path>\move.go:4:11
18  .  .  .  .  Name: "User"
19  .  .  .  }
20  .  .  }
21  .  }
22  }
```

- 配列 leanableCharacters []Character

```
0  *ast.Field {
1  .  Names: []*ast.Ident (len = 1) {
2  .  .  0: *ast.Ident {
3  .  .  .  NamePos: <full path>\move.go:14:2
4  .  .  .  Name: "leanablePokemons"
5  .  .  .  Obj: *ast.Object {
6  .  .  .  .  Kind: var
7  .  .  .  .  Name: "leanablePokemons"
8  .  .  .  .  Decl: *(obj @ 0)
9  .  .  .  }
10  .  .  }
11  .  }
12  .  Type: *ast.ArrayType {
13  .  .  Lbrack: <full path>\move.go:14:20
14  .  .  Elt: *ast.Ident {
15  .  .  .  NamePos: <full path>\move.go:14:22
16  .  .  .  Name: "Pokemon"
17  .  .  }
18  .  }
19  }
```

- ポインタ配列: leanablePokemons []\*indetifier.PokemonId

```
0  *ast.Field {
1  .  Names: []*ast.Ident (len = 1) {
2  .  .  0: *ast.Ident {
3  .  .  .  NamePos: <full path>\move.go:16:2
4  .  .  .  Name: "leanablePokemons"
5  .  .  .  Obj: *ast.Object {
6  .  .  .  .  Kind: var
7  .  .  .  .  Name: "leanablePokemons"
8  .  .  .  .  Decl: *(obj @ 0)
9  .  .  .  }
10  .  .  }
11  .  }
12  .  Type: *ast.ArrayType {
13  .  .  Lbrack: <full path>\move.go:16:19
14  .  .  Elt: *ast.StarExpr {
15  .  .  .  Star: <full path>\move.go:16:21
16  .  .  .  X: *ast.SelectorExpr {
17  .  .  .  .  X: *ast.Ident {
18  .  .  .  .  .  NamePos: <full path>\move.go:16:22
19  .  .  .  .  .  Name: "identifier"
20  .  .  .  .  }
21  .  .  .  .  Sel: *ast.Ident {
22  .  .  .  .  .  NamePos: <full path>\move.go:16:33
23  .  .  .  .  .  Name: "PokemonId"
24  .  .  .  .  }
25  .  .  .  }
26  .  .  }
27  .  }
28  }
```

- 埋め込み mixin.UpdateTimes

```
0  *ast.Field {
1  .  Type: *ast.SelectorExpr {
2  .  .  X: *ast.Ident {
3  .  .  .  NamePos: <full path>\move.go:16:2
4  .  .  .  Name: "mixin"
5  .  .  }
6  .  .  Sel: *ast.Ident {
7  .  .  .  NamePos: <full path>\move.go:16:8
8  .  .  .  Name: "UpdateTimes"
9  .  .  }
10  .  }
11  }
```

## jennifer によるコード生成

以下に example はあるものの読み取るのが大変なためケースごとに一部だけコードを記載

refs:

- [jennifer (Github - README)](https://github.com/dave/jennifer)
- [jennifer (godoc)](https://pkg.go.dev/github.com/dave/jennifer/jen)

パッケージ

```golang
f := jen.NewFile("pkg")
// package pkg
```

インポート

```golang
// f.ImportName("github.com/Symthy/Product/internal/xxx", "xxx")  // どちらでも変わらない模様
f.ImportName("github.com/Symthy/Product/internal/xxx", "")
// import xxx "github.com/Symthy/internal/xxx"

f.ImportAlias("github.com/Symthy/Product/internal/yyy", "ailias")
// import ailias "github.com/Symthy/internal/yyy"

importNames := map[string]string{
	"github.com/Symthy/Product/internal/xxx": "xxx",
	"github.com/Symthy/Product/internal/yyy": "yyy",
	"github.com/Symthy/Product/internal/zzz": "zzz",
}
f.ImportNames(importNames)
// import (
//     xxx "github.com/Symthy/Product/internal/xxx"
//     yyy "github.com/Symthy/Product/internal/yyy"
//     zzz "github.com/Symthy/Product/internal/zzz"
// )
```

構造体

```golang
f.Type().Id("SampleBuilder").Struct(
  jen.Id("id").Qual("github.com/Symthy/Product/internal/domain/value", "Indetifier"),
  jen.Id("name").String(),
  jen.Id("description").String(),
  jen.Id("effects").Index().Op("*").Qual("github.com/Symthy/Product/internal/domain/battles", "Effects"),
)
// type SampleBuilder struct {
//     id          value.Identifier
//     name        string
//     description string
//     effects     []*battles.Effects
//}

// 以下のように組み立てることも可能
fieldStatements := []*jen.Statement
fieldStatements = append(fieldStatements, jen.Id("id").Qual("github.com/Symthy/Product/internal/domain/value", "Indetifier"))
//  : 略
f.Type().Id("SampleBuilder").StructFunc(func(g *jen.Group) {
    for _, fieldStatement := range fieldStatements {
        g.Add(fieldStatement)
    }
})
```

コンストラクタ or 関数

```golang
typeName := "SampleBuilder"
f.Func().Id("New"+typeName).
		Params().
		Op("*").Qual("", typeName).
		Block(
			jen.Return(jen.Op("&").Qual("", typeName).Block()),
		)
// func NewSampleBuilder() *SampleBuilder {
//     return &SampleBuilder{}
// }
```

メソッド (セッター)

```golang
receiverName = "s"
typeName := "SampleBuilder"
argVarName := "name"
f.Func().
		Params(jen.Id(receiverName).Op("*").Id(typeName)).   // pointer receiver
		Id("Name").                                          // func
		Params(jen.Id(argVarName).String()).                 // arguments
		Op("*").Qual("", typeName).                          // return type
		Block(
			jen.Id(receiverName).Op(".").Id("name").Op("=").Id(argVarName),
			jen.Return(jen.Id(receiverName)),
		)
// func (s *SampleBuilder) Name(name string) *SampleBuilder {
//     s.name = name
//     return s
// }
```

部分的にに作って、Add() で任意の要素に付け足すことが可能なため柔軟。

## go での コード生成

- go generate で完結するようにした方が良い
- コード生成を行うための go ファイルに以下を追加すれば、 `go generate ./...` で実行できる

```golang
//go:generate go run .
```

ref: [go generate のベストプラクティス](https://qiita.com/yaegashi/items/d1fd9f7d0c75b2bb7446)
