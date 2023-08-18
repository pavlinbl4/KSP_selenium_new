import tkinter as tk

result = []


def input_window()->str:
    def confirm_input(event=None):
        # get text input
        text = input_field.get("1.0", 'end-1c')
        result.append(text)
        window.destroy()

    def cancel_input():
        window.destroy()

    # Create window
    window = tk.Tk()

    # Text input field
    input_field = tk.Text(window)
    input_field.grid(row=0, column=0)

    # Bind paste keyboard shortcut
    input_field.bind('<Control-v>', lambda e: input_field.event_generate('<<Paste>>'))

    # Bind enter key to confirm input
    input_field.bind('<Return>', confirm_input)

    # Paste button
    paste_btn = tk.Button(window, text="Paste", command=lambda: input_field.event_generate('<<Paste>>'))
    paste_btn.grid(row=1, column=0)

    # Other buttons
    tk.Button(window, text="Submit", command=confirm_input).grid(row=2, column=0)
    tk.Button(window, text="Cancel", command=cancel_input).grid(row=3, column=0)

    window.mainloop()

    return ''.join(result)


if __name__ == "__main__":
    print(type(input_window()))
