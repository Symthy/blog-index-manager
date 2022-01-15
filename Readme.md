# My Document & Blog Entry Manager

個人のドキュメント＆ブログ管理ツール

## The requirements that we wanted to achieve with this tool

- 記事(Markdownファイル)を書くことに集中したい
    - ドキュメント整理に労力を割きたくない -> ツールが自動で整理してくれる
    - 1ウィンドウで全て完結する（例えばVSCodeのみの操作で済む) -> CLI操作
- 記事原本は全てローカルで管理したい
    - カテゴリ毎に記事を振り分けて保持できる
    - 作成済み記事の(最低限の)検索ができる
    - 指定した記事をはてなブログへ投稿できる（画像付きでも可能）
    - ブログへ投稿済みの記事かどうか管理できる
    - 全記事一覧(Summary)を目次の形で自動生成できる（ローカル/ブログ共に）

## Tool introduction

### initialize settings

必要があれば、以下定義(Category Group 定義)を編集

- tools/definitions/category_group.yml

以下を実行

```shell
initialize.sh
```

以下を編集

- conf/blog.conf

### Detail description

※開発中 by Python3 (動確不十分のためバグがある可能性有)

#### 動作環境

- python3 (3.9以上推奨。3.9未満は動作保証しません)
    - 必要ライブラリ：準備中
- Linux OS / WindowsはGit Bash

#### 記事管理基本方針:

- 1フォルダ = 1記事
    - 1フォルダには1つのmdファイルまで (複数ある場合は動作を保証しない)
- 各記事にカテゴリ付与可能
    - mdファイルの先頭行は必ず "# ～" とする。 "～" の部分を記事タイトルとして扱う
    - フォルダ内の category.txt に記事に付与するカテゴリ名を記載要
    - 複数書く場合は1行1カテゴリで記載要
- 各記事のカテゴリ(先頭1つ)を元に定義(category_group.yml)に従ってグルーピング
    - 定義にないカテゴリorカテゴリ未設定のものは Others に紐づけ
    - グルーピングの結果は常にSUMMARY.mdに出力

#### フォルダ構成:

- docs: 作成した記事全てを管理するフォルダ（※フォルダ内直接編集非推奨/削除厳禁）
- work: 編集中の記事を格納するフォルダ（作成済み記事もコマンドにてこちらに取り出し編集要）
- backup: 取り出し中の記事のバックアップフォルダ（※削除厳禁）
- tools: ツール本体（※削除厳禁）

#### 用語

- Entry: 1記事の事を指します
    - Blog Entry:  ブログ記事を指します
    - Doc Entry:   ローカルで管理する記事(mdファイル格納フォルダ)を指します
- document set: 1記事分のフォルダ及びフォルダに格納されるファイルセット

#### document set 構成

初期生成(-i, -init オプション)にてworkフォルダ直下に生成されるフォルダ

フォルダ名：初期生成時は現在時刻の数列（フォルダ名は変更可能）

- Doc.md: 記事本体（ファイル名は変更可能）
    - ファイル内の先頭行 "# ～" のうち "～" の部分を記事タイトルとして扱う
- category.txt: 記事に付与するカテゴリ用ファイル
- images: 記事に使用する画像を配置するためのフォルダ（ここに配置されなかったものは無効）
- .id_xxxxx: 内部的に付与するID

### Usage:

Todo: 日本語でも書きます

```
Document and Blog Entry Manager

USAGE:
  run.sh [OPTIONS]

OPTIONS:
  -i, -init                            initialize docs directory (don't delete exist file and dir).
  -n, -new [<OPTS>]                    new document set under "work" dir (create dir, md file and category file).
    OPTS (can also specify the following together):                                
      -t, -title <DocTitle>              specified document title (default: "Document").
      -c, -category <CategoryName>       specified category (default: empty value).
  -s, -search <Keyword>                specifiable keyword: Group Name, Category Name, Title Keyword(partial match).
  -p, -push [<OPTS>] <DirName>         push document set from "work" dir to "docs" dir.
    OPTS: -a, -all                       in addition to the above, post your blog.
  -r, -retrieve [<OPTS>] <DocEntryID>  retrieve document set from "docs" dir to "work" dir (and backup).
    OPTS: -c, -cancel                    cancel retrieve (move the backup back to "docs" dir).
  -b, -blog <OPTS>                     operation to your blog.
    OPTS (can't also specify the following together):                                
      -c, -collect                       collect all blog entries from your blog. 
      -p, -push <DocEntryID>             post specified document to your blog.
  -h, -help                            show usage.
```

開発メモ

- 某ブログより最新記事取得し管理用データを更新: 済
- 某ブログに用意するIndexページの更新(投稿): 済
- 指定したmdの投稿(新規/更新)＆ダンプデータに追加登録: 動確
    - 文章のみの記事投稿実行: 済
    - 画像の自動登録＆本文自動置換して投稿実行: 動確
    - 投稿済みローカルリストに追加: 動確
- ローカルmdファイル初期セットの自動作成: 済
- ローカルmdファイルセットの自動配置 (work -> docs): 済
    - フォルダ移動＆フォルダ名をタイトルに変更: 済
    - 管理用データへの登録/更新: 済
    - 各データのダンプ: 済
- docsを元にSUMMARY.md(GitBook用)の自動更新: 済
- docsからworkへの取り出し(&backup): 動確
    - id指定: 動確
    - title指定: 保留
    - キャンセル(backupから戻す): 動確
- document検索＆コンソール出力: 動確
    - group指定: 動確
    - category指定: 動確
    - title指定: 動確
- docsから管理用データ更新: 保留
- コマンドオプションとreadme.mdの整備: 済

※ ひとまずローカル -> 某ブログへの一方通行

追加機能メモ

- push時、id指定
- push時、指定directory存在チェック
- docs フォルダからダンプデータ更新

## used third party tools

- GitBook (予定)