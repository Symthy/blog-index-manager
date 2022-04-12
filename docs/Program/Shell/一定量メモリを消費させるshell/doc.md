# 一定量メモリを消費させるshell

stress コマンドが使えるならば、お手軽にできるかもしれない。

使えない環境のため、以下で実施した。その記録

- 理由が分かっていないが、指定したバイトの2倍取られた
- 一度に大きい量を一気に消費はできないのでループ
- 消費させるメモリ量が増えれば、その分時間がとてもかかるようになる（1GBで数分レベル）

ご利用は計画的に、もっといい方法がありそう。

```shell
#! /bin/bash

INIT_ALLOC_MEM=209715200  # 200MB * 2 消費
LOOP_NUM=2  # INIT_ALLOC_MEM * N
REPEAT_ALLOC_MEM=10485760  # 10MB * 2 消費

echo PID=$$
echo "# start: init memory allocate."
for i in `seq ${LOOP_NUM}`
do
  eval a$i'=$(head --bytes ${INIT_ALLOC_MEM} /dev/zero |cat -v)'
  echo -n " $i"
done
echo
echo "# end."

echo -n "[ Enter : add 20 MB ] , [ Ctrl+d : stop ]"
c=0
while read byte; do
   eval b$c'=$(head --bytes ${REPEAT_ALLOC_MEM} /dev/zero |cat -v)'
   c=$(($c+1))
   echo -n ">"
done
echo
```

以下、メモリ量確認用shell (freeコマンドの結果から抽出)

```shell
mem_free=`free -m | awk '/Mem:/ {print $4}'`
swap_free=`free -m | awk '/Swap:/ {print $4}'`
buff_cache=`free -m | awk '/Mem:/ {print $6}'`
total_virtual_mem=`expr ${mem_free} \+ ${swap_free} \+ ${buff_cache}`

echo "Mem Free:   ${mem_free} MB"
echo "Swap Free:  ${mem_free} MB"
echo "Buff/Cache: ${mem_free} MB"
echo "Total:      ${total_virtual_mem} MB"
```

ref: [Linuxで手軽にCPU/メモリの負荷をかける方法](https://qiita.com/keita0322/items/8fba88debe66fa8d2b39)