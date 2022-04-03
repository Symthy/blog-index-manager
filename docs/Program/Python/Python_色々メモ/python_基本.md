# Python 色々メモ

某ツール作成時に使った物をメモ（毎度期間が空いて綺麗さっぱり忘れてはググりまくるため）

## reference stack

[python 色々まとめ](https://note.nkmk.me/python/)

[ArgumentParserを使ってpythonのコマンドライン引数をとことん使ってみた](https://qiita.com/mimitaro/items/a845b45df35b39a59c95)

[Pythonでクラスの引数や戻り値の型アノテーションに自己のクラスを指定する](https://qiita.com/MtDeity/items/fa6cfc4fff8f58140caa)

```python
# これのみでいけた
from __future__ import annotations
```

[[Python] インスタンスのプロパティへ動的にアクセスする](https://www.yoheim.net/blog.php?q=20161002)

```python
c = Container()

setattr(c, "key", "value")
print(c.key)  # => value

val = getattr(c, "key")
print(val)  # => value
```

---

### date 系

[Python日付型](https://qiita.com/motoki1990/items/8275dbe02d5fd5fa6d2d)

[Pythonで日付文字列からのdatetime変換やタイムゾーンの変更などをいい加減覚えたい](https://www.soudegesu.com/python/python-datetime)

[Pythonで文字列 <-> 日付(date, datetime) の変換](https://qiita.com/shibainurou/items/0b0f8b0233c45fc163cd)

```python
from datetime import datetime as dt

# 文字列 → 日時
tstr = '2012-12-29 13:49:37'
tdatetime = dt.strptime(tstr, '%Y-%m-%d %H:%M:%S')

# 日時 → 文字列
tdatetime = dt.now()
tstr = tdatetime.strftime('%Y/%m/%d %H:%M:%S')
```

---

### 文字列系

[Pythonで文字列を比較（完全一致、部分一致、大小関係など）](https://note.nkmk.me/python-str-compare/)

[Pythonの文字列フォーマット（formatメソッドの使い方）](https://gammasoft.jp/blog/python-string-format/)

[Pythonのf文字列の使い方](https://gammasoft.jp/blog/python-f-string/)

```python
# 書式設定 (インデックス番号は省略可)
"{0:<20,.3f}".format(12345.67)  # '12,345.670'        
"{:<20,.3f}".format(12345.67)  # '12,345.670'

# int型：左に空白
"{:2d}".format(100)  # '100'
"{:10d}".format(100)  # '       100'
# ゼロパティング
"{:010d}".format(100)  # '0000000100'
# 小数点以下
"{:.1f}".format(0.01)  # '0.0'
"{:.2f}".format(0.01)  # '0.01'
"{:.5f}".format(0.01)  # '0.01000'
# 指数表記
"{:.1e}".format(0.01)  # '1.0e-02'
"{:.2e}".format(0.01)  # '1.00e-02'
"{:.5e}".format(0.01)  # '1.00000e-02'
"{:.5E}".format(0.01)  # '1.00000E-02'

# str型：右に空白
"{:2}".format("abcde")  # 'abcde'
"{:10}".format("abcde")  # 'abcde     '
# 右寄せ
"{:>20}".format("abcde")  # '               abcde'
"{:*>20}".format("abcde")  # '***************abcde'
# 最大文字数指定
"{:.3}".format("abcde")  # 'abc'
"{:.7}".format("abcde")  # 'abcde'
```

[Pythonで文字列を置換（replace, translate, re.sub, re.subn）](https://note.nkmk.me/python-str-replace-translate-re-sub/)

```python
# 複数の文字を指定して置換
s = 'one two one two one'
print(s.translate(str.maketrans({'o': 'XXX', 't': None})))
# XXXne wXXX XXXne wXXX XXXne
```

[Pythonで文字列の先頭と末尾から空白や文字列を削除する：strip()](https://uxmilk.jp/12804)

```python
# 先頭/末尾削除
"Hello World World Hello".strip('Hello')  # " World World "
# 先頭/末尾の空白/改行削除
s = "  Hello World\n".strip()  # "Hello World"
# 先頭のみ削除
s = "  Hello World\n".lstrip()  # "Hello World\n"
# 末尾のみ削除
s = "  Hello World\n".rstrip()  # "  Hello World"
```

---

### List

[Pythonでリストをソートするsortとsortedの違い](https://note.nkmk.me/python-list-sort-sorted/)

---

### Dictionary

[Pythonで辞書のキー・値の存在を確認、取得（検索）](https://note.nkmk.me/python-dict-in-values-items/)

[Pythonで辞書を作成するdict()と波括弧、辞書内包表記](https://note.nkmk.me/python-dict-create/)

```python
# 辞書内包表記
l = ['Alice', 'Bob', 'Charlie']
d = {s: len(s) for s in l}
```

[Pythonで辞書に要素を追加、辞書同士を連結（結合）](https://note.nkmk.me/python-dict-add-update/)

```python
d1 = {'k1': 1, 'k2': 2}
d2 = {'k1': 10, 'k3': 3, 'k4': 4}
# 別オブジェクトで生成
d = d1 | d2  # {'k1': 10, 'k2': 2, 'k3': 3, 'k4': 4}
# 上書き
d1 |= d2  # {'k1': 10, 'k2': 2, 'k3': 3, 'k4': 4}
```

---

### ファイル系

[[Python] フォルダやファイルのコピー、移動、削除（shutilモジュール）](https://hibiki-press.tech/python/shutil_copy_move_rmtree/1305#toc4)

[Pythonでファイル・ディレクトリを削除するos.remove, shutil.rmtreeなど](https://note.nkmk.me/python-os-remove-rmdir-removedirs-shutil-rmtree/)

```python
import shutil

# フォルダ丸ごとコピー (既にフォルダがあると失敗)
shutil.copytree('./sample', './sample_backup')
# フォルダ丸ごと削除
shutil.rmtree()
```

[【Python】 フォルダ内の特定のファイルを取得する](https://ni4muraano.hatenablog.com/entry/2017/01/30/184606)

```python
# フォルダ内の特定ファイル名のみ取得
import os

files = os.listdir('Folder\\')
extension = '.txt'
text_files = [file for file in files if extension in file]
for file_name in text_files:
    print(file_name)
```

```python
# フォルダ内の特定ファイルフルパス取得
import glob

extension = '.txt'
text_files = glob.glob('Folder\\*' + extension)
for file_path in text_files:
    print(file_path)
```

[Pythonでファイルのタイムスタンプ（作成日時や更新日時）を取得](https://note.nkmk.me/python-os-stat-file-timestamp/)

```python
# 最終アクセス日時
print(os.path.getatime('/temp/test.txt'))
# = os.stat('temp/test.txt')).st_atime

# 最終内容更新日時
print(os.path.getmtime('/temp/test.txt'))
# = os.stat('temp/test.txt')).st_mtime

# メタデータの最終更新日時（UNIX） / 作成日時（Windows）
print(os.path.getctime('/temp/test.txt'))
# = os.stat('temp/test.txt')).st_ctime

# 作成日時（macOSを含むFreeBSD系の一部のUNIXのみ）
# os.stat('temp/test.txt')).st_birthtime
```

[PythonでWeb上の画像などのファイルをダウンロード（個別・一括）](https://note.nkmk.me/python-download-web-images/)

```python
import os
import urllib.error
import urllib.request


def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file, open(dst_path, 'wb') as local_file:
            local_file.write(web_file.read())
    except urllib.error.URLError as e:
        print(e)


def download_file_to_dir(url, dst_dir):
    download_file(url, os.path.join(dst_dir, os.path.basename(url)))


url = 'xxxxxx'
dst_dir = 'data/temp'
download_file_to_dir(url, dst_dir)
```

---

XML 操作系

[【Python】XMLのデータを読み取り・書き込みする(ElementTree)](https://pg-chain.com/python-xml-read-write)

[【Python】XMLを解析・読み取りする(ElementTree)](https://pg-chain.com/python-xml-elementtree)

[PythonでのXMLファイル操作例](https://qiita.com/sino20023/items/0314438d397240e56576)

[ElementTreeやlxmlで名前空間を含むXMLの要素を取得する](https://orangain.hatenablog.com/entry/namespaces-in-xpath)

---




