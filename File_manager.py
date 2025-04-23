import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import platform


class FileManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Файловый менеджер")
        self.root.geometry("900x600")

        self.current_path = os.getcwd()
        self.create_widgets()
        self.update_file_list()

    def create_widgets(self):
        self.path_frame = ttk.Frame(self.root)
        self.path_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(self.path_frame, text="Путь:").pack(side=tk.LEFT)
        self.path_entry = ttk.Entry(self.path_frame, width=70)
        self.path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.path_entry.insert(0, self.current_path)

        ttk.Button(self.path_frame, text="Обзор", command=self.browse_folder).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.path_frame, text="Назад", command=self.go_up).pack(side=tk.LEFT)

        self.tree = ttk.Treeview(
            self.root,
            columns=("Name", "Type", "Size"),
            show="headings",
            selectmode="browse"
        )
        self.tree.heading("Name", text="Имя")
        self.tree.heading("Type", text="Тип")
        self.tree.heading("Size", text="Размер (КБ)")
        self.tree.column("Size", width=100, anchor="e")
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)


        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)


        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Return>", self.on_double_click)

    def update_file_list(self):
        self.tree.delete(*self.tree.get_children())

        try:
            items = os.listdir(self.current_path)
            for item in items:
                full_path = os.path.join(self.current_path, item)
                if os.path.isdir(full_path):
                    self.tree.insert("", tk.END, values=(item, "Папка", ""))
                else:
                    size_kb = os.path.getsize(full_path) // 1024
                    self.tree.insert("", tk.END, values=(item, "Файл", f"{size_kb} КБ"))

            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, self.current_path)

        except PermissionError:
            messagebox.showerror("Ошибка", "Нет доступа к папке!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список: {e}")

    def go_up(self):
        parent_dir = os.path.dirname(self.current_path)
        if parent_dir != self.current_path:
            self.current_path = parent_dir
            self.update_file_list()

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.current_path)
        if folder:
            self.current_path = folder
            self.update_file_list()

    def on_double_click(self, event):
        selected_item = self.tree.focus()
        item_data = self.tree.item(selected_item)
        item_name, item_type = item_data["values"][0], item_data["values"][1]
        full_path = os.path.join(self.current_path, item_name)

        if item_type == "Папка":
            self.current_path = full_path
            self.update_file_list()
        else:
            self.open_file(full_path)

    def open_file(self, file_path):

        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            elif platform.system() == "Darwin":
                subprocess.run(["open", file_path])
            else:
                subprocess.run(["xdg-open", file_path])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = FileManagerApp(root)
    root.mainloop()