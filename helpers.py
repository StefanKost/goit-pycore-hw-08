from exceptions import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NotFoundError as e:
            return e.message
        except ConflictError as e:
            return e.message
        except InvalidPhone as e:
            return e.message
        except InvalidBirthday as e:
            return e.message
        except KeyError as e:
            return f"Error: {e}"
        except ValueError as e:
            return f"Error: {e}"
        except IndexError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"An error occurred: {type(e).__name__}: {e}"

    return inner
