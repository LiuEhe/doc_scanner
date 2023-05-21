# doc_scanner

## 项目描述

这个项目是一个文档扫描仪应用程序，使用Python编写。它可以帮助用户加载图片并裁剪文档，提供方便的文档扫描功能。

## 项目运行效果截图


<img src="https://github.com/LiuEhe/doc_scanner/blob/main/result/picture1.jpg" width="350" height="140"><img src="https://github.com/LiuEhe/doc_scanner/blob/main/result/picture2.jpg" width="200" height="140">


## 功能

- 选择图片：通过点击 "Select Image" 按钮选择要加载的图片。
- 裁剪文档：点击 "Crop" 按钮可以裁剪文档，将文档从图片中提取出来。
- 鼠标移动显示：勾选 "Show Mouse Move" 复选框可以在鼠标移动时显示相关信息（如果有实现）。

## 依赖

该项目依赖以下库：

- tkinter：用于创建GUI应用程序。
- PIL：用于处理图片。
- OpenCV：用于图片处理和计算机视觉任务。
- numpy：用于进行数值计算。

可以使用以下命令安装所需依赖：

```bash
pip install opencv-python numpy Pillow
```

## 使用

1. 安装所需依赖（参见上面的依赖部分）。
2. 运行 `app.py` 文件。
3. 点击 "Select Image" 按钮选择要加载的图片。
4. 调整文档的角落位置（如果有实现）。
5. 点击 "Crop" 按钮裁剪文档。
6. 勾选 "Show Mouse Move" 复选框以启用鼠标移动显示（如果有实现）。

## 注意

请注意以下事项：

- 本项目仅支持基于Python的脚本文件。
- 请确保已安装所需的依赖库。
- 鼠标移动显示功能的具体实现可能因代码内容而异，请查看代码了解详细信息。
