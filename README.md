# handtracking-Application

1. Download

```shell
$ git clone https://github.com/SnorlaxSE/handtracking-Application.git
```

2. Dependency
```shell
$ cd handtracking-Application/
$ pip install -r requirement.txt
```

* 如若是Windows操作系统，需手动安装FFMPEG，可参考[ffmpeg Windows安装及命令使用](https://blog.csdn.net/kaikai136412162/article/details/80746961)

3. Startup

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/Interface.png)
```shell
$ python detectVideo.py
```

* 如若视频中演示者放下的手仍出现在视野中，则执行下述指令
```shell
$ python detectVideo.py  --crop true
```

4. Choose the Video

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/VideoChosen.png)

5. Run

![](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/run.png)

* 视频选择后，检测开始；
* `Pause` 按钮 可暂停检测；
* `Stop` 按钮 可提前结束检测；

![视频播放完毕](https://cdn.jsdelivr.net/gh/SnorlaxSE/Photo-CDN@master/github/handtracking-Application/play-Completed.png)

6. 视频裁剪

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
