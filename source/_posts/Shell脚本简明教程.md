---
title: Shell脚本简明教程
date: 2018-12-23 23:23:54
categories: 编程语言
tags: shell
---

# 变量
* 变量定义或者赋值的时候必须是等号两边没有空格
* 使用变量的时候需要带$
* 需要将带空格的字符串赋值给变量时，要用双引号括起来
* 双引号和单引号。在字符串中使用变量，需要在双引号中

```
i=1
echo $i    #1
echo "${i}"  #1  // 变量名外面的花括号{ }是可选的，{}为了帮助解释器识别变量的边界， 
# 推荐给所有变量加上花括号{}，这是个良好的编程习惯。
echo '${i}'  #${i}
a=5
b=2
c=$((a+b)) #变量赋值  7
d=$a+$b #字符串  5+2

# 从键盘输入变量值
echo "What is your name "
read username
echo "Hello ${username}"

# 可以通过 val=$(command) 或者 variable=`command`。将command的执行结果赋值给val 
val=$(date)
echo ${val} # 2018年 7月24日 星期二 22时02分43秒 CST

```

#### 系统变量
|k|v|
|-----|--|
$0	|这个程序的执行名字
$n	|这个程序的第n个参数值，n=1…9
$*	|这个程序的所有参数
$#	|这个程序的参数个数
$$	|这个程序的PID
$!	|执行上一个背景指令的PID
$?	|上一个指令的返回值

# 表达式
```
#!/bin/bash
val=`expr 2 + 2`
echo "val = $val" # val = 4
```
* 表达式和运算符之间要有空格，例如 2+2 是不对的，必须写成 2 + 2。
* 完整的表达式要被 ` ` 包含，注意这个字符 *不是单引号* ，和键盘左上角的波浪号一起的【` ~】。

运算符|说明|举例
|--|--|--|
+|加法|`expr $a + $b` 结果为 30。
-|减法|`expr $a - $b` 结果为 10。
*|乘法|`expr $a \* $b` 结果为  200。
/|除法|`expr $b / $a` 结果为 2。
%|取余|`expr $b % $a` 结果为 0。
=|赋值|a=$b 将把变量 b 的值赋给 a。
==|相等。用于比较两个数字，相同则返回 true。|[ $a == $b ] 返回 false。
!=|不相等。用于比较两个数字，不相同则返回 true。|[ $a != $b ] 返回 true。
-eq|检测两个数是否相等，相等返回 true。|[ $a -eq $b ] 返回 true。
-ne|检测两个数是否相等，不相等返回 true。|[ $a -ne $b ] 返回 true。
-gt|检测左边的数是否大于右边的，如果是，则返回 true。|[ $a -gt $b ] 返回 false。
-lt|检测左边的数是否小于右边的，如果是，则返回 true。|[ $a -lt $b ] 返回 true。
-ge|检测左边的数是否大等于右边的，如果是，则返回 true。|[ $a -ge $b ] 返回 false。
-le|检测左边的数是否小于等于右边的，如果是，则返回 true。|[ $a -le $b ] 返回 true。
!|非运算，表达式为 true 则返回 false，否则返回 true。|[ ! false ] 返回 true。
-o|或运算，有一个表达式为 true 则返回 true。|[ $a -lt 20 -o $b -gt 100 ] 返回 true。
-a|与运算，两个表达式都为 true 才返回 true。|[ $a -lt 20 -a $b -gt 100 ] 返回 false。
=|检测两个字符串是否相等，相等返回 true。|[ $a = $b ] 返回 false。
!=|检测两个字符串是否相等，不相等返回 true。|[ $a != $b ] 返回 true。
-z|检测字符串长度是否为0，为0返回 true。|[ -z $a ] 返回 false。
-n|检测字符串长度是否为0，不为0返回 true。|[ -z $a ] 返回 true。
str|检测字符串是否为空，不为空返回 true。|[ $a ] 返回 true。
-b file|检测文件是否是块设备文件，如果是，则返回 true。|[ -b $file ] 返回 false。
-c file|检测文件是否是字符设备文件，如果是，则返回 true。|[ -b $file ] 返回 false。
-d file|检测文件是否是目录，如果是，则返回 true。|[ -d $file ] 返回 false。
-f file|检测文件是否是普通文件（既不是目录，也不是设备文件），如果是，则返回 true。|[ -f $file ] 返回 true。
-g file|检测文件是否设置了 SGID 位，如果是，则返回 true。|[ -g $file ] 返回 false。
-k file|检测文件是否设置了粘着位(Sticky Bit)，如果是，则返回 true。|[ -k $file ] 返回 false。
-p file|检测文件是否是具名管道，如果是，则返回 true。|[ -p $file ] 返回 false。
-u file|检测文件是否设置了 SUID 位，如果是，则返回 true。|[ -u $file ] 返回 false。
-r file|检测文件是否可读，如果是，则返回 true。|[ -r $file ] 返回 true。
-w file|检测文件是否可写，如果是，则返回 true。|[ -w $file ] 返回 true。
-x file|检测文件是否可执行，如果是，则返回 true。|[ -x $file ] 返回 true。
-s file|检测文件是否为空（文件大小是否大于0），不为空返回 true。|[ -s $file ] 返回 true。
-e file|检测文件（包括目录）是否存在，如果是，则返回 true。|[ -e $file ] 返回 true。

条件表达式要放在方括号之间，并且要有空格，例如 [$a==$b] 是错误的，必须写成 [ $a == $b ]。

```
a=110
b=220
val=`expr $a \* $b`
echo "a * b : $val"

a=10
b=20
if [ $a -eq $b ]
then
   echo "$a -eq $b : a is equal to b"
else
   echo "$a -eq $b: a is not equal to b"
fi

if [ $a != $b ]
then
   echo "$a != $b : a is not equal to b"
else
   echo "$a != $b: a is equal to b"
fi

a="abc"
b="efg"
if [ $a = $b ]
then
   echo "$a = $b : a is equal to b"
else
   echo "$a = $b: a is not equal to b"
fi

file="${0}"
if [ -r $file ]
then
   echo "File ${file} has read access"
else
   echo "File ${file} does not have read access"
fi
# 输出结果
# a * b : 24200
# 10 -eq 20: a is not equal to b
# 10 != 20 : a is not equal to b
# abc = efg: a is not equal to b
# File ./xx.sh has read access
```

# 判断语句
* 使用if语句的时候进行判断如果是进行数值类的判断，建议使用let(())进行判断，对于字符串等使用test[ ] or [[ ]] 进行判断
* (())中变量是可以不使用$来引用的
* 使用[]要保证每个变量间都要有空格，括号前后也要有空格
* 多个条件判断 && ||
* 最后必须以 fi 来结尾闭合 if，fi 就是 if 倒过来拼写，后面也会遇见。

```
if condition1
then
    command1
elif condition2 
then 
    command2
else
    commandN
fi
    commandN
```
示例：
```
a=10
b=20
if [ $a == $b ]
then
   echo "a 等于 b"
elif [ $a -gt $b ]
then
   echo "a 大于 b"
elif [ $a -lt $b ]
then
   echo "a 小于 b"
else
   echo "没有符合的条件"
fi
   echo "结束"

num1=$[2*3]
num2=$[1+5]
if test $[num1] -eq $[num2]
then
    echo '两个数字相等!'
else
    echo '两个数字不相等!'
fi
```

# 循环语句

### for
```
for 变量 in 列表
do
    command1
    command2
    ...
    commandN
done
```

示例：
```
for loop in 1 2 3 4 5
do
    echo $loop  # 12345
done

for str in 'This is a string'
do
    echo $str # This is a string
done

# 显示主目录下以 .bash 开头的文件：
for FILE in $HOME/.bash*
do
   echo $FILE
done
```

### while

```
while 判断
do
   command
done
```

示例：
```
echo 'type <CTRL-C> to terminate'
echo -n 'enter your name: '
while read FILM
do
    echo "your name: $FILM"
done
```

在循环过程中，有时候需要在未达到循环结束条件时强制跳出循环，像大多数编程语言一样，Shell也使用 break 和 continue 来跳出循环。
特别的 可以通过 break + n 来标识跳出第几层循环，比如：break 2 表示跳出第二层循环

# 函数
像其他编程语言一样，Shell 也支持函数。Shell 函数必须先定义后使用。
* function 是可选的
* 函数返回值，可以显式增加return语句；如果不加，会将最后一条命令运行结果作为返回值。 
* 调用函数只需要给出函数名，不需要加括号。
* 函数返回值在调用该函数后通过 $? 来获得。
* 调用函数时可以向其传递参数。在函数体内部，通过 $n 的形式来获取参数的值，例如，$1表示第一个参数，$2表示第二个参数...
```
function function_name () {
    list of commands
    [ return value ]
}
```

| 特殊变量 | 说明 |
---|---
| $# | 传递给函数的参数个数。 |
| $* | 显示所有传递给函数的参数。 |
| $@ | 与$*相同，但是略有区别，请查看[Shell特殊变量](http://c.biancheng.net/cpp/view/2739.html)。 |
| $? | 函数的返回值。 |

示例：
```
#!/bin/bash
funInput(){
    echo "The function is to get the sum of two numbers..."
    echo -n "Input first number: "
    read aNum
    echo -n "Input another number: "
    read bNum
    funReturn $aNum $bNum 
    return $?
}

funReturn(){
    echo "The two numbers are $1 and $2"
    return `expr ${1} + ${2}`
}

funInput

echo "The sum of two numbers is $?"
```