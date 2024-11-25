class LibraryError(Exception):
    pass


class AuthenticationError(LibraryError):
    pass


class ResourceNotFoundError(LibraryError):
    pass


class ValidationError(LibraryError):
    pass
