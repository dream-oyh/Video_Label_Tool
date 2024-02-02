# Video_Label_Tool

# RUN

```sh
git clone git@github.com:dream-oyh/Video_Label_Tool.git
cd Video_Label_Tool
poetry install
poetry run python main.py
```

# Usage

## 打开文件

从左上角“打开文件”按钮导入待处理视频，按钮旁会显示已打开视频的绝对路径

处于设计的方便，本程序在打开视频后会自动播放 3 秒，作为第一分段

## 间隔步长

间隔步长用于控制视频分段的时间间隔，单位为秒，默认值为 3

## “Load Prev”按钮

回到上一个视频重新分类，如果当前视频是第一个视频，则无法使用该按钮

## “Load Next”按钮

跳转到下一个视频分类，如果当前视频是最后一个视频，则无法使用该按钮

## “Reload”按钮

重新播放本分段视频

## “Save”按钮

在右上角的标签栏中选择对应标签后，可通过“Save”按钮将分段文件保存至指定文件夹中（本按钮功能待优化，“Save”按钮按下后有一定的卡顿）

# 标签文件夹的说明

本程序会自动根据需要的标签，在程序运行文件夹下创建 label*folder 文件夹，并在其中创建以各个标签命名的子文件夹，每个子文件夹中存放着对应标签的视频分段，视频分段的命名为“标签名*分段序号.avi”

# 标签更改

若需要对标签进行更改，需要进入 `core/ui.py`，对 `MyFrame` 类中的 `option` 列表进行更改，标签顺序决定了 `core/app.py` 源码的 `save_segment` 函数中，`option_num` 对应的值，并且 `save_segment` 函数中各 `case` 存储路径也要随之调整
