# Refactor Diary 1 (Java: APIレスポンス解析)

例：ユーザロールチェック

ユーザ情報はAPIにより以下のようなものが取れるものとする

```java
// API Response Data Model
public class User {
    private String userName;
    private List<RoleEnum> roles;
    // 他にも複数のフィールドがあるものとする
    // Getter,Setter等省略
}
```

リファクタ前

```java
public class UserRoleValidator {

    private final Logger logger = LoggerFactory.getLogger(UserRoleValidator.class);
    private final ApiClient apiClient;  // OkHttpClient ラッパークラスとする
    private static final List<RoleEnum> REQUIRED_ANY_ROLES = Lists.of(RoleEnum.Admin, RoleEnum.Manage);

    UserRoleValidator(ApiClient apiClient) {
        this.apiClient = apiClient;
    }

    // APi実行～レスポンスボディ変換～ロールチェックまで全部入り
    public void execute() {
        OkHttp.Response response = apiClient.getUser(userName);
        if (!response.isSuccessful()) {
            LOGGER.error("Response Status Code: " + response.code());
            if (Objects.nonNull(response.body())) {
                LOGGER.error("Error Response Contents: " + response.body().string());
            }
            LOGGER.error("message");
            throw new IOException("message");
        }
        User user = new Gson().fromJson(response.body().string(), User.class)
        List<Role> roles = Objects.isNull(user.getRoles()) ? List.of() : user.getRoles();
        if (roles.isEmpty() || 
                REQUIRED_ANY_ROLES.stream().anyMatch(r -> roles.contains(r))) {
            LOGGER.error("message");
            throw new InsufficientRoleException("message");
        }
    }
}
```

何が問題か

- (レスポンスに対して共通で行うような) 共通処理が入り込み、流用できない
- ロールチェックのパターン網羅するテストを書くにあたり、全テストで apiClient をmockし、返すresponse body data を指定する必要がある等、テスト自体が見にくくなる


リファクタ後

```java
public class UserRoleValidator {

    private static final Logger LOGGER = LoggerFactory.getLogger(UserRoleValidator.class);
    private final ApiClient apiClient; 

    UserRoleValidator(ApiClient apiClient) {
        this.apiClient = apiClient;
    }

    public void execute(String userName) {
        var apiResponse = new DataStoreApiResponse(apiClient.getUser(userName));
        if (apiResponse.isSuccessful()) {
            LOGGER.error("message");
            throw new IOException("message");
        }
        validateUserRole(apiResponse.deserialize());
    }

    public void validateUserRole(User user) {
        if (RequiredRoles.isSatisfy(user.getRoles())) {
            LOGGER.error("message");
            throw new InsufficientRoleException("message");
        }
    }
}

// API Response Data Model
public class User {
    private String userName;
    private List<RoleEnum> roles;
    // Getter,Setter等省略
}

// レスポンスに対する共通処理の集約
class DataStoreApiResponse {
    
    private static final Logger LOGGER = LoggerFactory.getLogger(DataStoreApiResponse.class);
    private final isSuccessful;
    
    DataStoreApiResponse(OkHttp.Response response) {
        if (!response.isSuccessful()) {
            LOGGER.error("Response Status Code: " + response.code());
            if (Objects.nonNull(response.body())) {
                LOGGER.error("Error Response Contents: " + response.body().string());
            }
            isSuccessful = false;
            return;
        }
        isSuccessful = true;
    }

    boolean isSuccessfull() {
        return isSuccessful;
    }

    int getStatusCode() {
        return response.code();
    }

    <T> T deserialize(Class<T> cls) {
        return new Gson().fromJson(response.body().string(), cls)
    }
}

// 知識の確立
public class RequiredRoles {

    private static final List<RoleEnum> REQUIRED_ANY_ROLES = Lists.of(RoleEnum.Admin, RoleEnum.Manage);

    boolean isSatisfy(User user) {
        List<Role> roles = Objects.isNull(user.getRoles()) ? List.of() : user.getRoles();
        if (roles.isEmpty()) {
            return false;
        }
        return REQUIRED_ANY_ROLES.stream().anyMatch(r -> roles.contains(r));
    }
}
```

先にどういうところでどういうテストが必要になるかを考えて、テストしやすい部品を作る

- 不良を作りこみやすいような重要な箇所（上記例ならロールチェック処理）を見極め
- そこに対して、容易にテストができるよう部品に分ける

それにより、複数の重要な知識が1か所に混在し、結果として見通しが悪くなるようなことが防げる。テストも見やすくなり、どういったケースがあり得るのか等テストから読み取りが容易になる