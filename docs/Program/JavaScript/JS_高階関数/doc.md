# JS 高階関数

- 他の関数を引数に取るか
- 戻り値として関数を返すか
- もしくはその両方を満たすもの

利点

- 純粋関数 = 副作用がないため、テスト容易性/再利用性/スケーラビリティの点で優れる

元のデータの不変性を保てる

## カリー化

- JSは非同期処理によりコードが複雑になりがち -> これの解消に高階関数が使われることがある
- この目的で使用するのがカリー化

```js
const serviceLogs = serviceName => message => 
    console.log(`${serviceName}: ${message}`);

const log = serviceLogs('test');
log('Synchronous execution')
promissFunc(100).then(
    arg => log(`Asynchronous execution (arg: ${arg})`)
).catch(
    err => log(`Asynchronous execution error`)
)

// test: Synchronous execution
// test: Asynchronous execution (arg: 100)
// test: Asynchronous execution error
```

## 再起

非同期処理と組み合わせた時に真価を発揮する。再起呼び出しタイミングの調整ができる

```js
const countdown = (value, fn, delay = 1000) => {
    fn(value);
    return value > 0
        ? setTimeout(() => countdown(value - 1, fn, delay))
        : value;
}
const outputLog = value => console.log(value);
countdouwn(10, outputLog)
```

用途：

- データ構造の探索
- フォルダからファイル探索
- HTMLドキュメントから DOM 要素探索
- ネスト下オブジェクトとから指定のプロパティ値を取得

```js
const obj = {
    type: 'person',
    data: {
        gender: 'male',
        info: {
            id: 555,
            name: {
                first: 'SYM',
                last: 'XXXX'    
            }
        }
    }
}

deepPick('type', obj);  // person
deepPick('data.info.name.first', obj);  // SYM

const deepPick = (field, data = {}) => {
    [first, ...remaing] = field.split('.');
    return remaing.length > 0 ? deepPick(reaming.join('.'), data[first]) : data[first];
}
```

## 関数の合成

関数の合成とは

- 関数を順番に、もしくは並行に呼び出し、複数の関数呼び出しを束ねてより大きな関数を作ることで、アプリケーション全体を構築する過程

パターン

- chaining (連鎖)

```js
const template = 'HH:MM:SS TT';
const time = template
    .replace('HH', '01')
    .replace('MM', '23')
    .replace('SS', '45')
    .replace('TT', 'AM');
```

- compose (高階関数による関数合成)

関数合成関数：

```js
const compose = (...fns) => initFunc => {
    fns.reduce((composed, fn) => f(composed), initFunc)
}
```

```
const both = compose(civilianHours, appendAMPM);
both(new Date());

// compose(civilianHours, appendAMPM) で以下となる
// initFunc => {
//    [civilianHours, appendAMPM].reduce((composed, f) => f(composed), initFunc)
// }
//
// both(new Date()); で initFunc = new Date() に代入され、
// [civilianHours, appendAMPM].reduce((composed, fn) => fn(composed), new Date())
// となるので、reduce で 
//  (1) composed: new Date(), fn: civilianHours -> civilianHours(new Date())
//  (2) composed: civilianHours(new Date()), fn: appendAMPM 
//      -> appendAMPM(civilianHours(new Date()))  となる
```

サンプル

- 命令型

```js
setInterval(logClockTime, 1000);

function logClockTime() {
    let time = buildClockTime();
    console.clear();
    console.log(time);
}

function buildClockTime() {
    const date = new Date();
    let time = {
        hours: date.getHours(),
        minutes: date.getMinutes(),
        seconds: date.getSeconds(),
        ampm: 'AM'
    };
    
    if (time.hours == 12) {
        time.ampm = 'AM'
    } else if (time.hours > 12) {
        time.ampm = 'PM';
        time.hours -= 12;
    }
    
    if (time.hours < 10 {
        time.hours = '0' + time.hours;
    }
    if (time.minutes < 10) {
        time.minutes = '0' + time.minutes;
    }
    if (time.seconds < 10 {
        time.seconds = '0' + time.seconds;
    }
}
```

- 関数型
    - 関数は非破壊的であるため、実行後も元のオブジェクトは不変

```js
const oneSecond = () => 1000;  // 固定値を取得する時にも関数を用いる
const getCurrentTime = () => new Date();
const clear = () => console.clear();
const log = message => console.log(message);

const serializeClockTime = date => ({
    hours: date.getHours(),
    minutes: date.getMinutes(),
    seconds: date.getSeconds()
});

const civilianHours = clockTime => ({
    ...clockTime,
    hours: clockTime.hours > 12 ? clockTime.hours - 12 : clockTime.hours
});

const appendAMPM = clockTime => ({
    ...clockTime,
    ampm: clockTime.hours >= 12 ? 'PM' : 'AM';
});

const display = target => time => target(time);

const formatClock = format => time => 
    format.replace('HH', time.hours)
        .replace('MM', time.minutes)
        .replace('SS', time.seconds)
        .replace('TT', time.ampm)

const prependZero = key => clockTime => ({
    ...clockTime,
    [key]: clockTime[key] < 10 ? '0' + clockTime[key] : '' + clockTime[key]
});

const convertToCivilianTime = clockTime => compose(
    appendAMPM,
    civilianHours
)(clockTime);

const convertToDoubleDigits = civilianTime => compose(
    prependZero('hours'),
    prependZero('minutes'),
    prependZero('seconds')
)(civilianTime);

// 処理
const startTicking = () => setInterval(
    compose(
        clear,
        getCurrentTime,
        serializeClockTime,
        convertToCivilianTime,
        convertToDoubleDigits,
        formatClock('HH:MM:SS TT'),
        display(log)
    ),
    oneSecond()
);

startTicking();
```
