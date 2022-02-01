# Gson Serialize (Object -> String) での時刻フォーマット指定方法

速攻で解決したが念の為のメモ。

## 基本

Gson: https://github.com/google/gson ※Tutorialへのリンク有り

- serialize (obj -> json)

```java
Gson gson = new Gson();
String json = gson.toJson(obj);
```

- deserialize (json -> obj)

```java
String json = "{ ～ }";
Gson gson = new Gson();
SampleClass obj = gson.fromJson(json, SampleClass.class);
```

## 時刻フォーマット指定方法

- Date -> OffsetDateTime形式(文字列) の例

GsonBuilder に registerTypeAdapter で登録すればよい。Deserializerも同様。

Objectの中にObjectがあり、そこにDateがある場合でも、以下で可能

```java
class SampleComverter<T> {

  public static String convertObjToJson(T obj) {
    GsonBuilder gsonBuilder = new GsonBuilder();
    gsonBuilder.registerTypeAdapter(Date.class, new DateSerializer());
    Gson gson = gsonBuilder.setPrettyPrinting().create();
    return gson.toJson(obj);
  }
    
  private static class DateSerializer implements JsonSerializer<Date> {
    @Override
    public JsonElement serialize(Date src, Type srcType, JsonSerializationContext context) {
      OffsetDateTime datetime = OffsetDateTime.ofInstant(src.toInstant(), ZoneOffset.UTC);
      return new JsonPrimitive(DateTimeFormatter.ISO_OFFSET_DATE_TIME.format(datetime));
    }
  }
}
```

## ref

以下が分かりやすかった。

- [GSON - Custom Serialization and Deserialization Examples](https://www.javaguides.net/2018/10/gson-custom-serialization-and-deseriliazation-examples.html)

公式チュートリアルだと、以下の章に対応する話。

- [Gson Tutorial - 8.Using Custom Serialization and Deserialization classes ](https://studytrails.com/2016/09/12/java-google-json-custom-serializer-deserializer/)