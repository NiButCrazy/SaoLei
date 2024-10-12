# 扫雷小游戏
![Static Badge](https://img.shields.io/badge/%E8%AF%AD%E8%A8%80-python-blue?logo=python)
![Static Badge](https://img.shields.io/badge/%E5%BC%95%E6%93%8E-pygame-yellow)
![Static Badge](https://img.shields.io/badge/license-MIT-purple)
![GitHub contributors](https://img.shields.io/github/contributors/NiButCrazy/SaoLei?label=%E8%B4%A1%E7%8C%AE%E8%80%85)
![GitHub Release](https://img.shields.io/github/v/release/NiButCrazy/SaoLei?display_name=release&label=%E6%9C%80%E6%96%B0%E5%8F%91%E5%B8%83)
![GitHub last commit](https://img.shields.io/github/last-commit/NiButCrazy/SaoLei?label=%E4%B8%8A%E6%AC%A1%E6%8F%90%E4%BA%A4)


## 简介
练手，初学pygame，项目是做不完的，功能是越做越多的，逻辑动画效果是占了90%的，游戏是没做多少的
，感觉自己写的某些模块代码亿点点点乱，基本是想到什么就加什么，就先这样了，尤其是`eventManager`事件模块，已经顺带`UIBase`模块重构好几次了

## 最大的失误
以前没做过这种东西，以为帧率是固定的一个数，不会变化，结果发现帧数是动态的，每次刷新都会改变，必须要用pygame的`clock`模块来控制帧数，
这就导致了我这个用`time.sleep()`来控制帧率的行为像个傻逼，UI的所有过渡动画在原理上就错了

## 版本
>释放版本:`v2.0.1`  
>Beta版本:`v2.0.1-Beta`



## 语言
>Python

## 依赖库
>- pygame  
>- random

## 贡献者
![https://github.com/NiButCrazy/SaoLei/graphs/contributors](https://contrib.rocks/image?repo=NiButCrazy/SaoLei)