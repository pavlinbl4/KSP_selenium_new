import tkinter as tk
from tkinter import Text, WORD


def get_input_data():
    category_dict = {'Культура': '1000000', 'Правосудие': '2000000', 'Происшествия и конфликты': '3000000',
                     'Экономика и бизнес': '4000000', 'Образование': '5000000', 'Экология': '6000000',
                     'Медицина': '7000000', 'Светская жизнь': '8000000', 'Досуг, туризм и отдых': '10000000',
                     'Политика': '11000000', 'Религия': '12000000', 'Наука': '13000000', 'Общество': '14000000',
                     'Спорт': '15000000', 'Армия и ВПК': '16000000', 'Окружающая среда': '18000000'}

    selected_words = []
    words = [k for k in category_dict.keys()]

    def submit_category():
        for i, kword in enumerate(words):
            if checkboxes[i].get() == 1:
                selected_words.append(kword)
        input_window.quit()


    # Create a new Tkinter window
    input_window = tk.Tk()

    # Set the title of the window
    input_window.title("Shoot caption")
    input_window.resizable(False, False)

    # Добавляем логику чтобы окно было по центру экрана
    window_height = 650
    window_width = 800
    screen_width = input_window.winfo_screenwidth()
    screen_height = input_window.winfo_screenheight()
    x = int(screen_width / 4 - window_width / 2)
    y = int(screen_height / 2 - window_height / 2)
    input_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create a label for the input field
    input_label = tk.Label(input_window, text="Enter the shoot caption:")
    input_label.place(x=520, y=5)

    # old version
    tk.Entry(input_window, width=50)
    input_field = Text(wrap=WORD, font=("Arial", 20), background="#abdbe3")  # #abdbe3     #f4dca8
    input_field.place(x=400, y=35, width=380, height=530)

    checkboxes = []

    label = tk.Label(text="Category")
    label.pack(anchor='w', padx=50, pady=5)
    for x, word in enumerate(words):
        var = tk.IntVar()
        checkbox = tk.Checkbutton(text=word.strip(), variable=var, onvalue=1, offvalue=0)
        checkbox.pack(anchor='w', padx=20, pady=5)
        checkboxes.append(var)

        # Create a button to submit the data
    submit_button = tk.Button(input_window, text="Submit", command=submit_category, height=1, width=10)
    submit_button.pack(side='bottom', pady=10, anchor='center')
    submit_button.pack()

    # Start the main event loop for the window
    input_window.mainloop()

    # Get the entered data from the input field
    input_text = input_field.get("1.0", 'end-1c')

    # Destroy the window after it has been submitted
    input_window.destroy()

    # Return the entered data
    # return input_data
    return input_text, category_dict[selected_words[0]]


if __name__ == '__main__':
    print(get_input_data())
