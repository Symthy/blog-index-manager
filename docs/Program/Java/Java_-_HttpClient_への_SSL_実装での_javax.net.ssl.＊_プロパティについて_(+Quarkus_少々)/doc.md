# Java - HttpClient への SSL 実装での javax.net.ssl.\* プロパティについて (+Quarkus 少々)

## 前提知識メモ

- トラストストア

  - 自らが信頼する CA（Certificate Authority:認証局）のルート証明書または中間証明書を保存する場所（ファイル）。
  - クライアント側が認証するサーバー側の証明書を格納するファイル？
  - (トラストストアを持つ側＝クライアントが SSL 接続を行い)、SSL の通信先がサーバー証明書を送信してきた際に、トラストストアに保存されている証明書によって署名がなされているかどうかによって認証の可否を判断。

- キーストア
  - 自らのサーバー証明書を保存する場所
  - サーバーに送信するクライアントの証明書を格納するファイル
  - KS（Java Key Store）の場合、サーバー証明書をインストールする前に、その上位のルート証明書・中間証明書も共にインストールする必要がある。これにより証明書のチェーン（ルート証明書、中間証明書、サーバー証明書の連鎖）を SSL の通信先に送信する事が可能になる

ref: [Java の SSLSocket で SSL クライアントと SSL サーバーを実装する](https://codezine.jp/article/detail/105)

以下、簡単な実装例（トラストストア、キーストアのパスは直指定）

ref: [【Java】SSL 通信を実装する](https://ohs30359.hatenablog.com/entry/2016/07/16/174029)

## javax.net.ssl に関して

■ javax.net.ssl.SSLContext

SSLSocketFactory.getDefault () で使用される SSLContext と SSLContext.getDefault()で得られる SSLContext には、以下のシステムプロパティが影響する (※SSLContext.setContext()が行われた倍は除く)

- javax.net.ssl.keyStore
- javax.net.ssl.keyStorePassword
- javax.net.ssl.trustStore
- javax.net.ssl.trustStorePassword

ref: [Get SSLContext for default system truststore in Java(JSEE) - StackOverflow](https://stackoverflow.com/questions/30519267/get-sslcontext-for-default-system-truststore-in-javajsee)

■ javax.net.ssl.TrustManagerFactory & javax.net.ssl.X509TrustManager

> 注: null の KeyStore パラメータが SunJSSE の「PKIX」または「SunX509」TrustManagerFactory に渡される場合、ファクトリは次の手順でトラストデータを検索します。
>
> 1. システムプロパティ javax.net.ssl.trustStore が定義されている場合、TrustManagerFactory は、このシステムプロパティーで指定したファイル名を使ってファイルを検索し、このファイルをキーストアで使用

refs:

- https://docs.oracle.com/javase/jp/7/technotes/guides/security/jsse/JSSERefGuide.html#X509TrustManager
- https://docs.oracle.com/javase/jp/8/docs/technotes/guides/security/jsse/JSSERefGuide.html#X509TrustManager

ドキュメントの日本がおかしく正確なところは分からないが、恐らく TrustManagerFactory.getInstance() でアルゴリズムに「PKIX」または「SunX509」を指定した場合、`javax.net.ssl.trustStore` 等のシステムプロパティが指定されていればそれを優先して使用されると思われる

また、以下の通り

> デフォルトのトラストマネージャーのアルゴリズムは「PKIX」です。

デフォルトアルゴリズムは「PKIX」と思われるため `TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm())` で取得した TrustManagerFactory には`javax.net.ssl.trustStore` 等が適用されると思われる

## HTTP Client ライブラリ編

Java の HTTP Client はいくつかあるが、今回は google-client-java-api を見ていく（理由は特にない。業務で使われていたため）

■ google-client-java-api

サンプル

```java
SSLFactory sslFactory = SSLFactory.builder()
    .withIdentityMaterial("identity.jks", "password".toCharArray())
    .withTrustMaterial("truststore.jks", "password".toCharArray())
    .build();
NetHttpTransport httpTransport = new NetHttpTransport.Builder()
    .setSslSocketFactory(sslFactory.getSslSocketFactory())
    .setHostnameVerifier(sslFactory.getHostnameVerifier())
    .build();

// ref: https://sslcontext-kickstart.com/client/google.html
```

HttpTransport にはいくつか種類がある。

- NetHttpTransport：JDK の HttpURLConnection がベース　（今回はこちらを見る）
- ApacheHttpTransport：Apache HttpClient がベース
- 他にもいくつか

[NetHttpTransport.Builder](https://github.com/googleapis/google-http-java-client/blob/5ddb634887601bfad64ac482643f65c820b55fd4/google-http-client/src/main/java/com/google/api/client/http/javanet/NetHttpTransport.java#L187) を使用して証明書を設定できるようである。

特になにもセットしなければ、sslSocketFactory, hostnameVerifier は null となる。これらは null でなければ [NetHttpTransport.buildRequest](https://github.com/googleapis/google-http-java-client/blob/main/google-http-client/src/main/java/com/google/api/client/http/javanet/NetHttpTransport.java#L161) で、HttpURLConnection (https の場合は HttpsURLConnection) にセットされる。

[javax.net.ssl.HttpsURLConnection](https://docs.oracle.com/javase/jp/8/docs/api/javax/net/ssl/HttpsURLConnection.htm) に関しては以下の通り

> このクラスでは、HostnameVerifier と SSLSocketFactory を使用します。どちらのクラスにも、デフォルトの実装が定義されています。
> これらの実装は、クラスごと(static)またはインスタンスごとに置き換えることもできます。すべての新しい HttpsURLConnection のインスタンスには、生成時にデフォルトの static 値が割り当てられます。

SSLSocketFactory のデフォルトは、以下で取得できるものと思われる

[javax.net.ssl.SSLSocketFactory.getDefault()](https://docs.oracle.com/javase/jp/8/docs/api/javax/net/ssl/SSLSocketFactory.html) に関しては以下の通り

> このメソッドがはじめて呼び出されると、セキュリティ・プロパティ ssl.SocketFactory.provider が検査されます。null 以外の場合、その名前のクラスがロードされ、インスタンス化されます。
> それ以外の場合、このメソッドは SSLContext.getDefault().getSocketFactory()を返します。この呼出しに失敗した場合は、使用できないファクトリが返されます。

SSLContext.getDefault() は、前述の通り javax.net.ssl.\* システムプロパティが影響すると思われるため

NetHttpTransport.Builder に何もセットせず、すぐさま build() して得られる NetHttpTransport から生成する HttpRequest (HttpsURLConnection を保持) には、javax.net.ssl.\* のシステムプロパティが適用されると思われる。

※推測の域を出ないため要確認

■ 蛇足：Apache HttpComponents HttpClient

ちょっと参考になりそうなのを見つけたためリンクのみ添付

- [Java 日記～ Apache HttpComponents でクライアント認証～](https://www.cresco.co.jp/blog/entry/1032/))
- [Java 日記～ Apache HttpComponents でクライアント認証 ② ～](https://www.cresco.co.jp/blog/entry/1356/)

## Quarkus についてメモ

本件に関して調べ始めた発端。

Quarkus アプリケーション内 から 外部の HTTPS リソースにアクセスする場合は、以下等の quarkus のプロパティ(application.conf) は効かない

- quarkus.http.ssl.certificate.key-store-file
- quarkus.http.ssl.certificate.key-store-password
- quarkus.http.ssl.certificate.trust-store-file
- quarkus.http.ssl.certificate.trust-store-password

これらはあくまで、SSL を使用して Quarkus アプリケーション (サーバ) を公開する際に使用するためのプロパティ (ブラウザ等から Quarkus アプリケーションにアクセスする際に使用されるもの)

ref: [プロパティ quarkus.http.ssl.certificate.key-store-file が機能せず、要求されたターゲットへの有効な証明書パスが見つからない](https://stackoverflow.com/questions/60771856/property-quarkus-http-ssl-certificate-key-store-file-not-working-with-unable-to)

故に、実行時に javax.net.ssl.\* のシステムプロパティでトラストストア等を適用する必要がありそう。 ※それでもダメだった場合はソース上でトラストストア等を直接読み込んで、上記で触れた google-client-java-api では NetHttpTransport.Builder にセットすれば適用できそう。

また、認証局に OpenID Connect の認証を行うための仕組みが用意されており、OpenID Connect 時に使用する証明書を指定するためのプロパティが上記とは別に用意されている。

[OPENID CONNECT (OIDC) AUTHORIZATION CODE FLOW MECHANISM](https://quarkus.io/guides/security-openid-connect-web-authentication)

## さいごに

SSL の実装を行ったことがこれまでなく、参考になりそうなとあるサービスのコードを見ていて、証明書検証有効時には特に証明書を読み込むような処理もなく、無効時には https://gist.github.com/kazuhira-r/bb3ca27bc6194ff4900e のような実質検証を行わないような実装となっており、Why? というところからスタートしてからここまで調べ、恐らく javax.net.ssl.truststore 等で証明書適用できる、できなかった場合の代替案としてどういう風にすれば適用できるかまで見れたのでひとまず良しとする。

推測があっていたかは後日追記するかもしれない。
