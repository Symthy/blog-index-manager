# Golang コード自動生成

モチベーション：単調なコード追加の繰り返しはコード自動生成に置き換えたい

## Golang のコードから Golang のコードを生成する

単なるCRUDのコード実装だけなら（ビジネスロジックは関係ないため）

- domain層にentity追加

以下は(単純な追加だけなので)自動生成に置き換えられるはず

- domain層に追加したentityに対するRepositoryインターフェース
- entityのfactory
- Repositoryインターフェースの実装
- 実装したコードのテスト

AST(抽象構文木)を利用するのが正確な解析＆生成ができて良さそう。

### コードからの情報取得

ソースコードをparse -> AST（抽象構文木）にした後で解析して取得

- (構文木として意味を持った状態で扱えるため) 欲しいノードが探しやすい。正確に取得可

```golang
func main() {
  fset := token.NewFileSet()
  f, err := parser.ParseFile(fset, "./example/example.go", nil, 0)  // 第4引数はMode
  if err != nil {
    fmt.Println(err)
    return
  }

  // 最初に見つかったstruct名を入れる
  var name string
  ast.Inspect(f, func(n ast.Node) bool {
    x, ok := n.(*ast.TypeSpec) // type xxxx の型宣言部分取得
    if !ok {
      return true
    }
    if _, ok := x.Type.(*ast.StructType); ok {
      // 取れた type が struct なら その名前取得
      if name == "" {
        name = x.Name.String()
      }
    }
    return true
  })
  fmt.Println("struct name:", name)
}
```

構文解析参考：

- [Go言語の golang/go パッケージで初めての構文解析](https://qiita.com/po3rin/items/a19d96d29284108ad442)

### コード生成

AST（抽象構文木）を組み立てる

- 構文木として意味を持った状態で扱えるため、文法ミスがない
- ※テンプレートエンジン使用での実現方法は、テンプレートの構文間違えていても気付きにくい

ASTだと、以下の少量だけでも多量のコードを書く必要がある。
[jennifer (code generator)](https://github.com/dave/jennifer) を使用すればシンプルに書ける。

```golang
package main

import "fmt"

func main() {
  fmt.Println("Hello, 世界")
}
```

のコードを生成するのに、

- ASTの場合：

```golang
package main

import (
  "go/ast"
  "go/format"
  "go/token"
  "os"
  "strconv"
)

func main() {
  f := &ast.File{
      Name: ast.NewIdent("main"),
      Decls: []ast.Decl{
        &ast.GenDecl{
          Tok: token.IMPORT,  // import 部
          Specs: []ast.Spec{
              &ast.ImportSpec{
                Path: &ast.BasicLit{
                  Kind:  token.STRING,
                  Value: strconv.Quote("fmt"),
                },
              },
          },
        },
        &ast.FuncDecl{
          Name: ast.NewIdent("main"),  // main 関数部
          Type: &ast.FuncType{},
          Body: &ast.BlockStmt{
              List: []ast.Stmt{
                &ast.ExprStmt{
                  X: &ast.CallExpr{
                      Fun: &ast.SelectorExpr{
                        X:   ast.NewIdent("fmt"),
                        Sel: ast.NewIdent("Println"),
                      },
                      Args: []ast.Expr{
                        &ast.BasicLit{
                          Kind:  token.STRING,
                          Value: strconv.Quote("Hello, 世界"),
                        },
                      },
                  },
                },
              },
          },
        },
      },
  }

  format.Node(os.Stdout, token.NewFileSet(), f)
}
```

ref: [Goの抽象構文木（AST）を手入力してHello, Worldを作る #golang](https://qiita.com/tenntenn/items/0cbc6f1f00dc579fcd8c)

- jennifer の場合：

```golang
package main

import (
  "fmt"

  "github.com/dave/jennifer/jen"
)

func main() {
  f := NewFile("main")
  f.Func().Id("main").Params().Block(
    Qual("fmt", "Println").Call(Lit("Hello, world")),
  )
  fmt.Printf("%#v", f)
}
```

## ref

[entityからコード自動生成した話](https://tech.mfkessai.co.jp/2019/09/ebgen/)
