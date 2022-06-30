# Job: Golang で ログローテートと設定ファイル読み込み改修 取捨選択＆実装

自らの立ち回り、検討事項、実装コードを記す

## 背景

これまで Linux のみサポートの製品(言語:Golang)を 別プラットフォームに対応する必要がでてきた

- Linux 依存の部分(ログローテート等)があったため対応が必要
  - ログローテートも Golang で実装
- 第一候補として挙がったのが Golang のログローテートで有名な lumberjack

[Golang はどのようにクロスプラットフォームの開発とテストを簡素化するのか](https://qiita.com/KentOhwada_AlibabaCloudJapan/items/59c1053b3eec189318de)

### 着手前の状態

- ログローテートには Linux の logrotate.d が使用されていた

- 設定ファイルは、systemd のサービスユニットファイルで `EnvironmentFile=<value>` により環境変数に展開して使用

## 蛇足：Linux に関するちょっとした Tips

(コンテナ運用ではなく) Linux の systemd のサービスユニットファイルで設定した環境変数は、そのサービスのみで使用される private な環境変数となる＝他へ影響を及ぼさない/他からの影響を受けない

```
[Service]
Environment=<環境変数リスト>
EnvironmentFile=<環境変数ファイル>
```

これを golang では、以下のみで取れる（指定の key がなければ空文字が取れるだけ）

```golang
os.Getenv("key")
```

これの何が良いかと言うと、システムのグローバル変数として使うことができる

共通のグローバルな値を golang のコード上で定数/変数を定義した場合、メモリを占有し続けることになる。少量なら問題ないかもしれないが、積もり積もって、ガーベージコレクション時のオーバーヘッドが高くなれば、性能劣化に繋りかねない。（参考：[Go の GC のオーバーヘッドが高くなるケースと、その回避策](https://qiita.com/imoty/items/c1017099e63cd4630946)）

ただし、イミュータブルにすることはできずグローバルな「変数」であることに変わりないため、取り扱いには気を付ける必要がある。たとえば

- 定数として扱うように規約を定める、仕組化する
- グローバル変数として扱うなら、Repository 層のように取得/更新のインターフェースを定め、状態の管理を徹底する

など。

## 取り組み

### ログローテート

lumberjack が第一候補として挙がっていたが、ちょっとした問題点が見つかる。

1. ローテートの契機が (logrotate.d とは) 異なる
2. ローテートした後のファイル名のフォーマットが異なる

詳細：

|                             | logrotate.d                                                                    | lumberjack                                          |
| --------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------------- |
| 1. ローテート契機           | 1 日 1 回ローテート（時、週、月毎等変更可）                                    | 最大サイズ(default:100MB)を<br>超過したらローテート |
| 2. ローテート後のファイル名 | 末尾に付ける日付のフォーマット指定可（<ログファイル名>.log<指定フォーマット>） | 固定 (<ログファイル名>-yyyy-MM-ddTHH:mm:ss.fff.log) |

#### 「1. ローテートの契機が異なる」について

念のため、lumberjack で日毎にローテートする機構があったりしないか、コードも見て確認。
だが、以下の通り、ローテートするかは最大サイズしか見ていなかった (2022/6 時点)

```go
	if info.Size()+int64(writeLen) >= l.max() {
		return l.rotate()
	}
```

```go
	if l.size+writeLen > l.max() {
		if err := l.rotate(); err != nil {
			return 0, err
		}
	}
```

できれば、ローテート契機を変えずに済む OSS があればと思うが、

golang のログローテートといえば、lumberjack というイメージがあり、(以前プライベートで)日本語でググった際に他の有力な OSS を見かけたことがないため、存在していたとしてもマイナー寄りかもしれない。

そう思い、英語情報を漁らないと見つからない可能性があると判断。「golang log rotate daliy」で検索するも、

商用で使えるレベルのものは見つからなかった。

- 唯一使えそうに思えたのは以下。ただしアーカイブされていた
  - [file-rotatelogs](https://github.com/lestrrat-go/file-rotatelogs)
- 他は個人の方が作成されたようなもの位しか見つけられず

よって、lumberjack を使わず logrotate.d と同等のログローテートを実現しようとすると、自分達で作るしかない。例えば

- (ライセンス的に問題のない) OSS のコードを拝借する等して自分たちの持ち物とし、自作する
- lumberjack をフォークして日毎に 参考：[Daily Rolling Logger](https://sptci.com/docs/go/dailyrollinglogger.html)

ただ、自作したとして

- コスト（開発コスト、以降のメンテナンスコスト等）に対するリターンが、見合わない
- lumberjack を使うにあたり、1 面あたりの容量を 1 日以上持てる大きさにすれけば運用上もそう困ることはない

という点から lumberjack で行くことにした。

#### 「2. ローテートした後のファイル名のフォーマットが異なる」について

これにより何が起きるか

- logrotate.d でローテートされたログファイルを lumberjack には引き継がれない（無視する）ため、そのまま残り続ける

できれば lumberjack に引き継がれて、古いものから自然に削除されて欲しい。そこで考えた。

logrotate.d で作成されたファイル名を lumberjack がローテート時に付けるファイル名に合わせれば、lumberjack の仕組みに乗っかり、ローテートされるのはないかと推測。

lumberjack のソースを見る限り、この推測は正しそう。（該当箇所ソース：https://github.com/natefinch/lumberjack/blob/47ffae23317c5951a2a6267a069cf676edf53eb6/lumberjack.go#L400 ）

ファイル名を一括置換する shell を組んで実行。実機で lumberjack を使ったコードで動かして試してみると、推測通りに動き、この問題は回避できた。

### 設定ファイル

設定ファイルは、Linux のサービスユニットファイルで環境変数に読み込んで使用する。という Linux 依存の部分を golang の処理で設定ファイルを読み込むようにして、別プラットフォームに対応する。

設定ファイルの読み込み処理は新規に実装する必要があるため、挙げた選択肢は以下３つ。

1. go.ini を利用
2. godotenv を利用
3. 別サービスの既存コードを流用

結論を先に述べれば、選んだのは「go.ini を利用」。他を除外した理由はそれぞれ以下の通り。

- godotenv

読み込んだファイルを環境変数にセットしてくれ、os.Getenv で変わらず取得できる OSS。これが製品の既存コードとの親和性とも高いため、ベストな選択肢ではと最初は考えていた。

[godotenv](https://github.com/joho/godotenv)

だが、以下のように書かれており、動作の保証ができないため、使用を断念。

> There is test coverage and CI for both linuxish and Windows environments, but I make no guarantees about the bin version working on Windows.
>
> 翻訳結果：Linux 環境と Windows 環境の両方でテストカバレッジと CI がありますが、Windows で動作する bin バージョンについては保証しません。

- 別サービスの既存コード

あるにはあったレベル。理想は、共通部品として切り出して両者でそれを利用するようにするのが良いとは考えた。だが…

今すぐそれを行える余力が(組織的に)なく、かといって同じコードを量産したくない（流用したコードに何かあれば両者共に直す必要が出てくる可能性）。また、戻り値が `(map[string]string, error)` 関数のため、そのままでは少し扱いづらく改良も必要。

#### 実装

故に go.ini が安牌と考え、採用して実装した。

とはいえ、そのまま使用して製品コードと go.ini を密結合にさせると、不測の事態で go.ini から別の OSS または自作ソースへの乗り換えが発生した場合に、手間がかかってしまう。

そこで、interface を定義してラップし、疎結合とすることで、その手間を軽減する。

```golang
type Config interface {
	GetString(key string) string
	GetInt(key string) (int, error)
}

type GoIniConfig struct {
	file *ini.File
}

func (c GoIniConfig) GetString(key string) string {
	return c.file.Section("").Key(key).String()
}

func (c GoIniConfig) GetInt(key string) (int, error) {
	return c.file.Section("").Key(key).Int()
}
```

また、設定ファイルの構成は、(よくある？)システム用とユーザー用の２つあり、値の優先度は

- ユーザー設定ファイル > システム設定ファイル > デフォルト値

のため、そこもいい感じにコードで表現する。

```golang
type ConfigValueResolver struct {
	systemConf Config
	userConf   Config
}

func (c ConfigValueResolver) ResolveValueStringOrDefault(key string, defaultValue string) string {
	value := defaultValue
	value = getConfValueStringOrElse(c.systemConf, key, value)
	value = getConfValueStringOrElse(c.userConf, key, value)
	return value
}

func getConfValueStringOrElse(conf Config, key string, defaultValue string) string {
	// key がない場合は "" が返ってくる
	if confValue := conf.GetString(key); confValue != "" {
		return confValue
	}
	return defaultValue
}
```

コードの全体イメージ（テスト含む）は [こちら（Github）](https://github.com/Symthy/golang-practices/tree/main/go-config_load)

※テストには [testify](https://github.com/stretchr/testify) の mock を使用することで、設定値の優先度（ユーザー設定ファイル > システム設定ファイル > デフォルト値）のテストを実装し、実ファイルに依存することなくコード上で全テストケース表現（そのための Config の interface 化でもある）。また、各テストケースがどういう内容か見づらいため、 [Go のテーブル駆動テストをわかりやすく書きたい](https://zenn.dev/kimuson13/articles/go_table_driven_test) を参考に見やすくしてみた。

#### 蛇足

lumberjack.Logger を log.SetOutput() でセットしたり、フレームワークの[Echo](https://github.com/labstack/echo) を使用していたため、そちらのロガーに渡したりする必要があった。

が、lumberjack.Logger のインスタンス生成する前に、設定ファイルから必要な値を取得する必要がある。でも設定ファイル読み込み失敗等はログに出力する必要があるという矛盾…

なので、関数を使って簡易バッファリング。log.SetOutput() してから、まとめて出力。

```golang
LoadConfigFile(filePath string, logBufferedWriters []func()) (Config, []func()) {
	cfg, err := ini.Load(filePath)
	if err != nil {
		logWriters := append(logBufferedWriters, func() {
			log.Printf("Failed to file: %v\n", err)
		})
		return nil,
	}
	return &ConfigFile{file: cfg}, logBufferedWriters
}
```

※関数は便利。なんとなく方法として微妙な気がするが、良い方法を思いつかない。精進

## 最後に

実務で golang を初めて使う機会（一ヶ月間）を得て、それから半年強のブランクを経て、再度その機会が巡ってきた。

当時は、基本構文＋ α さえ押さえておけばなんとかなるレベルであったため、事前にそのレベルまでの習得に留めたが、それからポートフォリオを作ろうとプライベートで半年書き続けていた甲斐あり、ある程度スムーズにこなすことができた（途中割り込みありありで 700step 強/3 日、速くはないか…）。

地道な努力が功を奏したと思える瞬間。だがまだ精進が必要。チャンスを掴み取るためにも地道に積み重ねるしかない。
