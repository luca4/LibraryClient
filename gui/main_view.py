import tkinter as tk
from gui.login_view import LoginView
from gui.user_view import UserView
from gui.admin_view import AdminView

from library_client import LibraryClient


class MainView(tk.Tk):
    """ Startup window """

    def __init__(self, client: LibraryClient, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = client

        self._setup_window()

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_frame("LoginView")

    def show_frame(self, frame_name: str) -> None:
        """ Change top frame the user is viewing """
        if frame_name == "LoginView":
            frame = LoginView(self.container, self, self.client)
        elif frame_name == "AdminView":
            frame = AdminView(self.container, self, self.client)
        elif frame_name == "UserView":
            frame = UserView(self.container, self, self.client)
        else:
            raise ValueError(f"Invalid frame name {frame_name}")

        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def _setup_window(self) -> None:
        """Configure window properties and position."""
        self.title("Library Client")
        self.minsize(300, 200)
        self._center_window()

    def _center_window(self) -> None:
        """ Make sure the windows is positioned centered to the screen """
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")
