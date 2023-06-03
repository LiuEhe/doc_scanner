'''
- "app.py" 文件是一个文档扫描仪应用程序的主要入口点。
- 它提供了一个可视化的用户界面，用于加载图片、调整文档角落位置、裁剪文档并显示结果。
- 它的作用是提供一个简单易用的界面，使用户能够方便地进行文档扫描操作。
'''

import tkinter as tk  # 导入 tkinter 库，用于创建 GUI
from tkinter import filedialog  # 从 tkinter 库中导入 filedialog，用于弹出文件选择对话框
from PIL import Image, ImageTk  # 导入 PIL 库，用于处理图片
import cv2 as cv  # 导入 OpenCV 库，用于图片处理和计算机视觉任务
from doc_scanner import DocScanner  # 从 doc_scanner 文件中导入 DocScanner 类
import numpy as np  # 导入 numpy 库，用于进行数值计算


class DocScannerApp:
    def __init__(self):
        self.doc_scanner = DocScanner()  # 创建 DocScanner 类的实例

        self.corners = None  # 初始化识别出文档的四个角落为 None
        self.dragging_idx = -1  # 这个变量用来标记正在被拖动的角落，设置为-1表示现在没有
        self.img = None  # 初始化图片为 None
        
        self.root = tk.Tk()  # 创建一个 Tkinter 窗口

        # 在窗口中创建一个宽600，高400画布
        # 用于把图片和裁剪框绘制上去
        self.canvas = tk.Canvas(self.root, width=600, height=400)  # 创建一个宽600，高400画布  #TODO
        # 将画布添加到窗口中
        #TODO 
        self.canvas.pack()
        
        # 为画布绑定鼠标事件
        # 鼠标左键按下,释放和移动事件都绑定到方法：mouse_callback 上
        # 注意绑定的事是实例方法，不要忘了self
        #TODO  # 鼠标按下事件
        #TODO  # 鼠标释放事件
        #TODO  # 鼠标移动事件

        self.canvas.bind("<ButtonPress-1>", self.mouse_callback)  # 鼠标按下事件
        self.canvas.bind("<ButtonRelease-1>", self.mouse_callback)  # 鼠标释放事件
        self.canvas.bind("<Motion>", self.mouse_callback)  # 鼠标移动事件

        # 创建一个 "Select Image" 按钮，点击时执行 self.select_image 函数
        btn_select = tk.Button(self.root, text="Select Image", command=self.select_image)  
        btn_select.pack(side=tk.LEFT)  # 将按钮添加到窗口左侧

        self.show_mouse_move = tk.BooleanVar()#TODO  # 创建一个 BooleanVar 实例来保存复选框的状态
        # 创建一个复选框，文本为 "Show Mouse Move"，把状态与 self.show_mouse_move 绑定
        chk_show_mouse_move = tk.Checkbutton(self.root, text="Show Mouse Move", variable=self.show_mouse_move)  # 创建一个复选框，文本为 "Show Mouse Move"，把状态与 self.show_mouse_move 绑定#TODO
        chk_show_mouse_move.pack(side=tk.LEFT)  # 将复选框添加到窗口左侧

        # 创建一个 "Crop" 按钮，点击时执行 self.crop 函数
        btn_crop = tk.Button(self.root, text="Crop", command=self.crop)  
        btn_crop.pack(side=tk.RIGHT)  # 将按钮添加到窗口右侧

    def select_image(self):
        """选择图片并加载图片和角落。"""
        file_path = filedialog.askopenfilename()  # 打开文件选择对话框并获取文件路径
        self.img, self.corners = self.doc_scanner.load_image(file_path)  # 加载图片和角落
        img_height, img_width, _ = self.img.shape  # 获取图片的高度和宽度
        if img_height > 600 or img_width > 800:  # 如果图片的高度大于600或宽度大于800
        
            scale = min(600 / img_height, 800 / img_width)#TODO  # 计算缩放比例
            self.img = cv.resize(self.img, None, fx=scale, fy=scale)#TODO  # 缩放图片
            self.corners = self.corners * scale #TODO  # 缩放角落
            img_height, img_width, _ = self.img.shape # 更新图片的高度和宽度
            
        self.canvas.config(width=img_width, height=img_height)  # 调整画布的大小以适应图片
        self.canvas.pack()  # 更新画布
        self.root.geometry(f"{img_width+50}x{img_height+50}")  # 调整窗口的大小以适应画布
        self.redraw()  # 重新绘制图片和角落

    def mouse_callback(self, event):
        """鼠标回调函数，处理鼠标按下、释放和移动事件。"""
        x, y = event.x, event.y  # 获取鼠标位置
        if event.type == tk.EventType.ButtonPress:  # 如果是鼠标按下事件
            print(f"鼠标在({x},{y})按下")
            for idx, corner in enumerate(self.corners):  # 遍历每个角落点
                #TODO:  # 如果鼠标位置和角落的距离小于10
                    if np.linalg.norm(corner - np.array([x, y])) < 10:  # 如果鼠标位置和角落的距离小于10
                        self.dragging_idx = idx  # 设置正在拖动的角落索引值为当前的角落的索引值
                        print(f"要开始拖动角落: corners[{idx}]={corner} , 所以变量: dragging_idx 别设置为 {idx}")
                        break  # 已经找到了要拖动的点，所以跳出循环
        elif event.type == tk.EventType.ButtonRelease:  # 如果是鼠标释放事件
            print(f"鼠标在({x},{y})释放")
            self.dragging_idx = -1
        elif event.type == tk.EventType.Motion:  # 如果是鼠标移动事件
            if(self.show_mouse_move.get()):
                print(f"鼠标在({x},{y})移动")
            if self.dragging_idx != -1:  # 如果正在拖动一个角落
                self.corners[self.dragging_idx] = np.array([x, y])  # 更新该角落的位置
                self.redraw()  # 重新绘制图片和角落

    def redraw(self):
        """重新绘制图片和角落。"""
        img_copy = self.img.copy()  # 复制图片
        for idx, corner in enumerate(self.corners):  # 遍历每个角落
            # 在图片上绘制一个绿色的圆形标记角落的位置
            cv.circle(img_copy, tuple(corner.astype(int)), 5, (0, 255, 0), -1)
            # 在图片上绘制一个绿色的，宽度为2的多边形连接所有角落
            #TODO
            cv.drawContours(img_copy, [self.corners.astype(int)], -1, (0, 255, 0), 2)
            img_tk = self.cv2image_to_tkinter_image(img_copy)  # 将 OpenCV 图片转换为 Tkinter 图片
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)  # 在画布上创建图片
            self.canvas.image = img_tk  # 保存图片，防止被垃圾回收

    def cv2image_to_tkinter_image(self, cv2_image):
        """将 OpenCV 图片转换为 Tkinter 图片。"""
        cv2_image_rgb = cv.cvtColor(cv2_image, cv.COLOR_BGR2RGB)  # 将图片从 BGR 格式转换为 RGB 格式
        pil_image = Image.fromarray(cv2_image_rgb)  # 将数组转换为 PIL 图片
        return ImageTk.PhotoImage(pil_image)  # 将 PIL 图片转换为 Tkinter 图片


    def crop(self):
        """裁剪图片。"""
        cropped_img = self.doc_scanner.crop_image(self.img, self.corners)  # 调用 DocScanner 的 crop_image 方法来裁剪图片
        cropped_img_tk = self.cv2image_to_tkinter_image(cropped_img)  # 将裁剪后的 OpenCV 图片转换为 Tkinter 图片
        cropped_image_window = tk.Toplevel(self.root)  # 在主窗口上创建一个新窗口来显示裁剪后的图片
        cropped_image_window.title("Cropped Image")  # 设置新窗口的标题
        img_label = tk.Label(cropped_image_window, image=cropped_img_tk)  # 在新窗口中创建一个标签来显示裁剪后的图片
        img_label.pack()  # 将标签添加到新窗口中
        btn_close = tk.Button(cropped_image_window, text="Close", command=cropped_image_window.destroy)  # 创建一个 "Close" 按钮，点击时关闭新窗口
        btn_close.pack()  # 将按钮添加到新窗口中
        img_label.image = cropped_img_tk  # 保存图片，防止被垃圾回收

    def run(self):
        """运行应用程序。"""
        self.root.mainloop()  # 启动 Tkinter 事件循环

if __name__ == "__main__":
    app = DocScannerApp()  # 创建 DocScannerApp 类的实例
    app.run()  # 运行应用程序
