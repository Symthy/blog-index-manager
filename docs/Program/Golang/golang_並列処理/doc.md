# golang 並列処理

Goの魅力

- 他の言語は後から並列処理の機構を組み込むと大手術になることがあるが、Goは容易
- 高水準のパフォーマンスが出るコードを少ない手間で実現できるところ
- I/Oコストが高い領域はGoとの相性が良い

Goの業務アプリケーションで並列処理の適用を検討すべき場面は、1リクエスト/バッチタスクの内部を高速化したい時。（例：１リクエスト中で複数データストアから情報取得し、結果を複数箇所に格納が必要な時）

## Gorutine

- 個々のgoroutineは識別不可
- 優先度や親子関係はない
- 外部から終了させられない
- 終了検知には別の仕組みが必要（channel?)
- かなり少ない量のメモリしか要求せず、起動は高速
  - 起動コストはゼロではない

goroutineの乱用は避ける

- 並列処理は複雑さと高める
- goroutineを駆使したコードは意図が伝わりにくい
- 基本的には標準/準標準パッケージ機能の利用を検討

```go
func main() {
	go output("goroutine")

	go func(msg string) {
		fmt.Println(msg)
	}("immediate execution")
}
```

## Channel

- 同時実行するgoroutineを接続するパイプ（複数のgoroutineから送受信しても安全が保障されたキュー）
- Channelは同期の手段
  - Channelはgoroutineをブロックする
  - 送信goroutineと受信goroutineが揃うまでブロック（バッファなしの場合)
  - 送信側のバッファ一杯になると受信側が取りに来るまで or バッファが空ならブロック（バッファありの場合）

※ブロック＝待ち受け

```go
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

```go
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

```go
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

- 複数goroutineの待ち受け可
- 先に終わったものから捌く

```go
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

```go
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

- バッファなしchannelのため最初からブロック
- `<-readCh` : Channelから値読み込みを永遠に待ち続ける = 値書き込みがなければ永続待機 = deadlock発生

```go
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

```go

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

(チャネル受信待ちなど) ブロック中のgoroutineを解放

```go
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

クローズすることで、rangeを用いてchannelから取り出すことができる

※クローズしなければ受信待ちによるブロックでdeadlock

```go
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

```go
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

- バッファ指定ありの場合は、待ち受け？ バッファが空だからブロック、送信されたものをworkerが受け取るまでのタイムラグ？の間にmainのsleep実行か？
- バッファ指定なしの場合は、即実行？ 送信側(main)と受信側のgoroutine揃うためブロックされず、workerが受け取ったら即実行
  - 送信側もgoroutineにすると、起動のタイムラグで先にmainのsleep実行
- results をバッファ指定なしにした場合は、3回送信時点で受信側がそれ以上取り出そうとしdeadlock

## fan-out/fan-in

- ファンアウト：並列処理の起点となる１つのロジックから分岐。この分岐
- ファンイン：分岐の待ち合わせ

### sync.WaitGroup

- ファンアウト、ファンインの仕組みを提供
- 複数のgoroutineを管理

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

### errorgroup.Group

```go
func main() {
	// eg, ctx := errgroup.WithContext(ctx)
	var eg errgroup.Group
	for i := 1; i <= 5; i++ {
		id := i
		eg.Go(func() error {
			worker(id)
			return nil
		})
	}
	err := eg.Wait()
	if err != nil {
		fmt.Println("error: ", err)
	}
}
```


# refs

[Goのgoroutine, channelをちょっと攻略！](https://qiita.com/taigamikami/items/fc798cdd6a4eaf9a7d5e)

[Go by Example](https://gobyexample.com/)

[GoroutineとChannel](https://zenn.dev/mikankitten/articles/6344d71f4f4920)

[Goでの並列処理を徹底解剖！](https://zenn.dev/hsaki/books/golang-concurrency/viewer/basicusage)

[[Go言語]Channelを使い倒そうぜ！](https://selfnote.work/20201110/programming/how-to-use-channel-on-golang/)

[Go Concurrency Patterns: Pipelines and cancellation](https://go.dev/blog/pipelines)

[Go Concurrency Patterns](https://talks.golang.org/2012/concurrency.slide)

[Addvanced Go Concurrency Patterns](https://talks.golang.org/2013/advconc.slide)