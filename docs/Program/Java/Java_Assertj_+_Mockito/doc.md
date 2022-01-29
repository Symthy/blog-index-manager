# Java Assertj + Mockito

## Assertj

### 共通

- 同値

```java
assertThat("Foo").isEqualTo("Foo");
assertThat("Foo").isNotEqualTo("Bar");
```

- Null

```java
assertThat(actual).isNull();
assertThat(actual).isNotNull();
```

- 同一インスタンス

```java
assertThat(bar1).isSameAs(bar2);
assertThat(bar1).isNotSameAs(bar2);
```

- インスタンスの型

```java
assertThat(baz).isInstanceOf(Baz.class);
assertThat(qux).isInstanceOf(Baz.class).isInstanceOf(Qux.class);
assertThat(qux).isNotInstanceOf(Baz.class);
```

- toString()

```java
assertThat(fooBar).hasToString("FooBar");  // toString()の値確認
```

- 注釈

```java
assertThat("Foo").as("AssertJ sample").isEqualTo("Bar");
```

### 文字列

- 先頭/末尾一致

```java
assertThat("FooBar").startsWith("Foo");
assertThat("FooBar").endsWith("Bar");
```

- 大小無視の一致

```java
assertThat("Foo").isEqualToIgnoringCase("FOO");
```

- 空文字/Null

```java
assertThat("").isEmpty();
assertThat(actual).isNullOrEmpty(); // null
```

- 正規表現比較

```java
assertThat("FooBarBaz").matches("F..B..B..").matches("F.*z");
```

- 数字かどうか

```java
assertThat("1234567890").containsOnlyDigits();
```

- 行数確認

```java
assertThat("foo\nbar\nbaz").hasLineCount(3);
assertThat("foo\r\nbar\r\nbaz").hasLineCount(3);
```

### 数値

- 範囲(Between)

```java
assertThat(7).isBetween(0, 9).isBetween(7, 7);
assertThat(7).isCloseTo(5, within(2)); // 5 ± 2 
```

- 大なり/小なり

```java
assertThat(7).isGreaterThan(6).isGreaterThanOrEqualTo(7);
assertThat(7).isLessThan(8).isLessThanOrEqualTo(7);
```

### Collection(List/Set等)

- hasSize: サイズ確認

```java
assertThat(actuals).hasSize(4);
```

- isEmpty: 空か

```java
assertThat(actuals).isEmpty();
```

- contains： 並び順は検証しない。含まれていればOK

```java
List<String> actuals = Lists.newArrayList("Lucy", "Debit", "Anna", "Jack");
assertThat(actuals).contains("Lucy", "Anna");
```

- containsOnly: 並び順は検証しない。全て含むならOK

```java
List<String> actuals = Lists.newArrayList("Lucy", "Debit", "Anna", "Jack");
assertThat(actuals).containsOnly("Debit", "
Lucy", "Jack", "Anna");
```

- containsSequence: 並び順を検証。件数確認しない

```java
List<String> actuals = Lists.newArrayList("Lucy", "Debit", "Anna", "Jack");
assertThat(actuals).containsSequence("Lucy", "Debit");
```

- containsSubSequence: 並び順を検証。件数確認しない。抜け漏れOK

```java
List<String> actuals = Lists.newArrayList("Lucy", "Debit", "Anna", "Jack");
assertThat(actuals).containsSubsequence("Lucy", "Anna")
                   .containsSubsequence("Lucy", "Jack");
```

- containsOnlyOnce: 含む かつ 重複なしならOK

```java
List<String> actuals = Lists.newArrayList("Lucy", "Debit", "Anna", "Lucy");
assertThat(actuals).containsOnlyOnce("Debit", "Anna");
```

- containsAnyOf: いずれか１つがある

```java
assertThat(actuals).containsAny("Debit", "Anna");
```

- extracting

```java
// 特定フィールドのみ抽出
assertThat(list).extracting("name").containsExactly("佐藤","田中","鈴木");
```

### Map

- containsEntry

```java
assertThat(actuals).containsEntry("Key1", 101)
                   .containsEntry("Key2", 202)
                   .doesNotContainEntry("Key9", 999);
```

- containsKey

```java
assertThat(actuals).containsKeys("Key2", "Key3")
                   .doesNotContainKey("Key9");
```

- containsValue

```java
assertThat(actuals).containsValues(202, 303)
                   .doesNotContainValue(999);
```

- hasSize/isEmpty もある

### Iterable関係

#### まとめて検証

- allSatisfy: 全て満たす

```java
assertThat(hobbits).allSatisfy(character -> {
  assertThat(character.getRace()).isEqualTo(HOBBIT);
  assertThat(character.getName()).isNotEqualTo("Sauron");
});
```

- anySatisfy: いずれかを満たす

```java
assertThat(hobbits).anySatisfy(character -> {
  assertThat(character.getRace()).isEqualTo(HOBBIT);
  assertThat(character.getName()).isEqualTo("Sam");
});
```

- noneSatisfy: 全て満たさない

```java
assertThat(hobbits).noneSatisfy(character -> assertThat(character.getRace()).isEqualTo(ELF));
```

#### 特定の１つを検証

- first/element/last: 最初/間/最後

```java
Iterable<TolkienCharacter> hobbits = list(frodo, sam, pippin);
assertThat(hobbits).first().isEqualTo(frodo);
assertThat(hobbits).element(1).isEqualTo(sam);
assertThat(hobbits).last().isEqualTo(pippin);
```

#### 単一要素

```java
assertThat(babySimpsons).singleElement()
                        .isEqualTo("Maggie");
```

#### 特定フィールドの抽出

```java
assertThat(users).extracting((u) -> tuple(u.id, u.rank))
    .contains(tuple("abc", 10))
    .contains(tuple("def", 20));

assertThat(users).extracting("id", "rank")
    .contains(tuple("abc", 10))
    .contains(tuple("def", 20));
```

```java
assertThat(params)
  .extracting(Param::key, Param::value)
  .containsExactlyInAnyOrder(
     tuple("analysisId", "abc"),
     tuple("projectId", "cde"));
```

### 例外

- 例外確認

```java
assertThatThrownBy(() -> { throw new Exception("boom!"); })
    .isInstanceOf(Exception.class)  // 継承クラス含む
    .isExactlyInstanceOf(IOException.class)  // 一致
    .hasMessageContaining("boom");
```

- 例外が発生しない

```java
// どちらも同じ
assertThatNoException().isThrowBy(() -> System.out.println(""));
assertThatCode(() -> System.out.println("OK")).doesNotThrowAnyException();
```

- 指定した例外発生確認

```java
assertThatExceptionOfType(IOException.class)
    .isThrownBy(() -> { throw new IOException("boom!"); })
    .withMessage("%s!", "boom")
    .withMessageContaining("boom")
    .withNoCause();
```

- 特定の例外確認
    - assertThatNullPointerException
    - assertThatIllegalArgumentException
    - assertThatIllegalStateException
    - assertThatIOException

```java
assertThatIOException().isThrownBy(() -> { throw new IOException("boom!"); })
                       .withMessage("%s!", "boom")
                       .withMessageContaining("boom")
                       .withNoCause();
```

### カスタムAssertion

```java
var fooObj = new FooClass(); // 略
assertThat(fooObj).hasValue("bar");

public class FooClassAssert extends AbstractAssert<FooClassAssert, FooClass> {

  public FooClassAssert(FooClass actual) {  // 定型文
    super(actual, FooClassAssert.class);
  }

  public static FooClassAssert assertThat(FooClass actual) {  // 定型文
    return new FooClassAssert(actual);
  }

  public FooClassAssert hasValue(String key) {  // 独自Assertion
    isNotNull();
    if (actual.getValue(key) == null) {
      failWithMessage("エラーメッセージ");
    }

    return this;  // メソッドチェーンのために必須
  }
}
```

## Mockito

- mock 全体をモック化

```java
var mockedService = new Mock(MessageService.class);
// モック
when(mockedService).getMessage(any()).thenReturn("モック化");
doReturn("モック化").when(mockedService).getMessage(any());

// 呼び出し回数検証
verify(mockedService, times(2)).getMessage(any());
```

- spy 一部のみをモック化

```java
var mockedService = new Spy(MessageService.class);
doReturn("モック化").when(mockedService).getMessage(any());
```

※テスト対象クラスをspyするのは避けた方が良い。責務が大きくなり図来ている兆候 (シングルトンクラスのメソッドのテスト無理やりできるが非推奨。場合による)

- その他

[mockito でコンストラクターの mock を使ったテストをしたい (Mockito 3.5.0 以降)](https://keyno63.hatenablog.com/entry/2021/09/24/234828)

## ref

- [公式ドキュメント](https://assertj.github.io/doc/)

- [AssertJ版：テストでよく使う検証メソッド一覧](https://qiita.com/naotawool/items/6512ecbe2fd006dacfd2)