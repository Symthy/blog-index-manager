# コードレビュー どう取り組むか

言葉遣いで心掛けていること

- 上から目線、命令形は、ダメ絶対
    - なぜ悪いコードなのか、なぜそう書いた方がいいかまで説明を付ける
    - その上で、○○しませんか？(提案型)、or 明確にそうした方が良い時は○○しましょう(推奨型) でコメントを付ける。

## 観点

- 周辺との統一感が取れているか？
- ネストは浅くできているか？
    - 失敗ケースは早く返す（単純な if else は if のみに。ループは continue)
- メソッド化してコードを文書化できているか？
    - 長い条件式/文になっていないか？
        - 見やすく分割されているか？
- 変数/関数/クラス/パッケージのスコープは小さいか？
    - 小さくすることで依存を小さくできる＝最小限にできているか？
    - イミュータブルで済む物はそうできているか？
- 重複コード/冗長なコードがないか？
    - ただし、意味合いが異なる物をひとまとめにしてはならない
- コードは適切に分割できているか？
    - 汎用コードを(プロジェクトコードから)分離できているか？
    - クラス/メソッド/関数は責務が一意か？明確か？
    - 状態を持つ処理はクラス化できているか？
- コメント(Why?)の内容は具体的に（できれば具体例を添える）
    - 処理への要約コメントを書く位ならメソッド化してコードを文書化する
- 仕様面
    - 仕様を満たしているか
    - 仕様に考慮漏れがないか
    - デグレはないか
    - 良い設計か

### 簡易なもののサンプル

```java
Class ExampleService {

  // パス情報は別クラスで管理されている前提
  private static String EXTERNAL_CONF_DIR_PATH = ProductPorperties.getConfDir() + File.separator + "external";
  
  private static EXTERNAL_XXX_CONF_NAME = "external_xxx.conf";
  private static EXTERNAL_YYY_CONF_NAME = "external_yyy.conf";
  private static EXTERNAL_ZZZ_CONF_NAME = "external_zzz.conf";
  Logger LOGGER = LoggerFactory.getLogger(ExampleService.class);

  ExampleService() {
    initSetting()
    
    if () {
    
    try {
      loadExternalConfig()
    } catch (IOException e) {
      LOGGER.error("load failure.", e)
    }
  }


}
```

```java
Class ExampleService {

  // シングルトン想定
  private static ExampleService instance = new ExampleService();
  // パス情報は別クラスで管理されている前提
  private static PATH EXTERNAL_CONF_DIR_PATH = ProductPorperties.getConfDir();
  
  private static EXTERNAL_XXX_CONF_NAME = "external" + File.separator + "external_xxx.conf";
  private static EXTERNAL_YYY_CONF_NAME = "external" + File.separator + "external_yyy.conf";
  private static EXTERNAL_ZZZ_CONF_NAME = "external" + File.separator + "external_zzz.conf";
  private static Logger LOGGER = LoggerFactory.getLogger(ExampleService.class);

  private ExampleService() {
    initSetting()
    
    Path externalXxxConfPath = EXTERNAL_CONF_DIR_PATH.resolve(EXTERNAL_XXX_CONF_NAME);
    Path externalYyyConfPath = EXTERNAL_CONF_DIR_PATH.resolve(EXTERNAL_YYY_CONF_NAME);
    Path externalZzzConfPath = EXTERNAL_CONF_DIR_PATH.resolve(EXTERNAL_ZZZ_CONF_NAME);

    List<Path> configPaths = List.of(externalXxxConfPath, externalYyyConfPath, externalZzzConfPath);
    boolean isAllExist = true;
    for (Path p : configPaths) {
      if (Files.notExists(p)) {
        isAllExist = false;
        break;
      }
    }
    
    if (isAllExist) {
      try {
        loadExternalConfig()
      } catch (IOException e) {
        LOGGER.error("load failure.", e)
      }  
    } else {
      LOGGER.inf("files non exist: " + Stirng.join(nonExistConfigs, ", "));
    }
  }
}
```

```java
Class ExampleService {

  // パス情報は別クラスで管理されている前提
  private static String EXTERNAL_CONF_DIR_PATH = ProductPorperties.getConfDir() + File.separator + "external";
  
  private static EXTERNAL_XXX_CONF_NAME = "external_xxx.conf";
  private static EXTERNAL_YYY_CONF_NAME = "external_yyy.conf";
  private static EXTERNAL_ZZZ_CONF_NAME = "external_zzz.conf";
  Logger LOGGER = LoggerFactory.getLogger(ExampleService.class);

  ExampleService() {
    initSetting();
    loadExternalConfigIfExist();    
  }

  void loadExternalConfigExist() {
    List<String> nonExistConfigNames = findExternalCoinf();
    if (nonExistConfigs.isEmpty()) {
      LOGGER.inf("files non exist: " + Stirng.join(nonExistConfigs, ", "));
      return;
    }
    
    try {
      loadExternalConfigs()
    } catch (IOException e) {
      LOGGER.error("load failure.", e)
    }
  }

  List<String> findExternalCoinf() { 
    List<String> externalConfigNames = List
        .of(EXTERNAL_XXX_CONF_NAME, EXTERNAL_YYY_CONF_NAME, EXTERNAL_ZZZ_CONF_NAME);
    externalConfigNames.stream()
        .map(EXTERNAL_CONF_DIR_PATH::resolve)
        .filter(Files::notExists)
        .map(File::getFileName)
        .collect(Collections::toList);
  }

}
```

## 命名まとめ

※随時追加

- ～ならxxxする： loadConfigIfExist

[メソッド名、迷った時に参考にできる単語一覧](https://blog.77jp.net/guidelines-for-variables-and-method-names-summary)

## コードレビューでやること

最低限の品質担保（これが満たせないと本来レビューすべきことに中々入れない）

- コードフォーマット
- メソッドの長さ/ネストの深さなど
- 記述が分かりやすいか（メソッド名/関数名/簡潔なロジック）
- セキュリティ担保
    - validateする
    - 自前でHTML組立て->XSS、ユーザ入力そのままSQLに->SQLインジェクション、等
- パフォーマンス担保
    - 不要なインスタンス
    - ループ数削減できない？
    - N+1問題

→ツールで機械的チェックできるものはそうした方が良い。良いフレームワークに乗っかることで回避できるものもある。

本来レビューすべきこと

- 仕様を満たしているか
- 仕様に考慮漏れがないか
- デグレはないか
- 良い設計か

→ 確認するためのフォーマットを設ける（以下実際に使っている物）

- 概要/目的
    - この修正でできるようになること。
    - 元ネタがあればリンクを貼る。
- 方針
- 実機確認結果
- 補足事項
    - diffの当該行に直接コメント

※必要なら、方針の段階でレビューする (WIP) -> 手戻り防止

## ref

[デキるプログラマだけが知っているコードレビュー7つの秘訣](https://www.slideshare.net/rootmoon/7-37892729)

[「速」を落とさないコードレビュー](https://www.slideshare.net/takafumionaka/ss-71482322)