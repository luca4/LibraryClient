import tkinter as tk
from tkinter.messagebox import showinfo

from library_client import LibraryClient
from gui.gui_utils import LARGE_FONT
from exceptions import *

GRID_PADDING = {"padx": 5, "pady": 5}


class AdminView(tk.Frame):
    """Admin user view """

    def __init__(self, parent, controller, client: LibraryClient):
        super().__init__(parent)

        self.controller = controller
        self.client = client

        self.columnconfigure(index="0 1", weight=1)
        self.rowconfigure(index="0 1 2 3", weight=1)

        self._init_ui()

    def _init_ui(self) -> None:
        """ create frame UI """
        self.controller.minsize(300, 500)
        button_home = tk.Button(self, text='Back to Login page',
                                command=lambda: self.controller.show_frame("LoginView"))
        button_home.grid(row=0, column=0, pady=5)

        self._create_add_book_ui()
        self._create_books_list_ui()
        self._fill_books_list()

    def _bind_scroll(self, canvas) -> None:
        """ Configure mousewheel scrolling """

        def _on_mousewheel(event) -> None:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _fill_books_list(self) -> None:
        """ Gather data from server and fill list of books """
        books = None
        try:
            books = self.client.get_books()
        except AuthenticationError as error:
            show_message("Error", str(error), True)

        for book in books["books"]:
            book_view = self.SingleBookView(self.books_list, book, self)
            book_view.pack()

    def _create_books_list_ui(self) -> None:
        """ Create UI that contains books listing """
        tk.Label(self, text="List of books:", font=LARGE_FONT).grid(row=2, column=0, pady=5)

        # Create canvas and scrollbar
        canvas = tk.Canvas(self)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create frame to hold books
        self.books_list = tk.Frame(canvas)
        self.books_list.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.books_list)

        canvas.grid(row=3, column=0, columnspan=2)
        scrollbar.grid(row=3, column=1)

        # Enable mousewheel scrolling
        self._bind_scroll(canvas)

    def _create_add_book_ui(self) -> None:
        """ Create frame used for book adding """
        add_book_frame = tk.Frame(self, highlightbackground="black", highlightthickness=1)
        add_book_frame.columnconfigure(index="0 1", weight=1)
        add_book_frame.rowconfigure(index="0 1 2 3", weight=1)
        tk.Label(add_book_frame, text="Add a book here:", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady=5)
        tk.Label(add_book_frame, text="Title: ").grid(row=1, column=0, padx=5)
        self.ent_title = tk.Entry(add_book_frame)
        self.ent_title.grid(row=1, column=1, padx=5)
        tk.Label(add_book_frame, text="Author: ").grid(row=2, column=0, padx=5)
        self.ent_author = tk.Entry(add_book_frame)
        self.ent_author.grid(row=2, column=1, padx=5)
        self.check_is_borrowed = tk.BooleanVar()
        self.c1_is_borrowed = tk.Checkbutton(add_book_frame, text='Is already booked', variable=self.check_is_borrowed)
        self.c1_is_borrowed.grid(row=3, column=0, columnspan=2)
        btn_add = tk.Button(add_book_frame, text="Add", command=self._on_click_add_btn)
        btn_add.grid(row=4, column=0, columnspan=2, pady=5)

        add_book_frame.grid(row=1, column=0, pady=5)

    def _validate_book_data(self, title: str, author: str) -> bool:
        if not title.strip() or not author.strip():
            show_message("Validation Error", "Title and Author cannot be empty.", is_error=True)
            return False
        return True

    def _on_click_add_btn(self) -> None:
        """ add book btn handler """
        title, author = self.ent_title.get(), self.ent_author.get()
        if not self._validate_book_data(title, author):
            return
        book_data = {"title": title, "author": author, "is_borrowed": self.check_is_borrowed.get()}

        try:
            book_id = self.client.add_book(book_data)
            book_data["id"] = book_id
            self.SingleBookView(self.books_list, book_data, self).pack()
            show_message("Book added", "Book successfully added")
        except LibraryError as error:
            show_message("Error", str(error), True)

    class SingleBookView(tk.Frame):
        """ Contains book's info """

        def __init__(self, book_list, book_data: dict, parent):
            super().__init__(book_list, highlightbackground="black", highlightthickness=1)
            self.parent = parent
            self.book_id = book_data["id"]

            self._display_book_info(book_data)

        def _display_book_info(self, book_data: dict) -> None:
            """ Create single book UI """
            lbl_title = tk.Label(self, text="title:")
            self.ent_title = tk.Entry(self)
            self.ent_title.insert(0, book_data['title'])
            lbl_author = tk.Label(self, text="author:")
            self.ent_author = tk.Entry(self)
            self.ent_author.insert(0, book_data['author'])
            self.check_is_borrowed = tk.BooleanVar()
            self.c1_is_borrowed = tk.Checkbutton(self, text='Is borrowed', variable=self.check_is_borrowed)
            self.check_is_borrowed.set(book_data['is_borrowed'])
            self.c1_is_borrowed.grid(row=3, column=0, columnspan=2)

            self.btn_save = tk.Button(self, text="Save", command=self._on_btn_save_click)
            self.btn_delete = tk.Button(self, text="Delete", command=self._on_btn_delete_click)

            # Position created components using grid layout
            lbl_title.grid(row=0, column=0, **GRID_PADDING)
            self.ent_title.grid(row=0, column=1, **GRID_PADDING)
            lbl_author.grid(row=1, column=0, **GRID_PADDING)
            self.ent_author.grid(row=1, column=1, **GRID_PADDING)
            self.c1_is_borrowed.grid(row=2, column=0, columnspan=2, **GRID_PADDING)
            self.btn_save.grid(row=3, column=0, **GRID_PADDING)
            self.btn_delete.grid(row=3, column=1, **GRID_PADDING)

        def _on_btn_save_click(self) -> None:
            """ save btn handler """
            try:
                # Call server
                book_data = {"title": self.ent_title.get(),
                             "author": self.ent_author.get(),
                             "is_borrowed": self.check_is_borrowed.get()}
                self.parent.client.update_book(self.book_id, book_data)

                show_message("Book saved", "Book data successfully saved")

            except LibraryError as error:
                show_message("Error", str(error), True)

        def _on_btn_delete_click(self) -> None:
            """ delete btn handler """
            if tk.messagebox.askyesno("Confirm", "Are you sure you want to delete this book?"):
                try:
                    # Call server
                    self.parent.client.delete_book(self.book_id)

                    # Update local info
                    self.destroy()

                    show_message("Book deleted", "Book successfully deleted")

                except LibraryError as error:
                    show_message("Error", str(error), True)


def show_message(title: str, message: str, is_error: bool = False):
    if is_error:
        tk.messagebox.showerror(title, message)
    else:
        tk.messagebox.showinfo(title, message)
