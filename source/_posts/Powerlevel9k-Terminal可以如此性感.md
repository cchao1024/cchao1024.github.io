---
title: Powerlevel9k - Terminal可以如此性感
date: 2018-12-22
tags:
---

Powerlevel9k 是使用[Powerline Fonts](https://github.com/powerline/fonts)的ZSH框架主题。

![687474703a2f2f67696679752e636f6d2f696d616765732f70396b6e65772e676966.gif](https://upload-images.jianshu.io/upload_images/1633382-42bbd7c8ac803649.gif?imageMogr2/auto-orient/strip)


# Oh-My-Zsh
## 安装
可以通过 **curl** 或者 **wget** 安装  [Oh-My-Zsh](https://github.com/robbyrussell/oh-my-zsh)
* curl 方式:
```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" 
```
* wget 方式:
```
sh -c "$(wget https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh -O -)"
```

安装结果输出：
```
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)" 
Cloning Oh My Zsh...
Cloning into '/Users/xxxx/.oh-my-zsh'...
remote: Counting objects: 831, done.
remote: Compressing objects: 100% (700/700), done.
remote: Total 831 (delta 14), reused 775 (delta 10), pack-reused 0
Receiving objects: 100% (831/831), 567.67 KiB | 75.00 KiB/s, done.
Resolving deltas: 100% (14/14), done.
Looking for an existing zsh config...
Found ~/.zshrc. Backing up to ~/.zshrc.pre-oh-my-zsh
Using the Oh My Zsh template file and adding it to ~/.zshrc
             __                                     __   
      ____  / /_     ____ ___  __  __   ____  _____/ /_  
     / __ \/ __ \   / __ `__ \/ / / /  /_  / / ___/ __ \ 
    / /_/ / / / /  / / / / / / /_/ /    / /_(__  ) / / / 
    \____/_/ /_/  /_/ /_/ /_/\__, /    /___/____/_/ /_/  
                            /____/                       ....is now installed!
Please look over the ~/.zshrc file to select plugins, themes, and options.
p.s. Follow us at https://twitter.com/ohmyzsh.
p.p.s. Get stickers and t-shirts at http://shop.planetargon.com.
```
## 插件安装
安装 **autosuggestions**
```
git clone https://github.com/zsh-users/zsh-autosuggestions $ZSH_CUSTOM/plugins/zsh-autosuggestions
```
安装 **syntax-highlighting**
```
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```
## 主题

oh my zsh 默认下载了许多主题 可以通过命令
```
ls ~/.oh-my-zsh/themes
```
查看已经下载的主题。
输入命令 **cat ~/.zshrc** 查看当前zsh的配置信息。编辑
```
ZSH_THEME="robbyrussell"
```
就能修改所使用的主题了，通过查看[主题wiki：https://github.com/robbyrussell/oh-my-zsh/wiki/Themes](https://github.com/robbyrussell/oh-my-zsh/wiki/Themes) 可以看到各主题的预览及介绍。
如设置 **ZSH_THEME="random"** 表示使用随机主题，每次打开终端都是不一样的风采。

# Powerlevel9k

## 安装
```
$ git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
```

clone完成后，**sudo vim ~/.zshrc** 修改zsh的主题为powerlevel9k
```
ZSH_THEME="powerlevel9k/powerlevel9k"
```
修改完成 重启终端或 **source ~/.zshrc**。
没错，你发现你的终端出现了一些乱码。那是因为我们还没有安装字体。

## 安装字体

我们有多种方式安装字体，这里使用 **[Nerds](https://github.com/ryanoasis/nerd-fonts/)**

通过 命令把字体下载到本地：
```
# Linux：
mkdir -p ~/.local/share/fonts
cd ~/.local/share/fonts && curl -fLo "Droid Sans Mono for Powerline Nerd Font Complete.otf" https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/DroidSansMono/complete/Droid%20Sans%20Mono%20Nerd%20Font%20Complete.otf
# macOS (OS X)
cd ~/Library/Fonts && curl -fLo "Droid Sans Mono for Powerline Nerd Font Complete.otf" https://github.com/ryanoasis/nerd-fonts/raw/master/patched-fonts/DroidSansMono/complete/Droid%20Sans%20Mono%20Nerd%20Font%20Complete.otf
```
下载完成后，去zsh配置文件修改**powerlevel9k**使用的字体 
```
POWERLEVEL9K_MODE="nerdfont-complete"
```

修改终端所使用的字体为 nerd font
修改完成 重启终端或 **source ~/.zshrc** 使配置生效。
# 其他配置项目
| key                                | value                                          |
| ---------------------------------- | ---------------------------------------------- |
| POWERLEVEL9K_CONTEXT_TEMPLATE      | 最左侧的提示符,默认是 `%n@%m`（用户名@终端名） |
| POWERLEVEL9K_LEFT_PROMPT_ELEMENTS  | 左侧的提示符                                   |
| POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS | 右侧的提示符                                   |
| POWERLEVEL9K_TIME_FORMAT           | 时间格式                                       |
...

## 变量
* battery 电量
* time 时间
* dir 目录
* vcs 版本管理
* ip 当前ip
* ram 内存
  ...

提示符可以通过 Powerlevel9k 提供的变量去替换.

## Sample
```
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS= (dir vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS= (time)
POWERLEVEL9K_DISABLE_RPROMPT=true
POWERLEVEL9K_PROMPT_ON_NEWLINE=true
POWERLEVEL9K_MULTILINE_LAST_PROMPT_PREFIX="▶ "
POWERLEVEL9K_MULTILINE_FIRST_PROMPT_PREFIX=""
```
![image.png](https://upload-images.jianshu.io/upload_images/1633382-1efc3030489b4ef8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


详细的配置项可以看 [官方文档](https://github.com/bhilburn/powerlevel9k/wiki)。
或者 直接复制他人共享的[配置文件](https://github.com/bhilburn/powerlevel9k/wiki/Show-Off-Your-Config)