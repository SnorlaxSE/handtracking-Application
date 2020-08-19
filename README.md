# handtracking-Application

> Cut gesture language Video

### Download

#### Linux or Mac OS

```shell
$ git clone https://github.com/SnorlaxSE/handtracking-Application.git
```

#### Windows

将`handtracking-Application.zip`压缩包解压至 `D 盘` 下任一位置 （切记，必须是`D 盘`，因为后续批处理文件相关内容中默认该压缩包解压至`D 盘`；否则，需要使用者手动编辑后续提及的批处理文件中的相关配置） 以防麻烦，建议遵从此设定

### Build run environment 

#### Linux or Mac OS
```shell
$ cd handtracking-Application/
$ pip install -r requirement.txt
```

#### Windows

* 前记：

i. 执行下述命令前，可随意将`handtracking-Application.zip`压缩包解压生成的文件（`handtracking-Application`文件夹）移动至 `D盘`下任一位置，确认`handtracking-Application`文件夹已放置于D盘下`合适的位置`;
ii. 此Repository中未放置Anaconda安装包（占用存储空间过大），请自行在[Anaconda官网下载](https://www.anaconda.com/products/individual) Windows 64-Bit Graphical Installer，并放置于`./software`文件夹下.


依次双击`1-Installation-conda.bat`; `2-Installation-env.bat`; `3-Installation-pkg.bat`; 

a) 1-Installation-conda.bat

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/slient_install_anaconda.png)

正在安装Anaconda，大致需耗时1.5min （稍作等待） ↑

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/slient_install_anaconda_completed.png)

出现“请按任意键继续...”，说明`1-Installation-conda.bat`指令已执行完毕，此时关闭命令行界面即可

b) 2-Installation-env.bat

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/create_env_1.png)

稍作等待... ↑ 


![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/create_env_2.png)

出现上面这个界面，为正常；若未出现，则原因为网络连接不稳定，需关闭窗口，重新双击`2-Installation-env.bat`，直至界面如上图所示；

此时，输入 `y`，按`回车键` ↓

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/create_env_2_1.png)

稍作等待... 

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/create_env_2_2.png)

此时，出现“请按任意键继续...”，说明`2-Installation-env.bat`指令已执行完毕，此时关闭命令行界面即可

c) 3-Installation-pkg.bat

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/install_pkg_1.png)

上图为正常执行界面，下载速度大致 1MB/s，稍作等待即可完成；
如若下载速度过慢，可关闭窗口，重新双击`3-Installation-pkg.bat`；如若下载速度一直很慢，请检查本地网路带宽信息

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/install_pkg_2.png)

此时，出现“请按任意键继续...”，说明`3-Installation-pkg.bat`指令已执行完毕，此时关闭命令行界面即可

d) 4-Installation-ffmpeg.bat

右键`4-Installation-ffmpeg.bat` "以管理员身份运行" （切记，需以管理员身份运行，双击运行 权限不足 部分指令无法生效）

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/set_ffmpeg.png)

此时，出现”成功：指定的值已得到保存“以及“请按任意键继续...”，说明`4-Installation-ffmpeg.bat`指令已执行完毕，此时关闭命令行界面即可

* 后记：由于使用批处理文件执行环境配置指令（方便使用者操作），`handtracking-Application`文件夹位置不可移动，否则部分系统环境变量路径指向失效，工具无法成功生成输出文件；

### RUN

#### Linux or Mac OS
![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/Interface.png)
```shell
$ python detectVideo.py
```

* 如若视频中演示者放下的手仍出现在视野中，则执行下述指令
```shell
$ python detectVideo.py  --crop true
```

#### Windows

鼠标双击 `run.bat`

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/win_run.png)

可选操作：
1）右键`run.bat`，点击"创建快捷方式"；
2）移动生成的快捷方式至合适的位置，如`桌面`；
3）重命名快捷方式为合适的名称，如`handtrack-Application.bat`；
4）双击`handtrack-Application.bat`

### Usage
1. Choose the Video

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/VideoChosen.png)

2. Run

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/run.png)

* 视频选择后，检测开始；
* `Pause` 按钮 可暂停检测；
* `Stop` 按钮 可提前结束检测；

![视频播放完毕](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/play-Completed.png)

3. 视频裁剪

* 点击"Cut", 选择视频输出文件夹地址

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/cut.png)
![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/cut-1.png)

* 视频裁剪中... (稍作等待)

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/wait-for-cut.png)

* 裁剪完成

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/cut-Completed.png)

裁剪完毕后，可在上述选择的视频输出文件夹中查看裁剪的片段视频

#### 相关参考

* [handtracking](https://github.com/victordibia/handtracking)
