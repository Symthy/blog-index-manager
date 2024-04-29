開発停止、後継 → https://github.com/Symthy/obs-docs-blog-entries-manager

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

## Tool Summary

カテゴリとカテゴリグループの定義（category_group_def.yml）に基づいて、

作成したドキュメントをカテゴリ毎にフォルダに振り分けてローカル管理＆はてなブログに投稿可能なツール

## Tool introduction

required: Docker

### Initialize settings

以下定義(ドキュメントをツリー構造で管理する上での Group(親) と Category(子) の 定義)を編集

- conf/category_group.yml

以下を実行

```shell
./initialize.sh
```

以下に自身のはてなブログの情報を設定

- conf/blog.conf

※ SUMMARY_ENTRY_ID には サマリーページとする1記事のIDを設定

### How to run tool

```sh
./run.sh <option>
```

`<option>` に指定可能な物は、Usage参照

## Tool Detail description

created by Python3 (最低限動確済)

### 記事管理基本方針:

- 1フォルダ = 1記事
    - 1フォルダには1つのmdファイルまで (複数ある場合は動作を保証しない)
    - mdファイルの先頭行は必ず "# ～" とする。 "～" の部分を記事タイトルとして扱う
- 各記事にカテゴリ付与可能
    - フォルダ内の category.txt に記事に付与するカテゴリ名を記載要
    - 複数書く場合は1行1カテゴリで記載要
- 各記事のカテゴリ(先頭1つ)を元に定義(category_group.yml)に従ってグルーピング
    - 定義にないカテゴリorカテゴリ未設定のものは Others に紐づけ
    - グルーピングの結果は常にSUMMARY.mdに出力

※フォルダの移動等は原則本ツールのコマンド実行にて実施

### フォルダ構成:

- docs: 作成記事全管理用フォルダ。ドキュメントマスターフォルダ（※フォルダ内直接編集非推奨/削除厳禁）
- work: 編集中記事格納フォルダ（docs下作成済み記事もコマンドにてwork下に取り出し/編集要）
- backup: 取り出し中の記事のバックアップフォルダ（※削除厳禁）
- tools: ツール本体（※削除厳禁）

### 用語

- Entry: 1記事の事を指します
    - Blog Entry:  ブログ記事を指します
    - Doc Entry:   ローカルで管理する記事(mdファイル格納フォルダ)を指す
- document set: 1記事分のフォルダ及びフォルダに格納されるファイル一式を指す
    - 初期生成(-i, -init オプション)にてworkフォルダ直下に生成されるフォルダ（initialize.shで実行）
    - フォルダ名：初期生成時は現在時刻の数列。登録後は記事タイトルとなる。
        - doc.md: 記事本体（ファイル名は変更可能）
            - ファイル内の先頭行 "# ～" のうち "～" の部分を記事タイトルとして扱う
        - category.txt: 記事に付与するカテゴリ用ファイル
        - images: 記事に使用する画像を配置するためのフォルダ（ここに配置されなかったものは無効）
        - .id_xxxxx: 内部的に付与するID (-p, -push実行時に付与。削除厳禁)

### Usage:

```
Document and Blog Entry Manager

USAGE:
  <command> [OPTIONS]

OPTIONS:
  -i, --init                            initialize docs directory (don't delete exist file and dir).
  -n, --new [<OPTS>]                    new document set under "work" dir (create dir, md file and category file).
    OPTS (can also specify the following together):                                
      -t, --title <DocTitle>                specified document title (default: "doc").
      -c, --category <CategoryName>         specified category (default: empty value).
  -s, --search <OPTS>                   search document entry (show entry id, title, group, category).
    OPTS:
      -g, --group <Group Name>              search by group name.
      -c, --category <Category Name>        search by category name.
      -t, --title <Keyword>                 search by title keyword (partial match). 
  -p, --push [<OPTS>] <DirName>         push document set from "work" dir to "docs" dir.
    OPTS: 
      -a, --all                         in addition to the above, post your blog.
      -d, --draft                       post as draft entry.
      -pu,--pickup                      post as pickup entry.
      -te,--title-escape                escape the entry title.
  -r, --retrieve [<OPTS>] <DocEntryID>  retrieve document set from "docs" dir to "work" dir (and backup).
    OPTS: 
      -c, --cancel                      cancel retrieve (move the backup back to "docs" dir).
  -d, --docs <OPTS>
    OPTS (can't also specify the following together):
      -pu, --pickup <DocEntryID>            toggle on/off of pickup in specified entry.                
  -b, --blog <OPTS>                     operation to your blog.
    OPTS (can't also specify the following together):                                
      -p, --push <DocEntryID>               post specified document to your blog.
      -d, --draft                       post as draft entry.
      -pu,--pickup                      post as pickup entry.
      -te,--title-escape                escape the entry title.
  -bc,--blog-collect                    collect all blog entries from your blog. (experimental function)
  -h, --help                            show usage.
```

機能一覧

- -i ：初期処理実行。
    - tools/definitions/category_group.yml に基づき docsフォルダ下に各Groupのフォルダを作成 (既存は削除しない。追加のみ実施)。
- -n ：新規 document set 作成
    - オプションにて document のタイトルとカテゴリを指定可能。
    - workフォルダ下にフォルダ/ファイルを作成。
- -s ：docsフォルダに登録(push)済み document の検索。
    - グループ名(完全一致)、カテゴリ名(完全一致)、タイトル(部分一致) にて検索可能。
    - 検索結果は以下のように表示

```
Doc Entry ID    Doc Entry Title                  Group Name      Category Name   Blog Posted
--------------- -------------------------------- --------------- --------------- -----------
20220115152044  xxxxxxxxxxxxxxx                  Program         Python          False
```  

- -p ：workフォルダ下の指定した document set を docsフォルダに登録する
    - オプションにて、ブログへの同時投稿も可能
- -r ：docsフォルダに登録(push)済み documentを、workフォルダに取り出し
    - 一度登録したdocumentを編集する際に使用。取り出し前の状態をbackupに保存
    - 取り出し中をキャンセル可能 (キャンセル時はbackupを再登録)
- -b ：はてなブログへの操作
    - 既存記事の収集が可能（機能未実装につき、収集した記事をローカルに保存は未サポート）
    - 投稿済みdocumentは上書き投稿となる
    - 各documentにて使用している画像の投稿も可能

※ ひとまずローカル -> ブログへの一方通行

## used third party tools

候補

- HonBook
- [Obsidian](https://zenn.dev/usagizmo/articles/beb73159edbe68)
