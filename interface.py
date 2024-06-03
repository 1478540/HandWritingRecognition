import tkinter as tk
from tkinter import filedialog, messagebox
import pretreatment
import Recognition


class HandwritingRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("手写数字识别")
        self.root.geometry("800x400")  # 设置窗口的初始大小
        self.root.configure(bg="#f0f0f0")

        # 标题
        self.title_label = tk.Label(root, text="手写数字识别系统", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.pack(pady=20)

        # 创建训练集路径输入框和按钮
        self.create_file_selection_section("训练集文件夹路径:", "构建", self.train_model,default_path="D:/CodeSet/VSCodeCode/Python/HandWritingRecognition1/trainingDigits")

        # 创建测试集路径输入框和按钮
        self.create_file_selection_section("测试集文件夹路径:", "测试", self.test_model,default_path="D:/CodeSet/VSCodeCode/Python/HandWritingRecognition1/testDigits")

        # 创建手写图片路径输入框和按钮
        self.create_file_selection_section("手写图片路径:", "识别", self.recognize_image,default_path="D:/CodeSet/VSCodeCode/Python/HandWritingRecognition1/test.jpg")

    def create_file_selection_section(self, label_text, button_text, command, default_path=""):
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(pady=10, padx=20, fill=tk.X)

        label = tk.Label(frame, text=label_text, font=("Helvetica", 12), bg="#f0f0f0")
        label.pack(side=tk.LEFT, padx=5)
        
        entry = tk.Entry(frame, width=40, font=("Helvetica", 12))
        entry.insert(0, default_path)  # 设置默认值
        entry.pack(side=tk.LEFT, padx=5)

        browse_button = tk.Button(frame, text="浏览", font=("Helvetica", 12), command=lambda e=entry: self.browse_file(e))
        browse_button.pack(side=tk.LEFT, padx=5)
        
        action_button = tk.Button(frame, text=button_text, font=("Helvetica", 12), command=command)
        action_button.pack(side=tk.LEFT, padx=5)

        # 保存 entry 对象以供后续使用
        if command == self.train_model:
            self.train_entry = entry
        elif command == self.test_model:
            self.test_entry = entry
        elif command == self.recognize_image:
            self.image_entry = entry

    def browse_file(self, entry):
        file_path = filedialog.askdirectory()
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, file_path)


    def train_model(self):
        train_path = self.train_entry.get()
        if not train_path:
            messagebox.showerror("错误", "请提供训练集文件夹路径")
            return
        
        Recognition.save_training_data_set(train_path)
        messagebox.showinfo("提示", "训练完毕")



    def test_model(self):
        test_path = self.test_entry.get()
        if not test_path:
            messagebox.showerror("错误", "请提供测试集文件夹路径")
            return

        # 弹出“请等待”的提示窗口
        wait_window = tk.Toplevel(self.root)
        wait_window.title("请等待")
        wait_window.geometry("200x100")
        wait_label = tk.Label(wait_window, text="请等待...", font=("Helvetica", 14))
        wait_label.pack(expand=True)

        self.root.update()

        # 运行 Recognition.handwritingTest(test_path) 函数
        result = Recognition.handwriting_test(test_path)

        # 关闭“请等待”的提示窗口
        wait_window.destroy()

        # 创建一个新的顶级窗口来显示测试结果
        result_window = tk.Toplevel(self.root)
        result_window.title("测试结果")
        result_window.geometry("400x200")

        # 创建一个 Label 来显示结果
        result_label = tk.Label(result_window, text=f"测试总数: {result[0]}\n错误总数: {result[1]}\n错误率: {result[2]}", font=("Helvetica", 12))
        result_label.pack(expand=True)




    def recognize_image(self):
        image_path = self.image_entry.get()
        if not image_path:
            messagebox.showerror("错误", "请提供手写图片路径")
            return
        # 识别图片的逻辑
        result=Recognition.classify_single_file(image_path)

        # 创建一个新的顶级窗口来显示测试结果
        result_window = tk.Toplevel(self.root)
        result_window.title("识别结果")
        result_window.geometry("400x200")

        # 创建一个 Label 来显示结果
        result_label = tk.Label(result_window, text=f"识别出来的数字是: {result}", font=("Helvetica", 12))
        result_label.pack(expand=True)




if __name__ == "__main__":
    root = tk.Tk()
    app = HandwritingRecognitionApp(root)
    root.mainloop()
