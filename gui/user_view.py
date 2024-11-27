import tkinter as tk
from exceptions import *

from tkinter.messagebox import showinfo

from library_client import LibraryClient

GRID_PADDING = {"padx": 5, "pady": 5}


class UserView(tk.Frame):
    """ Non-admin user view """

    def __init__(self, parent, controller, client: LibraryClient):
        super().__init__(parent)

        self.controller = controller
        self.client = client

        self._init_ui()
        self._fill_books_list()

    def _fill_books_list(self) -> None:
        books = None
        try:
            books = self.client.get_books()
        except AuthenticationError as error:
            show_message("Error", str(error), True)

        for book in books["books"]:
            book_view = self.SingleBookView(self.books_list, book, self)
            book_view.pack(**GRID_PADDING)

    def _init_ui(self) -> None:
        """ Initialize UI """
        self.controller.minsize(300, 200)

        button_home = tk.Button(self, text='Back to Login page',
                                command=lambda: self.controller.show_frame("LoginView"))
        button_home.pack(pady=5)

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

        canvas.create_window((0, 0), window=self.books_list, anchor="nw")

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Enable mousewheel scrolling
        self._bind_scroll(canvas)

    def _bind_scroll(self, canvas) -> None:
        """ Configure mousewheel scrolling """

        def _on_mousewheel(event) -> None:
            canvas.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    class SingleBookView(tk.Frame):
        """ Contains book's info """

        def __init__(self, book_list, book_data: dict, parent):
            super().__init__(book_list, highlightbackground="black", highlightthickness=1)
            self.parent = parent
            self.book_id = book_data["id"]

            self._display_book_info(book_data)

        def _display_book_info(self, book_data: dict) -> None:
            """ Create single book UI """
            lbl_title = tk.Label(self, text=f"title: {book_data['title']}")
            lbl_author = tk.Label(self, text=f"author: {book_data['author']}")
            self.lbl_is_borrowed = tk.Label(self,
                                            text=f"borrowed: {'yes' if book_data['is_borrowed'] else 'no'}")

            self.btn_borrow = tk.Button(self, text="Borrow", command=self._on_btn_borrow_click)
            self.btn_borrow.config(state=tk.DISABLED if book_data['is_borrowed'] else tk.NORMAL)
            self.btn_return = tk.Button(self, text="Return", command=self._on_btn_return_click)
            self.btn_return.config(state=tk.NORMAL if book_data['is_borrowed'] else tk.DISABLED)

            # Position created components using grid layout
            lbl_title.grid(row=0, column=0, **GRID_PADDING)
            lbl_author.grid(row=1, column=0, **GRID_PADDING)
            self.lbl_is_borrowed.grid(row=2, column=0, **GRID_PADDING)
            self.btn_borrow.grid(row=0, column=1, rowspan=3, **GRID_PADDING)
            self.btn_return.grid(row=0, column=2, rowspan=3, **GRID_PADDING)

        def _on_btn_borrow_click(self) -> None:
            """ borrow btn handler """
            try:
                # Call server
                self.parent.client.borrow_book(self.book_id)

                # Update local info
                self.btn_borrow.config(state=tk.DISABLED)
                self.btn_return.config(state=tk.NORMAL)
                self.lbl_is_borrowed.config(text="borrowed: yes")

                show_message("Book borrowed", "Book successfully borrowed")

            except LibraryError as error:
                show_message("Error", str(error), True)

        def _on_btn_return_click(self) -> None:
            """ return btn handler """
            try:
                # Call server
                self.parent.client.return_book(self.book_id)

                # Update local info
                self.btn_borrow.config(state=tk.NORMAL)
                self.btn_return.config(state=tk.DISABLED)
                self.lbl_is_borrowed.config(text="borrowed: no")

                show_message("Book returned", "Book successfully returned")

            except LibraryError as error:
                show_message("Error", str(error), True)


def show_message(title: str, message: str, is_error: bool = False):
    if is_error:
        tk.messagebox.showerror(title, message)
    else:
        tk.messagebox.showinfo(title, message)
