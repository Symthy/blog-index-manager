# JavaScript 基本

## クラス定義

・ES5

```js
function Member(firstName, lastName) {
  this.firstName = firstName;
  this.lastName = lastName;
}

Member.prototype.getName = function () {
  return this.lastName + this.firstName;
}
```

・ES6～

```js
class Member {
  constructor(firstName, lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
  }
  // プロトタイプメソッド
  getName() {
    return this.lastName + this.firstName;
  }
  // 上記と同じ。メンバーメソッドはアロー関数で書いた方が良い
  getName = () => {
    return this.lastName + this.firstName;
  }
}
```

※この宣言であればprototypeに紐づく

以下のようにすると、インスタンス毎にメソッドが作られる（その分メモリ喰う）

優先度：インスタンスメソッド＞プロトタイプメソッド

```js
class Counter {
    constructor() {
        this.count = 0;
        // インスタンスメソッド
        this.increment = () => {
            this.count++;
        };
    }
}
```

ref: [【JavaScript】ES6のクラスの定義方法](https://se-tomo.com/2019/02/12/%E3%80%90javascript%E3%80%91es6%E3%81%AE%E3%82%AF%E3%83%A9%E3%82%B9%E3%81%AE%E5%AE%9A%E7%BE%A9%E6%96%B9%E6%B3%95)

## prototype

プロトタイプベースでは、オブジェクトの抽象としてのクラスが存在しない。

オブジェクトは直接、他のオブジェクトを継承する。

そのときの継承元になったオブジェクト＝プロトタイプ。クラスの実体はプロトタイプチェーン

```js
class Bird {
  constructor(name) {
    this.name = name;
  }
  cry = () => {
    console.log(`${this.name} is cry`);
  };
  static show = (name) => {
    console.log(`${name} is Bird`);
  };
}
class FlyableBird extends Bird {
  constructor(name) {
    super(name);
  }
  fly = () => {
    console.log(`${this.name} is fly`);
  };
}
```

プロトタイプチェーンは、最終的には `{}`（空オブジェクト）を経て`null`に到達する

```js
const swallow = new FlyableBird('燕');

> swallow.__proto__
FlyableBird {}
> swallow.__proto__.__proto__
Bird {}
> swallow.__proto__.__proto__.__proto__
{}
> swallow.__proto__.__proto__.__proto__.__proto__
null
```

上記のクラスは、実際には以下。

```js
function Bird(name) {
  this.name = name;
  this.cry = function () {
    console.log(`${this.name}が鳴きました`);
  };
  return this;
}
// static method
Bird.explain = function (name) {
  console.log(`${name}は翼があって卵を生みます`);
};

function FlyableBird(name) {
  Bird.call(this, name);
  this.fly = function () {
    console.log(`${this.name}が飛びました`);
  };
  return this;
}
// extends
FlyableBird.prototype.__proto__ = Bird.prototype;
```

prototypeチェーンについては、以下が分かりやすい

[や...やっと理解できた！JavaScriptのプロトタイプチェーン](https://maeharin.hatenablog.com/entry/20130215/javascript_prototype_chain)

## this と strict

thisの4パターン

1. new -> 生成されたオブジェクト

2. メソッド実行 -> 所属するオブジェクト

3. 1,2以外の関数［非Strict モード］-> グローバルオブジェクト

4. 1,2以外の関数［Strict モード］-> undefined

strict モードは、グローバルオブジェクトの汚染を防止

- 4のサンプル

```js
class Person {
  constructor(name) {
    this.name = name;
  }
  greet() {
    const doIt = function () {
      console.log(`Hi, I'm ${this.name}`);
    };
    doIt();
  }
}
const p = new Person('sym');
p.greet(); 
// TypeError: Cannot read property 'name' of undefined 
// doIt の this が undefinedのため
```

対処方法

```js
class Person {
  constructor(name) {
    this.name = name;
  }
  // 1. 関数にthisを束縛 bind()
  greet1() {
    const doIt = function () {
      console.log(`Hi, I'm ${this.name}`);
    };
    const bindedDoIt = doIt.bind(this); 
    bindedDoIt();
  }
  // 2. this を指定して実行 xxx.call(this)
  greet2() {
    const doIt = function () {
      console.log(`Hi, I'm ${this.name}`);
    };
    doIt.call(this); 
  }
  // 3. 変数にthisを移し替える
  greet3() {
    const self = this; // 3. 変数_this に値を移し替える
    const doIt = function () {
      console.log(`Hi, I'm ${self.name}`);
    };
    doIt();
  }
  // 4. アロー関数式で定義
  greet4() {
    // 2.メソッドなので,ここでのthisは所属するオブジェクトになる
    const doIt = () => { 
      console.log(`Hi, I'm ${this.name}`);
    };
    doIt();
  }
  // メソッド自身もアロー関数式で定義
  greet5 = () => { 
    // アロー関数なので外のスコープのthisを参照 = オブジェクト自身となる
    const doIt = () => {
      console.log(`Hi, I'm ${this.name}`);
    };
    doIt();
  }
}
```

アロー関数は暗黙の引数としての this を持たず、this を参照すると関数の外のスコープのthisの値がそのまま使われるの

## JSの関数型プログラミング

- 手続き型：文を多用。可変性
- 関数型：式の組み合わせ。不変性。

```js
const range = (start, end) => [...new Array(end - start).keys()].map((n) => n + start);
console.log(range(1, 101).filter((n) => n % 8 === 0));
```

関数型プログラミングのパラダイムでは主に次のようなことが行われる。

- 名前を持たないその場限りの関数（無名関数）を定義可

```js
(n) => n * 2;
```

- 変数に関数を代入可

```js
const double = (n) => n * 2;
```

- 関数の引数に関数を渡す、戻り値として関数を返却可（高階関数）

```js
const greeter = (target) => () => console.log(`Hi, ${target}!)`;

// const greeter = (target) => {
//   const sayHello = () => {
//     console.log(`Hi, ${target}!`);
//   };
//   return sayHello;
// };
```

- 関数に特定の引数を固定した新しい関数を作成可（部分適用）

```js
const withMultiple = (n) => (m) => n * m;  // カリー化
console.log(withMultiple(3)(5)); // 15
// const withMultiple = (n) => {
//   return (m) => n * m;
// };
// console.log(withMultiple(3)(5));

const triple = withMultiple(3);  // 関数の部分適用
console.log(triple(5)); // 15
```

- 複数の高階関数を合成してひとつの関数に合成可能（関数合成）
    - クロージャ(Closure)：関数閉包。関数を関数で閉じて包む。

```js
const counter = (count = 0) => (adds = 1) => count += adds;
const increment = counter();
increment(); // 1
increment(2); // 3


// const counter = (count = 0) => {  // counter = Enclosure
//   const increment = (adds = 1) => {  // increment = Closure
//     return count += adds;
//   };
//   return increment;
// };
```

一つの状態と一つのメソッドしか持たないようなクラスを作るくらいなら、クロージャで済ませたほうがスマート

## Promise

### 前提: JavaScriptは非同期

JavaScriptは非同期言語。実行完了を待たず次の処理が行われる。

```js
console.log("1番目");
setTimeout(() => {
  console.log("2番目(1秒後に実行)");
}, 1000);
console.log("3番目");

// 以下の順で出力
//  1番目
//  3番目
//  2番目(1秒後に実行)
```

### Promise基本形

```js
const promise = new Promise((resolve, reject) => {
  resolve();
  reject();
}).then(() => {
  console.log("resolved");
}).catch(() => {
  console.log("rejected");
}).finally(() => {
  console.log('Completed');
});
```

Promise は 処理順序を約束する。

```js
console.log("1番目");

new Promise((resolve) => {
  setTimeout(() => {
    console.log("2番目(1秒後に実行)");
    resolve();
  }, 1000);
}).then(() => {
  console.log("3番目");
});

// 以下の順で出力
//  1番目
//  2番目(1秒後に実行)
//  3番目
```

### Promise の状態

- pending: 未解決 (処理待ち状態。初期状態)
- resolved: 解決済み (処理成功)
- rejected: 拒否 (処理失敗)

状態に応じて以下の通りに振り分けられる

- resolved -> then()
- rejected -> catch()

### Promise複数実行 (all / race)

- Promise.all()

全てのPromiseがresolvedになったら次の処理に進む

```js
const promise1 = new Promise((resolve) => {
  setTimeout(() => { resolve(); }, 1000);
}).then(() => {
  console.log("promise1 end");
});

const promise2 = new Promise((resolve) => {
  setTimeout(() => { resolve(); }, 3000);
}).then(() => {
  console.log("promise2 end");
});

Promise.all([promise1, promise2]).then(() => {
  console.log("all finish");
});

// 出力順
// promise1 end
// promise2 end
// all finish
```

- Promise.race()

どれか1つのPromiseがresolvedになったら次に進む

```js
const promise1 = new Promise((resolve) => {
  setTimeout(() => { resolve(); }, 1000);
}).then(() => {
  console.log("promise1 end");
});

const promise2 = new Promise((resolve) => {
  setTimeout(() => { resolve(); }, 3000);
}).then(() => {
  console.log("promise2 end");
});

Promise.race([promise1, promise2]).then(() => {
  console.log("any finish");
});

// 出力順
// promise1 end
// any finish
// promise2 end
```

### async/await で簡潔に書ける

- then() を書く必要がなくなる

```js
// Promise.then()使用
const waitProcessor = (ms) => {
  new Promise((resolve) => {
    setTimeout(() => { resolve(); }, ms);
  }).then(() => {
    console.log(`stop: ${ms} ms`);
  });
};

// Promise & async/await使用
const waitProcessor = async (ms) => {
  new Promise((resolve) => {
    await setTimeout(() => { resolve(); }, ms);
  })
  console.log(`stop: ${ms} ms`);
};
```

- エラー処理は、try/catch で書けばよい

```js
const asyncErrorThrowFunc = async () => {
  throw new Error('Exception occurred!!')
}

const getError = async () => {
  try {
    const result = await asyncErrorThrowFunc()
    console.log('This is not executed')
  } catch(err) {
    console.log(err.message)
  } finally {
    console.log('finish')
  }
}
```

async： 非同期関数定義。頭に付けた関数は、Promiseオブジェクトを返す関数になる

await： 頭に付けた関数は、Promiseオブジェクトが値を返すのを待つようになる

```js
const asyncFunc = async () => {
  const x = await new Promise((resolve) => {
    setTimeout(() => {
      resolve(1);
    }, 1000);
  });
  const y = await new Promise((resolve) => {
    setTimeout(() => {
      resolve(1);
    }, 1000);
  });

  console.log(x + y);  // 2
};
```

ref: [【ES6】 JavaScript初心者でもわかるPromise講座](https://qiita.com/cheez921/items/41b744e4e002b966391a)

## references

[JavaScript Primer](https://jsprimer.net/)

[【JavaScript】ES6のクラスの定義方法](https://se-tomo.com/2019/02/12/%E3%80%90javascript%E3%80%91es6%E3%81%AE%E3%82%AF%E3%83%A9%E3%82%B9%E3%81%AE%E5%AE%9A%E7%BE%A9%E6%96%B9%E6%B3%95)

[【ES6】 JavaScript初心者でもわかるPromise講座](https://qiita.com/cheez921/items/41b744e4e002b966391a)
