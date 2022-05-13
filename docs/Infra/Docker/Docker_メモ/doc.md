# Docker メモ

## 基本コマンド

dockerコマンド

```sh
docker build <image> -f <Dockerfile Path> -t <name>

docker run <image> # image build, container build & run
docker run -d -t -v <mount> --rm --name <container> <image> <args>

docker ps

docker exec <container> <command>
docker exec -it product_web_1 bash

docker stop <container>
```

docker-composeコマンド

```sh
docker-compose build  # image build

docker-compose up  # container build & run
docker-compose up --build  # imageをbuildしてrun
docker-compose up -d  # detachedモード(バックグラウンド実行)

docker-compose ps

docker-compose exec <service> <command>
docker-compose exec web bash  # コンテナに入る

docker-compose down  # stopしてrm
```

停止しているコンテナ削除

```shell
docker system prune
```

## ENTRYPOINT & CMD

ENTRYPOINTを使うことで、Dockerコンテナをコマンドのようにすることができる

- ENTRYPOINT：コンテナ実行時に必ず実行するコマンド
- CMD：コンテナ実行時にデフォルトで実行するコマンド。上書き可

両方指定の場合は、ENTRYPOINTは固定部、CMDは変更可部分(引数で上書き)となる

詳細: [(Docker) CMDとENTRYPOINTの「役割」と「違い」を解説](https://hara-chan.com/it/infrastructure/docker-cmd-entrypoint-difference)

## ベストプラクティス

## ベストプラクティス

- １つのコンテナには１つのアプリケーション
- Docker ImageのLayer数は最小限にする
- Layerを作るのは、RUN、COPY、ADDの３つ
- コマンドは && で繋げるべし
- バックスラッシュ(\)で改行する
- Dockerfileを作る時は、キャッシュをうまく活用する
- CMDは Layerを作らない
- build context （ワークディレクトリのようなもの）に余計なファイルは置かない
- COPY / ADD の使い分け
    - COPY：単純にファイルやフォルダをコピーする場合に使用
    - ADD：tarの圧縮ファイルをコピーして回答したい時に使用

## Link Stack

随時、有益な物を追加

[実践 Docker - ソフトウェアエンジニアの「Docker よくわからない」を終わりにする本](https://zenn.dev/suzuki_hoge/books/2022-03-docker-practice-8ae36c33424b59)