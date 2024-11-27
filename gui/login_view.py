import tkinter as tk
from tkinter.messagebox import showinfo

from gui.gui_utils import LARGE_FONT
from exceptions import AuthenticationError
from library_client import LibraryClient


class LoginView(tk.Frame):
    """ Login view """

    def __init__(self, parent, controller, client: LibraryClient):
        super().__init__(parent)

        self.client = client
        self.controller = controller

        # configure rows and columns of grid layout
        self.columnconfigure(index="0 1", weight=1)
        self.rowconfigure(index="0 1 2 3", weight=1)

        self._init_ui()

    def _init_ui(self) -> None:
        self.controller.minsize(300, 200)

        """Create and position GUI components."""
        lbl_title = tk.Label(self, text="Please Log In", font=LARGE_FONT)
        lbl_username = tk.Label(self, text="Username: ")
        self.ent_username = tk.Entry(self)
        lbl_password = tk.Label(self, text="Password: ")
        self.ent_password = tk.Entry(self, show="*")
        btn_login = tk.Button(self, text="Log In", command=self._on_login_btn_click)

        # Position created components using grid layout
        lbl_title.grid(row=0, column=0, columnspan=2, pady=5)
        lbl_username.grid(row=1, column=0, padx=5, pady=10)
        self.ent_username.grid(row=1, column=1, padx=5, pady=10)
        lbl_password.grid(row=2, column=0, padx=5, pady=10)
        self.ent_password.grid(row=2, column=1, padx=5, pady=10)
        btn_login.grid(row=3, column=0, columnspan=2, pady=10)

        # Set focus to username entry field
        self.ent_username.focus_set()

    def _on_login_btn_click(self) -> None:
        """Handle login button click"""

        username = self.ent_username.get()
        password = self.ent_password.get()
        try:
            self.client.login(username, password)

            # Check if the user is admin or regular user
            if self.client.is_admin:
                show_message("Login success", f"Welcome admin {username}")
                self.controller.show_frame("AdminView")
            else:
                show_message("Login success", f"Welcome user {username}")
                self.controller.show_frame("UserView")

        except AuthenticationError:
            show_message("Login Error", "Incorrect username or password! Please retry", True)
        except Exception:
            show_message("Login Error", "Error while login", True)


def show_message(title: str, message: str, is_error: bool = False):
    if is_error:
        tk.messagebox.showerror(title, message)
    else:
        tk.messagebox.showinfo(title, message)
