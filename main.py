import os
import tkinter as tk
from tkinter import Menu, filedialog
from tkinter import ttk, messagebox
from utils.ascii_art import generate_ascii_art
from utils.anagram import generate_anagrams


class App:
    def __init__(self, root):
        self.root = root
        self.root.geometry('1200x800')  # Increase the size of the main window.
        self.root.title('ASCII Art and Anagram Generator')

        # Create a menu bar
        self.menu_bar = Menu(root)
        self.root.config(menu=self.menu_bar)

        # Create a file menu
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Save ASCII Art", command=self.save_ascii_art)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Create a theme menu
        self.theme_menu = Menu(self.menu_bar, tearoff=0)
        self.theme_menu.add_command(label="Default", command=lambda: self.change_theme('default'))
        self.theme_menu.add_command(label="Dark", command=lambda: self.change_theme('dark'))
        self.theme_menu.add_command(label="Light", command=lambda: self.change_theme('light'))
        self.theme_menu.add_command(label="Green", command=lambda: self.change_theme('green'))
        self.menu_bar.add_cascade(label="Theme", menu=self.theme_menu)

        # Create frames
        self.ascii_frame = tk.LabelFrame(root, text='ASCII Art')  # ttk.LabelFrame replaced by tk.LabelFrame
        self.ascii_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.anagram_frame = tk.LabelFrame(root, text='Anagrams')  # ttk.LabelFrame replaced by tk.LabelFrame
        self.anagram_frame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        self.create_ascii_art_frame()
        self.create_anagram_frame()

    # Add theme changing function
    def change_theme(self, theme):
        if theme == 'dark':
            self.root.configure(bg='black')
            self.ascii_frame.configure(bg='black', fg='white')
            self.anagram_frame.configure(bg='black', fg='white')
            self.ascii_art_text.configure(bg='black', fg='green')  # Green text on black background
            self.anagrams_listbox.configure(bg='black', fg='green')  # Green text on black background
        elif theme == 'light':
            self.root.configure(bg='white')
            self.ascii_frame.configure(bg='white', fg='black')
            self.anagram_frame.configure(bg='white', fg='black')
            self.ascii_art_text.configure(bg='white', fg='black')  # Black text on white background
            self.anagrams_listbox.configure(bg='white', fg='black')  # Black text on white background
        elif theme == 'green':
            self.root.configure(bg='dark green')
            self.ascii_frame.configure(bg='dark green', fg='white')
            self.anagram_frame.configure(bg='dark green', fg='white')
            self.ascii_art_text.configure(bg='dark green', fg='white')  # White text on dark green background
            self.anagrams_listbox.configure(bg='dark green', fg='white')  # White text on dark green background
        else:
            self.root.configure(bg='SystemButtonFace')
            self.ascii_frame.configure(bg='SystemButtonFace', fg='SystemWindowText')
            self.anagram_frame.configure(bg='SystemButtonFace', fg='SystemWindowText')
            self.ascii_art_text.configure(bg='SystemWindow',
                                          fg='SystemWindowText')  # System default text and background colors
            self.anagrams_listbox.configure(bg='SystemWindow',
                                            fg='SystemWindowText')  # System default text and background colors

    def create_ascii_art_frame(self):
        self.text_var = tk.StringVar()
        self.style_var = tk.StringVar()

        styles = ['block', 'banner', 'standard', 'lean', 'mini', 'small', 'big']

        # Create and place labels, entry field and dropdown menu for ASCII Art frame
        ttk.Label(self.ascii_frame, text='Enter Text:').grid(row=0, column=0, sticky='w')
        ttk.Entry(self.ascii_frame, textvariable=self.text_var, width=60).grid(row=0, column=1, sticky='ew')
        # Increase the width of the text entry field

        ttk.Label(self.ascii_frame, text='Choose Style:').grid(row=1, column=0, sticky='w')
        ttk.Combobox(self.ascii_frame, textvariable=self.style_var, values=styles, width=57).grid(row=1, column=1,
                                                                                                  sticky='ew')
        # Increase the width of the style dropdown menu

        # Create and place generate button
        ttk.Button(self.ascii_frame, text='Generate ASCII Art', command=self.generate_ascii).grid(row=2, column=0,
                                                                                                  columnspan=2)

        # Create frame to hold Text widget and Scrollbar
        self.ascii_art_frame = tk.Frame(self.ascii_frame)
        self.ascii_art_frame.grid(row=3, column=0, columnspan=2, sticky='nsew')

        # Create Text widget and Scrollbar and put them in the frame
        self.ascii_art_text = tk.Text(self.ascii_art_frame, width=100, height=30, wrap='none')
        # Increase the size of the ASCII art result area

        self.ascii_art_scrollbar = tk.Scrollbar(self.ascii_art_frame, orient='horizontal',
                                                command=self.ascii_art_text.xview)

        # Connect Scrollbar to Text widget
        self.ascii_art_text['xscrollcommand'] = self.ascii_art_scrollbar.set

        # Grid the Text widget and Scrollbar
        self.ascii_art_text.grid(row=0, column=0, sticky='nsew')
        self.ascii_art_scrollbar.grid(row=1, column=0, sticky='ew')

        self.ascii_art_frame.grid_columnconfigure(0, weight=1)
        self.ascii_art_frame.grid_rowconfigure(0, weight=1)

        self.ascii_frame.grid_columnconfigure(1, weight=1)
        self.ascii_frame.grid_rowconfigure(3, weight=1)

    def create_anagram_frame(self):
        self.chars_var = tk.StringVar()
        self.size_var = tk.IntVar(value=1)
        self.num_var = tk.IntVar(value=1)

        # Create and place labels, entry field and spinboxes for Anagram frame
        ttk.Label(self.anagram_frame, text='Enter Characters:').grid(row=0, column=0, sticky='w')
        ttk.Entry(self.anagram_frame, textvariable=self.chars_var, width=60).grid(row=0, column=1, sticky='ew')
        # Increase the width of the characters entry field

        ttk.Label(self.anagram_frame, text='Size of anagrams:').grid(row=1, column=0, sticky='w')
        ttk.Spinbox(self.anagram_frame, from_=1, to=10, textvariable=self.size_var).grid(row=1, column=1, sticky='ew')

        ttk.Label(self.anagram_frame, text='Number of anagrams:').grid(row=2, column=0, sticky='w')
        ttk.Spinbox(self.anagram_frame, from_=1, to=10, textvariable=self.num_var).grid(row=2, column=1, sticky='ew')

        # Create and place generate button and listbox for results
        ttk.Button(self.anagram_frame, text='Generate Anagrams', command=self.generate_anagrams).grid(row=3, column=0,
                                                                                                      columnspan=2)
        self.anagrams_listbox = tk.Listbox(self.anagram_frame, width=100, height=30)
        # Increase the size of the anagram result area
        self.anagrams_listbox.grid(row=4, column=0, columnspan=2, sticky='nsew')

        self.anagram_frame.grid_columnconfigure(1, weight=1)
        self.anagram_frame.grid_rowconfigure(4, weight=1)

    def generate_ascii(self):
        self.ascii_art_text.delete(1.0, tk.END)
        ascii_art = generate_ascii_art(self.text_var.get(), self.style_var.get())
        self.ascii_art_text.insert(tk.END, ascii_art)

    def generate_anagrams(self):
        self.anagrams_listbox.delete(0, tk.END)
        chars = self.chars_var.get()
        size = self.size_var.get()
        num = self.num_var.get()

        if len(chars) > 10:  # Choose a suitable maximum length
            messagebox.showwarning('Input too large', 'The input string is too large. Please enter a shorter string.')
        elif size > len(chars):
            messagebox.showwarning('Anagram size too large',
                                   'The chosen anagram size is greater than the length of the input string. Please '
                                   'choose a smaller size.')
        else:
            anagrams = generate_anagrams(chars, size, num)
            for anagram in anagrams:
                self.anagrams_listbox.insert(tk.END, anagram)

    # Add save ASCII art function
    def save_ascii_art(self):
        file = filedialog.asksaveasfile(initialdir=os.getcwd(), title="Save File",
                                        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file:
            file.write(self.ascii_art_text.get("1.0", "end-1c"))
            file.close()
        else:
            messagebox.showinfo("Information", "Cancelled")


def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()


if __name__ == "__main__":
    main()
