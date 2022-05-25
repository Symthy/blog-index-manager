# gRPC (by golang)

動機：SOAのとあるシステムで、新規のデータを新規DBに持ち、かつそのデータを既存サービス＆新設サービスの２つ(a) が利用するようになるため、新規のデータ群の管理を担う新規サービス(b)を立て、(a)(b)両者のやりとりに gRPC を用いるのが適切と思ったため Study

## gRPC とは

Google が開発した RPC フレームワークで、gRPC を使うと異なる言語で書かれたアプリケーション同士が gRPC により自動生成されたインターフェースを通じて通信することが可能。
データのシリアライズには Protocol Buffers を使用。

RPC（Remote Procedure Call）：

- ネットワーク上の他の端末と通信するための仕組み。
- 「クライアント−サーバー」型の通信プロトコルであり、サーバー上で実装されている関数（Procedure、プロシージャ）をクライアントからの呼び出しに応じて実行する技術
- （RESTのようにパスとメソッドの指定ではなく）メソッド名と引数を指定する
- （リソースと機能(関数)の紐づけがされるため、時折 REST API 設計で発生するリソースと機能のマッピングで困る点が解消される？）

### 利点/欠点

利点：

- HTTP/2による高速な通信が可能。(データはバイナリデータでやり取りする仕様)
- Protocol Buffersによるスキーマファーストの開発。protoファイルというIDLからコードの自動生成が可能。
- 様々なストリーミング方式の通信が可能。

欠点：

- クライアントとサーバの両方に特別なソフトウェアを導入しなければならない
- クライアントとサーバが別環境の場合、protoファイルの変更の追随を解決しなければならない
- gPRCで生成されたコードはクライアントとサーバのビルドプロセスに組み込まなければならない
- HTTP2通信ができる環境が必要

### 適したケース

- マイクロサービス間の通信
  - バックエンド間は恩恵が多く得られる
- モバイルユーザが利用するサービス
  - 通信量削減
- 速度が求められる場合

### APIとの比較 (個人の主観)

- 大量データ送受信
  - REST APIの場合：制御面で多少手間がかかる？
    - サーバへ送信：multipart/form-data (分割送信) or Base64 
      - ref: [WebAPI でファイルをアップロードする方法アレコレ](https://qiita.com/mserizawa/items/7f1b9e5077fd3a9d336b)
      - multipart/form-data は GraphQLのようにJSONでやり取りせざるを得ない場合使えない。Base64 で送信 ref: [GraphQL APIで画像をアップロードする](https://blog.spacemarket.com/code/graphql-image/)
    - サーバから取得：streamingで1レスポンスで分割送信、206応答しAPIを複数回実行してもらっての分割取得、等
  - gRPCの方が得意（ストリーミング方式で仕組化されている上、HTTP2通信により速度も速い） 
- 仕様変更追従
  - REST APIの場合 (OpenAPI記述のyaml等から自動生成)
    - とあるサービスorデータストア(サーバ側)のAPI仕様に変更が入っても、それを利用する（クライアント）側に影響のない変更であれば即追従の必要はない（そのまま運用できる）
    - 裏を返せば、追従漏れを起こすリスクもある
  - gRPCの場合
    - 変更が入ったら、利用する（クライアント）側も即追従する必要がある？
    - 裏を返せば、即追従が必要なほどサービス同士が密な関係であれば、（即追従する必要があるため）追従漏れは起きず、有効に働くのではないか


## 環境構築

protocol buffer install (Windowsの場合)：

https://github.com/protocolbuffers/protobuf/releases から zip取得。環境変数にbinのパス追加

Go plugins install：

```sh
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```

確認

```sh
protoc --version
protoc-gen-go --version
protoc-gen-go-grpc --version
```

```sh
go get -u google.golang.org/grpc
```

## Protocl Buffers

|#|利点|欠点|
|---|---|---|
|JSON|・あらゆる言語で利用可能<br>・複雑な形式(配列/ネスト)を扱える|・データスキーマを強制できない<br>・データサイズが大きくなりがち|
|Protocol Buffers|・型が保証される<br>・データサイズは小さい(バイナリ)|・複雑すぎる構造には不向き<br>・一部言語は未対応|

.protoを作成 → 開発言語のオブジェクト自動生成 → (送信時データを)バイナリ形式へシリアライズ

## .proto ファイル

### 書き方

- message
  - フィールドのフォーマット： <フィールドの型> <フィールド名> = <タグ番号>; (例： `int32 id = 1;`)
  - スカラー型：https://developers.google.com/protocol-buffers/docs/proto3#scalar
  - ネストが可能

- tag
  - (Protocol Buffersは) フィールドをタグ番号で識別。一意な番号
  - 最小値：１，最大値：2^29 - 1 (536,870,911)
  - 19000～19999 は予約番号のため使用不可
  - 1～15番は1byteのためパフォーマンス良。よく使うフィールドを割り当てるのが吉
  - タグは連番にする必要がない

- enum (列挙型)
  - タグ番号が0から始まる

- 各種フィールド
  - repated： 配列相当のフィールド。複数の要素を含めることが可能
  - map：連想配列相当のフィールド。
  - oneof：いずれかの型を持つフィールド。repatedフィールドにはできない

- import/package が可能

```
syntax = "proto3";

package employee

impot "proto/date.proto";

message Employee {
  int32 id = 1;
  string name = 2;
  string email = 3;
  Occupation occupation = 4;
  repeated string third_party_account = 5;
  map<string, Company.Product> products = 6;
  oneof profile {
    string text = 7;
    URL url = 8;
  }
  date.Date joinedDate
}

enum Occupation {
  UNKNOWN = 0;
  ENGINEER = 1;
  DESIGNER = 2;
  MANAGER = 3;
}

message Company {
  message Product {}
}
message URL {
}
```

```date.proto
package date;

message Date {
  int32 year = 1;
  int32 month = 2;
  int32 day = 3;
}
```

### コンパイル

```
protoc -I. --go_out=. proto/*.proto 
```

gRPC用のコードも出力

```
protoc -I. --go_out=. --go-grpc_out=. proto/*.proto
```

## gRPC 4つの方式 & Servicea定義

### Unary RPC

- 1リクエスト1レスポンス方式
- 通常の関数コールのように扱える
- 用途：API等

```
message SayHelloRequest {}
message SayHelloResponse {}

service Greeter {
    rpc SayHello (SayHelloRequest) returns (SayHelloResponse);
}
```

### Server Streaming RPC

- 1リクエスト・複数レスポンス方式
- クライアントはサーバから送信完了の信号が送信されるまでStreamのメッセージを読み続ける

```
message SayHelloRequest {}
message SayHelloResponse {}

service Greeter {
    rpc SayHello (SayHelloRequest) returns (stream SayHelloResponse);
}
```

### Client Streaming RPC

- 複数リクエスト・1レスポンス方式
- サーバはクライアントからリクエスト完了の信号が送信されるまでStreamからメッセージを読み続ける。全部受け取ってからレスポンスを返す
- 

```
message SayHelloRequest {}
message SayHelloResponse {}

service Greeter {
    rpc SayHello (stream SayHelloRequest) returns (SayHelloResponse);
}
```

### Bidirectional Streaming RPC

- 複数リクエスト・複数レスポンス方式
- クライアントとサーバのStreamが独立
- リクエストとレスポンスの順序は問わない
- 用途：チャット、オンライン対戦ゲームなど

```
message SayHelloRequest {}
message SayHelloResponse {}

service Greeter {
    rpc SayHello (stream SayHelloRequest) returns (stream SayHelloResponse);
}
```

## Interceptor

- メソッド前後に処理を挟むための仕組
- 認証やロギング、監視、バリデーションなど複数のRPCで共通して行いたい処理で利用する
- サーバ側/クライアント側どちらも対応
  - サーバ
    - UnaryServerInterceptor
    - StreamServerInterceptor
  - クライアント
    - UnaryClientInterceptor
    - StreamClientInterceptor

以下を満たす関数を実装

```go
type UnaryServerInterceptor func(
  ctx context.Context
  req interface{}
  info *UnaryServerInfo // メソッド等のサーバ情報
  handler UnaryHandler  // クライアントからコールされるhandler
) (resp interface{}, err error) // resp: handlerからのレスポンス
```

Interceptor追加方法

```go
// サーバ
server := grpc.NewServer(
  grpc.UnaryInterceptor(myInterceptor())
)

// クライアント
connection, err := grpc.Dial(
  "localhost:50001",
  grpc.WithUnaryInterceptor(myInterceptor())
)
```

### ロギング

```go
func logging() grpc.UnaryServerInterceptor {
    return func(ctx context.Context, req interface{}, info *grpc.UnaryServerInfo, handler grpc.UnaryHandler) (resp interface{}, err error) {
        log.Printf("request: %+v", req)
        resp, err = handler(ctx, req)
        if err != nil {
          return nil, err
        }
        log.Printf("response: %+v", resp)
        return resp, nil
    }
}
```

### 認証

https://github.com/grpc-ecosystem/go-grpc-middleware

例：

- サーバ側

```go
func main() {
  // :
  server := grpc.NewServer(
		grpc.UnaryInterceptor(
			grpc_middleware.ChainUnaryServer(
				buildLogging(),
				grpc_auth.UnaryServerInterceptor(authorize),
			),
		),
	)
  pb.RegisterFileServiceServer(server, &Server{})
  // :
}

func authorize(ctx context.Context) (context.Context, error) {
	token, err := grpc_auth.AuthFromMD(ctx, "Bearer")
	if err != nil {
		return nil, err
	}

	if token != "xxxxx" {
		return nil, status.Error(codes.Unauthenticated, "token is invalid")
	}
	return ctx, nil
}
```

- クライアント側

```go
func callServerMethod() {
	md := metadata.New(map[string]string{"authorization": "Bearer xxxxx"})
	ctx := metadata.NewOutgoingContext(context.Background(), md)

  // :
}
```

認証エラー出力（クライアント側）

```
2022/05/25 21:35:44 rpc error: code = Unknown desc = bad token
exit status 1
```

### エラーハンドリング

公式ドキュメント： https://www.grpc.io/docs/guides/error/

例：

- サーバ側

```go
return nil, status.Error(codes.NotFound, "not found")
```

- クライアント側

```go
  res, err := client.serverMethod(ctx, &pb.ServerRequest{})
	if err != nil {
		resErr, ok := status.FromError(err)
		if ok {
			if resErr.Code() == codes.NotFound {
				log.Fatalf("Error Code: %v, Error Message: %v", resErr.Code(), resErr.Message())
			}
		} else {
			log.Fatalln("unknown error")
		} 
  } else {
    log.Fatalln(err)
  }
```

### Deadlines

サーバからレスポンスを待つ時間（超えたらタイムアウトでエラー）

例：

- クライアント側

```go
func callServerMethod() {
	ctx, cancel := context.WithTimeout(ctx, 3*time.Second)
	defer cancel()

  res, err := client.serverMethod(ctx, &pb.ServerRequest{})
  if err != nil {
		resErr, ok := status.FromError(err)
    if resErr.Code() == codes.DeadlineExceeded {
	  	log.Fatalln("deadline exceeded")
    }
    // :
  }
}
```

### SSL通信化

例：

- サーバ側

```go
func main() {
  // :
  credentials, err := credentials.NewServerTLSFromFile(
		"ssl/localhost.pem",
		"ssl/localhost-key.pem",
	)
	if err != nil {
		log.Fatalln(err)
	}

	server := grpc.NewServer(
		grpc.Creds(credentials),
    // :
  )
  // :
}
```

- クライアント側

```go
func main() {
  certfile := "xxxxxx/rootCA.pem"
  creds, err := credentials.NewClientTLSFromFile(certFile, "")
  conn, err := grpc.Dial("localhost:50000", grpc.WithTransportCredentials(creds))
  // :
}
```

## ref 

環境構築：

- [gRPC Quick Start](https://grpc.io/docs/languages/go/quickstart/)
- [Protocol Buffer Basics: Go](https://developers.google.com/protocol-buffers/docs/gotutorial)

参考：

- [サービス間通信のための新技術「gRPC」入門](https://knowledge.sakura.ad.jp/24059/)

- [Go言語で簡単なgRPCサーバーを作成](https://dev.classmethod.jp/articles/golang-grpc-sample-project/)

- [Go で実装しながら gRPC を理解する](https://reboooot.net/post/hello-grpc/)

Try Code：　https://github.com/Symthy/golang-practices/tree/main/go-gRPC