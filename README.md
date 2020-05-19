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

3. Startup

![](./src/README/Interface.png)
```shell
$ python detectVideo.py
```

4. Choose the Video

![](./src/README/VideoChosen.png)

5. Run

![](./src/README/run.png)

* 视频选择后，检测开始；
* `Pause` 按钮 可暂停检测；
* `Stop` 按钮 可提前结束检测；

![视频播放完毕](./src/README/play-Completed.png)

6. 视频裁剪

* 点击"Cut", 选择视频输出文件夹地址

![](./src/README/cut.png)
![](./src/README/cut-1.png)

* 视频裁剪中... (稍作等待)

![](./src/README/wait-for-cut.png)

* 裁剪完成

![](./src/README/cut-Completed.png)

裁剪完毕后，可在上述选择的视频输出文件夹中查看裁剪的片段视频

#### 相关参考

* [handtracking](https://github.com/victordibia/handtracking)