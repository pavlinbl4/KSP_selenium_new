from tkinter import filedialog, messagebox, Tk, Label, Button
from tkinter import font


def display_info(info):
    root = Tk()
    root.title("Information Window")

    # Set window size
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int(screen_width / 4)
    y = int(screen_height / 2 - window_height / 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Set font
    custom_font = font.Font(family="Didot", size=24)

    # Add label with specified font and color
    label = Label(root, text=info, font=custom_font, fg="green")
    label.pack(pady=20)

    # Add close button
    button = Button(root, text="Close", command=root.destroy)
    button.pack(pady=40)

    # Start the main loop
    root.mainloop()


def select_folder_via_gui():
    root = Tk()
    root.withdraw()

    choose_folder = filedialog.askdirectory(
        initialdir='/Volumes/big4photo-4/EDITED_JPEG_ARCHIV/Downloaded_from_fotoagency',
        title="Select your Source directory")
    if len(choose_folder) > 0:
        return choose_folder
    else:
        messagebox.showwarning("Warning", "You haven't chosen a folder. Program terminated.")
        root.destroy()


if __name__ == '__main__':
    # display_info("NO KEYWORDS FOR WORK")
    select_folder_via_gui()
