from gui.main_view import MainView
from library_client import LibraryClient

client = LibraryClient()
app = MainView(client)
app.mainloop()


