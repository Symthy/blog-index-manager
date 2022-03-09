# Golang Gorm 実践メモ＆注意点

随時追記

[公式ドキュメント]()https://gorm.io/ja_JP/docs/index.html

- Golang のデファクトスタンダード的ポジションのORM
- テーブルとオブジェクトの紐づけ。SQL実行。両方提供 = 単体でCORS実装可能

## 注意事項

1. Create、Update、Save の振舞いの違い

- Create: 新規作成
- Update: 空値が除外、任意のカラムのみ選択可能
- Save: 空値も含めて全てのカラムを一律保存

使い分けの方針

- 新規レコード作成時: Create
- 既存レコード更新時: Update
- 更新時に空値を含めてStructで更新: Save
- 更新時に空値を含めてMapで更新: Update

Saveは、なければ新規作成、あれば更新。となるため注意が必要

2. (コールバックで)自動的に関連レコードが全て保存される

関連レコード含めて全て更新される

回避： 関連レコードの一括保存や、そのほかBeforeCreateのようなコールバックメソッドを呼ばずに更新したい場合、 UpdateColumn、UpdateColumnsを使用

3. マイグレーション機能は本番向きでない

一回きりのマイグレーションで完結する場合は十分かもしれないが、長期的な運用の管理には機能不足

[migrate](https://github.com/golang-migrate/migrate) 等、別のツールを使う

4. Query Conditions関数は、必ずWhere() を使用して条件を指定

```golang
db.Where("id = ?", 1).Find(&users)
```

様々な書き方ができるように設計されているが

```golang
db.Where("id = ?", "1").Find(&users)
// SELECT * FROM `users`  WHERE (id = '1')
db.Where(User{ID: 1}).Find(&users)
// SELECT * FROM `users`  WHERE (`users`.`id` = 1)
db.Find(&users, "id = ?", "1")
// SELECT * FROM `users`  WHERE (id = '1')
db.Find(&users, User{ID: 1})
//  SELECT * FROM `users`  WHERE (`users`.`id` = 1)
db.Find(&users, "1")
// SELECT * FROM `users`  WHERE (`users`.`id` = '1') 
```

5番目の書き方トラップがあり、以下のように書くと任意のSQL実行できてしまう。

```golang
userInputID := "1=1"
db.Find(&users, userInputID)
// SELECT * FROM `users`  WHERE 1=1  ※全権取得になる

userInputID := "1=1);DROP table users;--"
db.Find(&users, userInputID)
// SELECT * FROM `users`  WHERE (1=1);DROP table users;--)  ※usersテーブル削除
```

## ref

- [Go言語のGormを実践投入する時に最低限知っておくべきことのまとめ](https://qiita.com/ttiger55/items/3606b8dd570637c12387)
- [Gormにおける「仕様通り」なSQLインジェクションの恐れのある実装についての注意喚起](https://tech.andpad.co.jp/entry/2022/02/18/140000)
