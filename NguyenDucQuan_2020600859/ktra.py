#Ý TƯỞNG
#THÊM NÚT CHỌN ẢNH, XỬ LÝ ẢNH, XOAY ẢNH, PHÓNG TO, THU NHỎ, NỔI BẬT ĐƯỜNG VIỀN BẰNG Laplacian
#CÓ NÚT LƯU KẾT QUẢ SAU KHI XỬ LÝ ẢNH

import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

#TẠO LỚP XỬ LÝ ẢNH
class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("XỬ LÝ ẢNH")

        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.zoom_scale = 0

        self.create_widgets()
#TẠO GIAO DIỆN
    def create_widgets(self):
        # Buttons
        self.load_button = tk.Button(self.root, text="CHỌN ẢNH", command=self.load_image)
        self.load_button.pack(pady=10)

        self.process_button = tk.Button(self.root, text="XỬ LÝ ẢNH", command=self.process_image)
        self.process_button.pack(pady=10)

        self.rotate_label = tk.Label(self.root, text="Xoay ảnh:")
        self.rotate_label.pack()

        self.rotate_value = tk.StringVar(self.root)
        self.rotate_value.set("0")  # Góc xoay mặc định là 0 độ

        self.rotate_combobox = ttk.Combobox(self.root, textvariable=self.rotate_value, values=["0", "90", "180", "270"])
        self.rotate_combobox.pack()

        self.rotate_button = tk.Button(self.root, text="XOAY", command=self.rotate_image)
        self.rotate_button.pack(pady=10)

        self.zoom_label = tk.Label(self.root, text="Phóng to/Thu nhỏ:")
        self.zoom_label.pack()

        self.zoom_slider = tk.Scale(self.root, from_=0.1, to=3.0, resolution=0.1, orient=tk.HORIZONTAL,
                                    command=self.zoom_image, length=200)
        self.zoom_slider.set(1.0)
        self.zoom_slider.pack()

        self.edge_button = tk.Button(self.root, text="NỔI BẬT ĐƯỜNG VIỀN", command=self.detect_edges)
        self.edge_button.pack(pady=10)

        self.save_button = tk.Button(self.root, text="LƯU KẾT QUẢ", command=self.save_image)
        self.save_button.pack(pady=10)

        self.canvas = tk.Canvas(self.root)
        self.canvas.pack()
#CẢI TIẾN CÓ THỂ CHỌN ẢNH
    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if file_path:
            image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            if image is not None:
                self.image_path = file_path
                self.original_image = image
                self.display_image(self.original_image)
            else:
                messagebox.showerror("LỖI", "KHÔNG THỂ ĐỌC ẢNH.")
#HÀM XỬ LÝ ẢNH
    def process_image(self):
        if self.original_image is None:
            messagebox.showwarning("CẢNH BÁO", "HÃY CHỌN ẢNH TRƯỚC KHI ẤN XỬ LÝ.")
            return

        smoothed_image = self.smooth_image(self.original_image)
        sobel_horizontal = cv2.Sobel(smoothed_image, cv2.CV_64F, 1, 0, ksize=5)
        sobel_vertical = cv2.Sobel(smoothed_image, cv2.CV_64F, 0, 1, ksize=5)

        cv2.imshow('Original', self.original_image)
        cv2.imshow('Sobel_horizontal', sobel_horizontal)
        cv2.imshow('Sobel_vertical', sobel_vertical)

        self.processed_image = sobel_horizontal
#CẢI TIẾN CÓ THỂ SAVE ẢNH SAU KHI XỬ LÝ
    def save_image(self):
        if self.processed_image is None:
            messagebox.showwarning("CẢNH BÁO", "HÃY XỬ LÝ ẢNH TRƯỚC KHI LƯU.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if save_path:
            cv2.imwrite(save_path, self.processed_image)
#HÀM LÀM MỊN BẰNG Gaussian
    def smooth_image(self, image):
        if image is not None:
            smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)
            return smoothed_image
#CẢI TIẾN CÓ THỂ XOAY HÌNH ẢNH ĐỂ DỄ QUAN SÁT
    def rotate_image(self):
        if self.original_image is None:
            messagebox.showwarning("CẢNH BÁO", "HÃY CHỌN ẢNH TRƯỚC KHI XOAY.")
            return

        angle = int(self.rotate_combobox.get())
        rows, cols = self.original_image.shape[:2]
        center = (cols // 2, rows // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
        rotated_image = cv2.warpAffine(self.original_image, rotation_matrix, (cols, rows))

        self.original_image = rotated_image
        self.display_image(self.original_image)
#CẢI TIẾN CÓ THỂ ZOOM IN/OUT ĐỂ DỄ QUAN SÁT SAU KHI XỬ LÝ
    def zoom_image(self, value):
        self.zoom_scale = float(value)
        scaled_width = int(self.original_image.shape[1] * self.zoom_scale)
        scaled_height = int(self.original_image.shape[0] * self.zoom_scale)
        resized_image = cv2.resize(self.original_image, (scaled_width, scaled_height))

        self.display_image(resized_image)
#HÀM PHÁT HIỆN VIỀN BỘ LỌC Laplacian
    def detect_edges(self):
        if self.original_image is None:
            messagebox.showwarning("CẢNH BÁO", "HÃY CHỌN ẢNH TRƯỚC KHI PHÁT HIỆN ĐƯỜNG VIỀN.")
            return

        edges = cv2.Laplacian(self.original_image, cv2.CV_64F)
        self.display_image(edges)
#HÀM MÀN HÌNH
    def display_image(self, image):
        if image is not None:
            image = cv2.cvtColor(image, cv2.IMREAD_COLOR)
            image = Image.fromarray(image)
            photo = ImageTk.PhotoImage(image=image)
            self.canvas.config(width=photo.width(), height=photo.height())
            self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.canvas.image = photo


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
