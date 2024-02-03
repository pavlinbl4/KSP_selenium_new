import tkinter as tk
from tkinter import Text, WORD


def get_input_data():
    # function inserts the clipboard content into the Text widget:
    def paste():
        input_field.insert('insert', input_window.clipboard_get())

    # Create a new Tkinter window
    input_window = tk.Tk()

    # Set the title of the window
    input_window.title("Shoot Caption")
    input_window.resizable(False, False)

    # Center the window
    window_height = 200
    window_width = 400
    screen_width = input_window.winfo_screenwidth()
    screen_height = input_window.winfo_screenheight()
    x = int(screen_width / 2 - window_width / 2)
    y = int(screen_height / 2 - window_height / 2)
    input_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a label for the input field
    input_label = tk.Label(input_window, text="Enter the shoot caption:")
    input_label.pack()

    # Create a multi-line text field for the input data
    input_field = Text(
        input_window,
        wrap=WORD,
        font=("Arial", 20),
        background="#abdbe3",
        width=38,
        height=20,
    )
    input_field.pack(padx=10, pady=10)

    # Bind paste keyboard shortcut
    input_field.bind('<Control-v>', paste)

    # Create a submit button
    submit_button = tk.Button(
        input_window,
        text="Submit",
        command=lambda: input_window.destroy(),
        height=1,
        width=10,
    )
    submit_button.pack(side="bottom", pady=10, anchor="center")

    # Start the main event loop for the window
    input_window.mainloop()

    # Get the entered data from the Text widget
    input_text = input_field.get("1.0", "end-1c")

    # Destroy the window after finishing
    input_window.destroy()

    # Return the entered data
    return input_text


if __name__ == "__main__":
    print(get_input_data())
