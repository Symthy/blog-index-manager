# golang で windows サービス を開発する

## 前置き

golange で開発し、ビルドして生成した exe ファイルは、そのままでは

sc や [NSSM (the Non-Sucking Service Manager)](http://nssm.cc/) では、Windows サービス化はできても、起動ができない。

以下によると、[kardianos/service](https://github.com/percona/kardianos-service) を使えばよいとのこと。

[Cannot start a Go application exe as a windows services](https://stackoverflow.com/questions/35605238/cannot-start-a-go-application-exe-as-a-windows-services?newreg=af7591295de54a9d9525272feac3c9e9&answertab=createdasc#tab-top)

[Windows サービスとして golang アプリケーション exe を起動できません](https://www.web-dev-qa-db-ja.com/ja/windows/windows%E3%82%B5%E3%83%BC%E3%83%93%E3%82%B9%E3%81%A8%E3%81%97%E3%81%A6golang%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3exe%E3%82%92%E8%B5%B7%E5%8B%95%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%9B%E3%82%93/823916534/amp/)

詳細な理由までは分かっていないが、windows サービス化するためには、それに必要な処理が実装されている必要があるらしい。

ref: [エラー 1053：カスタムサービスが開始されません](https://answers.microsoft.com/en-us/windows/forum/all/error-1053-custom-service-does-not-start/810fcf93-0cca-43cd-9e71-9050e7ee80ed)

golang には、windows サービス化 に必要となる処理も含む準標準ライブラリ（golang.org/x/sys）があり、ご丁寧にサンプルコードもある（https://pkg.go.dev/golang.org/x/sys@v0.0.0-20220702020025-31831981b65f/windows/svc/example）

## kardianos/service とは

[kardianos/service](https://github.com/percona/kardianos-service) は windows の処理に関しては上記ライブラリを使用しつつ、win, linux, 等でサービス化を可能とするための共通のインターフェースを提供している。

- OS 毎にサービス化するために必要な制御は異なる（特に Windows は大きく異なる）が、その制御処理は、kardianos/service に実装されており
  共通のインターフェース (Service interface) を提供している。

https://github.com/percona/kardianos-service/blob/master/service.go#L292

- Service interface を実装する windows 向けの service struct があるため、コンストラクタ(New 関数) に Start(), Stop() を実装したものを渡せばよい

https://github.com/percona/kardianos-service/blob/master/service_windows.go

- コマンドライン引数はデフォルトで６つ用意してある。 install/unistall で Windows のサービス作成/削除ができ、Start/Stop で サービスの起動/停止ができる。

https://github.com/percona/kardianos-service/blob/master/service.go#L335

## ソース

ログファイルへの出力も可能か試したが、可能であった

https://github.com/Symthy/golang-practices/tree/main/go-win-service

# refs

- kardianos/service 使用サンプル

[Go 言語で Windows の Service を作成する](https://qiita.com/mako2kano/items/70e893b6c0fe178d5239) 2018/06

[Go 言語で Windows,Linux の常駐システムを開発する](https://tech-blog.optim.co.jp/entry/2022/04/28/100000)

[go で Windows service を作成する](https://qiita.com/yamasaki-masahide/items/c60e49a908c7927ca600) 2014/12

- その他

[Go 言語 - Windows 上でのプロセス存在チェック](https://blog.y-yuki.net/entry/2018/08/03/000000)
