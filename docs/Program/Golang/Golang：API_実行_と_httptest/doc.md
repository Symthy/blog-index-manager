# Golang：API 実行 と httptest

## httptest

テスト用のモックサーバをたてることができる

- API 実行コード

```golang
const apiurl = "https:/xxxxxx"

func buildGetRequest(name string) (*http.Request, error) {
	url := apiurl + name
	req, err := http.NewRequest(http.MethodGet, url, nil)
	if err != nil {
		return nil, err
	}
	return req, err
}

func getResource(req *http.Request) ([]byte, error) {
	client := &http.Client{Timeout: 10 * time.Second}

	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("Error Response. Status:%s, Body:%s", resp.Status, body)
	}

	return body, err
}
```

- テストコード

```golang
func TestFailureToGet(t *testing.T) {
	ts := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusBadRequest)
		resp := make(map[string]string)
		resp["message"] = "Bad Request"
		jsonResp, err := json.Marshal(resp)
		if err != nil {
			log.Fatalf("Error happened in JSON marshal. Err: %s", err)
		}
		w.Write(jsonResp)
	}))
	defer ts.Close()

	req, err := http.NewRequest(http.MethodGet, ts.URL, strings.NewReader(""))
	if err != nil {
		assert.FailNow(t, "failed to build request")
	}
	actual, err := getResource(req)
	assert.EqualError(t, err, "Error Response. Status:400 Bad Request, Body:{\"message\":\"Bad Request\"}")
	assert.Nil(t, actual)
}
```

このように、正常系だけでなく、エラーレスポンスを返却させることもできる。（テスト捗る）

## refs

[Go の test を理解する - httptest サブパッケージ編](https://budougumi0617.github.io/2020/05/29/go-testing-httptest/)

[Go のテストに入門してみよう！](https://future-architect.github.io/articles/20200601/#API%E3%82%B5%E3%83%BC%E3%83%90%E3%81%AB%E3%82%A2%E3%82%AF%E3%82%BB%E3%82%B9%E3%81%99%E3%82%8B%E3%83%86%E3%82%B9%E3%83%88%E3%82%92%E3%81%97%E3%81%9F%E3%81%84)
