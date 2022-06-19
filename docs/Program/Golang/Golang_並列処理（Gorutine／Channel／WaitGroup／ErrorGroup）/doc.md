# Golang 並列処理（Gorutine/Channel/WaitGroup/ErrorGroup）

Go の魅力

- 他の言語は後から並列処理の機構を組み込むと大手術になることがあるが、Go は容易
- 高水準のパフォーマンスが出るコードを少ない手間で実現できるところ
- I/O コストが高い領域は Go との相性が良い

Go の業務アプリケーションで並列処理の適用を検討すべき場面は、1 リクエスト/バッチタスクの内部を高速化したい時。（例：１リクエスト中で複数データストアから情報取得し、結果を複数箇所に格納が必要な時）

## Gorutine

- 個々の goroutine は識別不可
- 優先度や親子関係はない
- 外部から終了させられない
- 終了検知には別の仕組みが必要（channel?)
- かなり少ない量のメモリしか要求せず、起動は高速
  - 起動コストはゼロではない

goroutine の乱用は避ける

- 並列処理は複雑さと高める
- goroutine を駆使したコードは意図が伝わりにくい
- 基本的には標準/準標準パッケージ機能の利用を検討

```golang
func main() {
	go output("goroutine")

	go func(msg string) {
		fmt.Println(msg)
	}("immediate execution")
}
```

## Channel

- 同時実行する goroutine を接続するパイプ（複数の goroutine から送受信しても安全が保障されたキュー）
- Channel は同期の手段
  - Channel は goroutine をブロックする
  - 送信 goroutine と受信 goroutine が揃うまでブロック（バッファなしの場合)
  - 送信側のバッファ一杯になると受信側が取りに来るまで or バッファが空ならブロック（バッファありの場合）

※ブロック＝待ち受け

```golang
func main() {
	msgs := make(chan string, 3)
	msgs <- "main"
	go func() {
		msgs <- "func1"
	}()
	go func() {
		msgs <- "func2"
	}()

	msg1 := <-msgs  // channelから値を読み込むまでメインgoroutineストップ
	msg2 := <-msgs
	msg3 := <-msgs
	fmt.Println(msg1, msg2, msg3)  // main func2 func1
}
```

- 一方向チャネル型
  - チャネルの向きを指定できる。向き：送信/受信

```golang
func send(recvCh chan<- string, msg string) {
	recvCh <- msg
}

func receive(sendCh <-chan string, recvCh chan<- string) {
	msg := <-sendCh
	recvCh <- msg
}

func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)

	// send(ch1, "sending")  deadlock..
	// receive(ch1, ch2)
	go send(ch1, "sending")
	go receive(ch1, ch2)
	fmt.Println(<-ch2)
}
```

- キャパシティが一杯のチャネルに書き込もうとするゴルーチンは、チャネルの空きが出るまで待機する
- 空のチャネルから読み込もうとするゴルーチンは、チャネルに要素が入ってくるまで待機する

```golang
func main() {
	// send slow
	ch1 := make(chan string, 2)
	go func() {
		for i := 0; i < 6; i++ {
			send := "send" + strconv.Itoa(i)
			ch1 <- send
			time.Sleep(1 * time.Second)
		}
	}()
	go func() {
		for j := 0; j < 3; j++ {
			fmt.Println("sub:", j, <-ch1)
		}
	}()
	for j := 0; j < 3; j++ {
		fmt.Println("main:", j, <-ch1)
	}
	time.Sleep(3 * time.Second)
}
//main: 0 send0
//sub: 0 send1
//main: 1 send2
//sub: 1 send3
//main: 2 send4
//sub: 2 send5
```

### Select

複数チャネルの待ち受けかつチャネル毎の制御ができる。

- 複数 goroutine の待ち受け可
- 先に終わったものから捌く

```golang
func main() {
	ch1 := make(chan string)
	ch2 := make(chan string)
	// ch3 := make(chan string)
	go func() {
		time.Sleep(1 * time.Second)
		ch1 <- "one"
	}()
	go func() {
		time.Sleep(2 * time.Second)
		ch2 <- "two"
	}()

	for i := 0; i < 2; i++ {
		select {
		case msg1 := <-ch1:
			fmt.Println("received1", msg1)
		case msg2 := <-ch2:
			fmt.Println("received2", msg2)
		// default:
		// fmt.Println("none")
     	// default句を入れると待ち受けが起こらず全てnoneが出力
		// default句は何も送受信がなかった時の処理
		// goroutine起動のタイムラグによるすり抜け
		}
	}
}
// received1 one
// received2 two
```

#### timeout

```golang
func main() {

	ch1 := make(chan string, 1)
	go func() {
		time.Sleep(2 * time.Second)
		ch1 <- "sending 1"
	}()

	select {
	case res := <-ch1:
		fmt.Println(res)
	case <-time.After(1 * time.Second):
		fmt.Println("timeout 1")
	} // timeout

	ch2 := make(chan string, 1)
	go func() {
		time.Sleep(2 * time.Second)
		ch2 <- "sending 2"
	}()
	select {
	case res := <-ch2:
		fmt.Println(res)
	case <-time.After(3 * time.Second):
		fmt.Println("timeout 2")
	} // success
}
```

#### Non-Blocking Channel Operation

- バッファなし channel のため最初からブロック
- `<-readCh` : Channel から値読み込みを永遠に待ち続ける = 値書き込みがなければ永続待機 = deadlock 発生

```golang
func main() {
	// var writeCh chan<- string
	var readCh <-chan string
	ch := make(chan string)
	readCh = ch

	go func() {
		// writeCh <- "Writing..."
	}()

	fmt.Println(<-readCh)
}
// fatal error: all goroutines are asleep - deadlock!
```

上記ケースを制御できるのが default

```golang
func main() {
	messages := make(chan string)
	signals := make(chan bool)

	select {
	case msg := <-messages:
		fmt.Println("received message", msg)
	default:
		fmt.Println("no message received")
	}

	msg := "hi"
	select {
	case messages <- msg:
		fmt.Println("sent message", msg)
	default:
		fmt.Println("no message sent")
	}

	select {
	case msg := <-messages:
		fmt.Println("received message", msg)
	case sig := <-signals:
		fmt.Println("received signal", sig)
	default:
		fmt.Println("no activity")
	}
}
```

### close

(チャネル受信待ちなど) ブロック中の goroutine を解放

```golang
func main() {
	jobs := make(chan int, 5)
	done := make(chan bool)

	go func() {
		for {
			j, more := <-jobs
			if more {
				fmt.Println("received job", j)
			} else {
				fmt.Println("received all jobs")
				done <- true
				return
			}
		}
	}()

	for j := 1; j <= 3; j++ {
		jobs <- j
		fmt.Println("sent job", j)
	}
	close(jobs) // ループも解除
	time.Sleep(time.Second)
	fmt.Println("sent all jobs")

	<-done
}
```

クローズすることで、range を用いて channel から取り出すことができる

※クローズしなければ受信待ちによるブロックで deadlock

```golang
func main() {
    queue := make(chan string, 2)
    queue <- "one"
    queue <- "two"
    close(queue) // 削除するとdeadlock

    for elem := range queue {
        fmt.Println(elem)
    }
}
```

## worker

```golang
func worker(id int, jobs <-chan int, results chan<- int) {
    for j := range jobs {
        fmt.Println("worker", id, "started  job", j)
        time.Sleep(time.Second)
        fmt.Println("worker", id, "finished job", j)
        results <- j * 2
    }
}

func main() {
    const jobNum = 5
    jobs := make(chan int, numJobs)  // ★バッファ有無で挙動が変わる
    results := make(chan int, numJobs)  // バッファ指定なくすとdeadlock

    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }
	// go func() {
    for j := 1; j <= jobNum; j++ {
        jobs <- j
    }
	// }
	fmt.Println("sleep...")
	time.Sleep(2 * time.Second)
	fmt.Println("sleep end")
    close(jobs)

    for a := 1; a <= jobNum; a++ {
		fmt.Println(<-results)
    }
}
// ★ バッファ指定なしの場合
// worker 3 started  job 1
// worker 1 started  job 2
// worker 2 started  job 3
// worker 1 finished job 2
// worker 1 started  job 4
// worker 2 finished job 3
// worker 2 started  job 5
// worker 3 finished job 1
// sleep...
// worker 1 finished job 4
// worker 2 finished job 5
// sleep end
// 4
// 6
// 2
// 8
// 10

// ★ バッファなしでも jobs <- j のループを別goroutineにすると以下
// sleep...
// worker 1 started  job 1
// worker 2 started  job 2
// worker 3 started  job 3
// worker 3 finished job 3
// worker 3 started  job 4
// worker 2 finished job 2
// worker 2 started  job 5
// worker 1 finished job 1
// sleep end
// 6
// 4
// 2
// worker 3 finished job 4
// 8
// worker 2 finished job 5
// 10

// ★ バッファ指定ありの場合
// sleep...
// worker 1 started  job 1
// worker 2 started  job 2
// worker 3 started  job 3
// worker 3 finished job 3
// worker 3 started  job 4
// worker 1 finished job 1
// worker 1 started  job 5
// worker 2 finished job 2
// worker 1 finished job 5
// worker 3 finished job 4
// sleep end
// 6
// 2
// 4
// worker 1 finished job 5
// 10
// worker 2 finished job 4
// 8
```

- バッファ指定ありの場合は、待ち受け？ バッファが空だからブロック、送信されたものを worker が受け取るまでのタイムラグ？の間に main の sleep 実行か？
- バッファ指定なしの場合は、即実行？ 送信側(main)と受信側の goroutine 揃うためブロックされず、worker が受け取ったら即実行
  - 送信側も goroutine にすると、起動のタイムラグで先に main の sleep 実行
- results をバッファ指定なしにした場合は、3 回送信時点で受信側がそれ以上取り出そうとし deadlock

## fan-out/fan-in

- ファンアウト：並列処理の起点となる１つのロジックから分岐。この分岐
- ファンイン：分岐の待ち合わせ

### sync.WaitGroup

- ファンアウト、ファンインの仕組みを提供
- 複数の goroutine を管理

メソッド：

- Add：タスク数登録
- Done：タスク完了
- Wait：タスク完了の待機

```go
func worker(id int) {
	fmt.Printf("Worker %d start\n", id)
	time.Sleep(time.Second)
	fmt.Printf("Worker %d end\n", id)
}

func main() {
    var wg sync.WaitGroup
    for i := 1; i <= 5; i++ {
        wg.Add(1)
        i := i
        go func() {
            defer wg.Done()
            worker(i)
        }()
    }
    wg.Wait()
}
```

Channel で同様にデータの受け渡しが可能

```golang
func responseSize(wg *sync.WaitGroup, url string, nums chan int) {
	defer wg.Done()
	response, err := http.Get(url)
	if err != nil {
		log.Fatal(err)
	}
	defer response.Body.Close()
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		log.Fatal(err)
	}
	nums <- len(body)
}

func main() {
	wg := new(sync.WaitGroup)
	nums := make(chan int)
	wg.Add(1)
	go responseSize(wg, "https://www.example.com", nums)
	fmt.Println(<-nums)
	wg.Wait()
	close(nums)
}
```

### errorgroup.Group

- 基本形

```golang
func main() {
	var eg errgroup.Group
	for i := 1; i <= 5; i++ {
		id := i
		eg.Go(func() error {
			worker(id)
			return nil
		})
	}

	if err := eg.Wait(); err != nil {
		fmt.Println("error: ", err)
	}
}
```

- エラーが発生したときに後続の Goroutine をキャンセルする（context）

```golang
func main() {
	eg, ctx := errgroup.WithContext(context.Background())

	for i := 0; i < 100; i++ {
		i := i
		eg.Go(func() error {
			time.Sleep(2 * time.Second) // 長い処理

			select {
			case <-ctx.Done():
				fmt.Println("Canceled:", i)
				return nil
			default:
				if i > 90 {
					fmt.Println("Error:", i)
					return fmt.Errorf("Error: %d", i)
				}
				fmt.Println("End:", i)
				return nil
			}
		})
	}
	if err := eg.Wait(); err != nil {
		log.Fatal(err)
	}
}
```

# refs

良き Example

- [Go by Example](https://gobyexample.com/)

Groutine/Channel

- [Go の goroutine, channel をちょっと攻略！](https://qiita.com/taigamikami/items/fc798cdd6a4eaf9a7d5e)
- [Goroutine と Channel](https://zenn.dev/mikankitten/articles/6344d71f4f4920)
- [[Go 言語]Channel を使い倒そうぜ！](https://selfnote.work/20201110/programming/how-to-use-channel-on-golang/)

WaitGroup/ErrGroup

- [複数の Goroutine を WaitGroup（ErrGroup）で制御する](https://blog.toshimaru.net/goroutine-with-waitgroup/)
- [Catch values from Goroutines](https://www.golangprograms.com/catch-return-values-from-goroutines.html)

golang 並列処理のはまりどころ

- [errgroup のはまりどころと回避策](https://zenn.dev/ikawaha/articles/20211218-f37638b56e5807)

詳細な解説

- [Go での並列処理を徹底解剖！](https://zenn.dev/hsaki/books/golang-concurrency/viewer/basicusage)

Concurrency Patterns

- [Go Concurrency Patterns: Pipelines and cancellation](https://go.dev/blog/pipelines)
- [Go Concurrency Patterns](https://talks.golang.org/2012/concurrency.slide)
- [Addvanced Go Concurrency Patterns](https://talks.golang.org/2013/advconc.slide)
