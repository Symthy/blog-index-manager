# Golang ビルド制約使用時の golps に関する注意事項

## 前置き

プラットフォーム毎の処理を実装するときは、runtime.GOOS での判定は NG、 ビルド制約を使うのが吉

[Golang はどのようにクロスプラットフォームの開発とテストを簡素化するのか](https://qiita.com/KentOhwada_AlibabaCloudJapan/items/59c1053b3eec189318de#os%E3%81%A8%E3%82%A2%E3%83%BC%E3%82%AD%E3%83%86%E3%82%AF%E3%83%81%E3%83%A3)

## vscode + gopls で ビルド制約 を扱う

gopls では、ビルドタグを、2 つ以上同時には設定できない。

1 つしか設定できない＝ linux,windows 等複数プラットフォームに対する個別処理を実装する際には、随時 buildFlags を切り替えるしかなさそう。

ref: [x/tools/gopls: improve handling for build tags #29202](https://github.com/golang/go/issues/29202#issuecomment-1013455808)

なので、ワークスペースの設定ファイル作り、以下のように、buildFlags を windows, linux 切り替える shell 等 を用意して１コマンドで切り替えられるようにすれば、多少手間は省けるかと。

※ただし、ビルド制約を使用しているソースに関しては、例えば buildFlags を windows にしている時は それ以外のプラットフォーム用のソースで 警告かエラーが必ず出てしまう。 （そこに関しては妥協するしかないのだろうか…）

```shell
VSCODE_SETTINGS=".vscode/settings.json"
TAGS_WIN="\"-tags=windows\""
TAGS_LINUX="\"-tags=linux\""
REGEX_WIN=".*${TAGS_WIN}.*"
REGEX_LINUX=".*${TAGS_LINUX}.*"

build_flag_line=`grep "build.buildFlags" ${VSCODE_SETTINGS}`

if [[ ${build_flag_line} =~ ${REGEX_WIN} ]]; then
    echo "chage windows to linux"
    sed -i -e "s/${TAGS_WIN}/${TAGS_LINUX}/g" ${VSCODE_SETTINGS}
elif [[ ${build_flag_line} =~ ${REGEX_LINUX} ]]; then
    echo "change linux to windows"
    sed -i -e "s/${TAGS_LINUX}/${TAGS_WIN}/g" ${VSCODE_SETTINGS}
else
    echo "no change"
fi

cat ${VSCODE_SETTINGS}
```
