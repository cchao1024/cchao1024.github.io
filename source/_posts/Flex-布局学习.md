---
title: Flex 布局学习
tags: 未定义
categories: Web技术
date: 2019-07-16 10:05:28
---

# 盒(Box) 模型

当你的浏览器展现一个元素时，这个元素会占据一定的空间。这个空间由四部分组成。

中间是*元素*呈现内容的区域。这个区域的外面是*内边距*。再外面是*边框*。最外面的是*外边距*，外边距将该元素与其它元素分开。

依赖 [display](https://developer.mozilla.org/en-US/docs/Web/CSS/display)属性 + [position](https://developer.mozilla.org/en-US/docs/Web/CSS/position)属性 + [float](https://developer.mozilla.org/en-US/docs/Web/CSS/float)属性 实现复杂布局

![](../images/2019-7/blog20190716101102.png)



```css
h3 {
  border-top: 4px solid #7c7; /* 中绿 */
  background-color: #efe;     /* 浅绿 */
  color: #050;                /* 深绿 */
  }
img {border: 2px solid #ccc;}

```



# Flex 布局

Flex是Flexible Box的缩写，意为”弹性布局”，用来为盒状模型提供最大的灵活性。

任何一个容器都可以指定为Flex布局。

Webkit内核的浏览器，必须加上-webkit前缀。

![image-20190716101927006](../images/2019-7/image-20190716101927006.png)

## 名词

- flex container:  Flex 容器
- flex item:  Flex 项目，容器成员
- main axis:  主轴， 项目默认沿主轴排列
- cross axis:  交叉轴

单个项目占据的主轴空间叫做main size，占据的交叉轴空间叫做cross size

## 容器属性

- flex-direction:  决定主轴的方向
  - row（默认）   主轴为水平方向，起点在左端
  - row-reverse    主轴为水平方向，起点在右端
  - column
  - column-reverse  主轴为垂直方向，起点在下沿
- flex-wrap:  决定换行 nowrap(默认) | wrap | wrap-reverse(换行且第一行在下方。）
- flex-flow:  是flex-direction属性和flex-wrap属性的简写形式，默认值为row nowrap。
- justify-content:  定义了项目在主轴上的对齐方式。
  - flex-start（默认值）：左对齐 ,  flex-end（右对齐），center（居中）
  - space-between：两端对齐，项目之间的间隔都相等。
  - space-around：每个项目两侧的间隔相等。所以，项目之间的间隔比项目与边框的间隔大一倍。
- align-items:  定义项目在交叉轴上如何对齐。
  - flex-start：交叉轴的起点对齐。flex-end(终点对齐), center(中点对齐)
  - baseline: 项目的第一行文字的基线对齐。
  - stretch（默认值）：如果项目未设置高度或设为auto，将占满整个容器的高度。

## 项目属性

- order:  排列顺序。数值越小，排列越靠前，默认为0。
- flex-grow:  放大比例，默认为0，即如果存在剩余空间，也不放大。
- flex-shrink:  缩小比例，默认为1，即如果空间不足，该项目将缩小。
- flex-basis:  在分配多余空间之前，项目占据的主轴空间（main size）。浏览器根据这个属性，计算主轴是否有多余空间。它的默认值为auto，即项目的本来大小。
- flex:  是flex-grow, flex-shrink 和 flex-basis的简写，默认值为0 1 auto。后两个属性可选。
- align-self:  单个项目有与其他项目不一样的对齐方式，可覆盖align-items属性。默认值为auto，表示继承父元素的align-items属性，如果没有父元素，则等同于stretch。



# Reference

[<https://www.runoob.com/w3cnote/flex-grammar.html>](https://www.runoob.com/w3cnote/flex-grammar.html)

[<https://developer.mozilla.org/zh-CN/docs/Web/Guide/CSS/Getting_started/Boxes>](https://developer.mozilla.org/zh-CN/docs/Web/Guide/CSS/Getting_started/Boxes)