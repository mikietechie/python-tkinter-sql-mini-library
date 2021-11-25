'''
By Mike Zinyoni

25 November 2021

+263713122648
mzinyoni7@outlook.com
looking for a job ASAP
'''
import tkinter as tk
import tksheet
from db import Book
from tkinter import messagebox


class Application(object):
    def __init__(self):
        self.root = root = tk.Tk()
        root.title("Mini Library")
        root.minsize(720, 600)
        root.maxsize(720, 600)
        
        self.filter_val = tk.StringVar()
        self.filter_column  = tk.StringVar(value="id")
        
        self.book_id = tk.IntVar()
        self.book_title = tk.StringVar()
        self.book_author = tk.StringVar()
        self.book_year = tk.IntVar()
        self.book_publisher = tk.StringVar()
        
        # menu
        toolbar = tk.Frame(root, cnf={"bg": "#cccccc"})
        toolbar.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        tk.Button(toolbar, text="Create", command=self.add_book).place(relx=0.6, rely=0.1, relwidth=0.08,relheight=0.8)
        tk.Button(toolbar, text="Edit", command=self.edit_book).place(relx=0.7, rely=0.1, relwidth=0.08,relheight=0.8)
        tk.Button(toolbar, text="Delete", command=self.delete_book).place(relx=0.8, rely=0.1, relwidth=0.08,relheight=0.8)
        filters_frame = tk.Frame(toolbar)
        filters_frame.place(relx=0.05, rely=0.1, relwidth=0.5, relheight=0.8)
        
        column_options = tk.OptionMenu(filters_frame, self.filter_column, *["id", "title", "author", "year", "publisher"])
        column_options.configure({"relief": "flat"})
        column_options.place(relx=0, rely=0, relwidth=0.35, relheight=1)
        tk.Entry(filters_frame, textvariable=self.filter_val).place(relx=0.35, rely=0, relwidth=0.35, relheight=1)
        tk.Button(filters_frame, text="Filter", command=self.apply_filter).place(relx=0.73, rely=0.1, relwidth=0.14, relheight=0.8)
        tk.Button(filters_frame, text="All", command=self.clear_filter).place(relx=0.85, rely=0.1, relwidth=0.14, relheight=0.8)
        
        main = tk.Frame(root)
        main.place(relx=0,rely=0.1, relwidth=1,relheight=0.9)
        
        self.form_frame = tk.Frame(main)
        self.form_frame.place(relx=0,rely=0, relwidth=1,relheight=1)
        
        self.table_frame = tk.Frame(main)
        self.table_frame.place(relx=0,rely=0, relwidth=1,relheight=1)
        self.show_table_frame(books=Book.all())
    
    def clear_filter(self, event=None):
        self.show_table_frame(books=Book.all())
    
    def apply_filter(self, event=None):
        self.show_table_frame(books=Book.filter(self.filter_column.get().strip(), self.filter_val.get().strip()))
    
    def show_form_frame(self, book: Book=None):
        if book:
            self.book_id.set(book.id)
            self.book_title.set(book.title)
            self.book_author.set(book.author)
            self.book_year.set(book.year)
            self.book_publisher.set(book.publisher)
        else:
            pass
        tk.Label(self.form_frame, text=(f"Edit book {book.id}" if book.title else "Create Book")).place(relx=0.05, rely=0.1, relwidth=0.9, relheight=0.1)
        tk.Label(self.form_frame, text="Title").place(relx=0.05, rely=0.25, relwidth=0.3, relheight=0.1)
        tk.Entry(self.form_frame, textvariable=self.book_title).place(relx=0.45, rely=0.25, relwidth=0.5, relheight=0.1)
        tk.Label(self.form_frame, text="Author").place(relx=0.05, rely=0.4, relwidth=0.3, relheight=0.1)
        tk.Entry(self.form_frame, textvariable=self.book_author).place(relx=0.45, rely=0.4, relwidth=0.5, relheight=0.1)
        tk.Label(self.form_frame, text="Year").place(relx=0.05, rely=0.55, relwidth=0.3, relheight=0.1)
        tk.Entry(self.form_frame, textvariable=self.book_year).place(relx=0.45, rely=0.55, relwidth=0.5, relheight=0.1)
        tk.Label(self.form_frame, text="Publisher").place(relx=0.05, rely=0.7, relwidth=0.3, relheight=0.1)
        tk.Entry(self.form_frame, textvariable=self.book_publisher).place(relx=0.45, rely=0.7, relwidth=0.5, relheight=0.1)
        tk.Button(self.form_frame, text=("Update Book" if book.title else "Add Book"), command=self.save_form).place(relx=0.2, rely=0.85, relwidth=0.6, relheight=0.1)
        self.form_frame.tkraise()
    
    def save_form(self, event=None):
        book = Book(self.book_title.get(), self.book_author.get(), self.book_year.get(), self.book_publisher.get(), id=self.book_id.get())
        msg = f"Updated book {book}" if book.id else f"Success full added {book}"
        if book.save():
            messagebox.showinfo("Successful", msg)
            self.show_table_frame(Book.all())
        else:
            messagebox.showerror("Error", "An errror occured.")
    
    def delete_book(self, event=None):
        book = self.get_selected_book()
        if book:
            confirm = messagebox.askyesno("Confirm delete", f"Are you sure you want to delelte {book}?")
            if confirm:
                book.delete()
                messagebox.showinfo("Successful", f"The book {book} was deleted successfully.")
                self.show_table_frame(Book.all())
        else:
            messagebox.showwarning("Warning", "Please select book.")
    
    def edit_book(self, event=None):
        book = self.get_selected_book()
        if book:
            self.show_form_frame(book=book)
        else:
            messagebox.showwarning("Warning", "Please select book.")
            
    def add_book(self, event=None):
        self.show_form_frame(book=Book("", "", 0, "", 0))
    
    def show_table_frame(self, books=[]):
        self.books_sheet = tksheet.Sheet(self.table_frame, headers=["id", "title", "author", "year", "publisher"])
        self.books_sheet.place(relx=0,rely=0, relwidth=1,relheight=1)
        self.books_sheet.set_sheet_data([list(book) for book in books])
        self.books_sheet.enable_bindings(("single_select", "row_select", "column_width_resize", "arrowkeys", "right_click_popup_menu", "rc_select", "rc_insert_row", "rc_delete_row", "copy", "cut", "paste", "delete", "undo"))
        self.books_sheet.change_theme(theme="light blue")
        self.table_frame.tkraise()
    
    def get_selected_book(self, event=None):
        try:
            book = Book.get(int(self.books_sheet.get_row_data(self.books_sheet.get_selected_rows().pop())[0]))
            return book
        except:
            return None
    
    def run(self):
        self.root.mainloop()


def main():
    Application().run()

if __name__ == '__main__':
    main()
    

