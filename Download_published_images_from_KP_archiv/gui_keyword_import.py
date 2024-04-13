import tkinter as tk
import time

from Download_published_images_from_KP_archiv.download_my_ksp_images import main_kp_downloader


def enter_keyword():
    keyword = []

    root = tk.Tk()
    root.title("Enter keyword")

    def start_operation():
        keyword.append(entry.get())
        root.destroy()
        return keyword

    # Установка размера окна
    root.geometry("400x200")

    # Размещение окна в центре экрана
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width / 2 - window_width / 2)
    center_y = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

    entry = tk.Entry(root, width=50)
    entry_label = tk.Label(root, text="Enter keyword")
    entry_label.pack(pady=15)
    entry.pack(pady=1)

    # Кнопка для начала операции
    start_button = tk.Button(root, text="Start", command=start_operation)
    start_button.pack(pady=10)

    root.mainloop()

    return keyword[0] if keyword else None


def main_function():
    keyword_from_enter_keyword = enter_keyword()
    if keyword_from_enter_keyword:
        shoot_id = ''
        download_dir = f'/Volumes/big4photo-4/selenium_downloads/keyword_{keyword_from_enter_keyword}'
        main_kp_downloader(shoot_id, download_dir, keyword_from_enter_keyword)


if __name__ == "__main__":
    main_function()
