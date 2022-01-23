# Git 追跡解除

## ローカルでのみ追跡を止める

assume-unchanged の変更は git reset --hard で消えるので, 基本的には skip-worktree を使うと良い

```shell
# 除外する
git update-index --skip-worktree path/to/file
# 除外をやめる
git update-index --no-skip-worktree path/to/file
# 確認
git ls-files -v | grep ^S
```

[git の監視から逃れる方法](https://qiita.com/sqrtxx/items/38a506e59df67cd5d3a1)

## ファイルを管理対象から外して追跡を完全いやめる

```
# .gitignore
/file_name.txt
```

```shell
git rm --cached file_name.txt
```

[gitで、追跡対象ファイルの外す（追跡をやめる）方法](https://www-creators.com/archives/1748#2)