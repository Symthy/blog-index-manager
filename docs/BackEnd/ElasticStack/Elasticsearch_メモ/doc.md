# Elasticsearch メモ

## 概要

- Elastic Stack の 1製品
- JSONベースの高速検索を可能とする検索・分析エンジン

用途: ブログ/記事投稿サイト等のWebサービスの全文検索＋α？に使われている模様

メモ：
- RDBに被せて使える物でもなく、利用するなら併用する形式
- RDBとは別サーバリソースが必要
- RDBのデータをElasticsearchに同期的に投入する必要がある

## RDBの代替にはならない



Elasticsearchのデータストアとしての振舞いの特徴

- ドキュメント型データベース
- スケーラブル
- トランザクションがない
- 結合は不得手

大量の文書を高速に検索することに適した仕組みを活かして、限定的に使用するのが良い

- RDBと比べてのデメリット
    - 学習コスト
    - 別のサーバーリソースを要する
    - 正規化できない、トランザクションがない

Elasticsearchは速度改善だけで選ぶものではない

- Elasticsearchにマッチする要件
    - 自然言語で記述された大量の文書データに対し、より文章として自然な検索結果を得たい
    - 検索キーワードを基にあいまいな検索結果を得たい
    - 肥大化するデータに対し、動的にクラスタ構成をスケーリングしたい

上記はRDBでは対応が難しい場合が多く、文章の検索に特化したElasticsearchならではの活用範囲

## ref

[Elasticsearch 入門。その１](https://dev.classmethod.jp/articles/elasticsearch-starter-1/)

[MySQL(Replication Protocol)とElasticsearchのほぼリアルタイム連携の実現（リアルタイム・インデクシング）](https://qiita.com/mokoenator/items/05b23af7321cfab95198)

[大量データを検索するサービスでElasticsearchはRDBの代替候補になりうるか？(Elasticsearch vs pg_bigm)](https://tech-blog.rakus.co.jp/entry/20190927/kamisen)
※連載