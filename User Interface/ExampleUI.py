import tkinter as tk
from tkinter import messagebox

class GUI:
    def __init__(self):
        self.root = tk.Tk()

        self.menubar = tk.Menu(self.root)
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="close", command=self.onclosing)
        self.menubar.add_cascade(menu=self.filemenu, label="file")
        self.root.config(menu=self.menubar)

        self.label = tk.Label(self.root, text="words", font=("Arial", 18))
        self.label.pack(padx=10, pady=10)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 18), background="red")
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        self.check_state = tk.IntVar()
        self.check = tk.Checkbutton(self.root, text="show message box", font=("Arial", 18), variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        self.button = tk.Button(self.root, text="show message", font=("Arial", 18), command=self.show_message)
        self.button.pack(padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.onclosing)

        self.root.mainloop()

    def show_message(self):
        if self.check_state.get() == 0:
            print(self.textbox.get("1.0", tk.END))
        else:
            messagebox.showinfo(title="message", message=self.textbox.get("1.0", tk.END))

    def shortcut(self, event):
        if event.keysym == "Return":
            print("Hello")

    def onclosing(self):
        if messagebox.askyesno(title="Quit?", message="Are you sure??"):
            self.root.destroy()
        else:
            pass


GUI()