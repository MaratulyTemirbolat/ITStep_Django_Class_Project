class Person:  # noqa
    first_name: str = None
    last_name: str = None
    email: str = None

    def __init__(self, first_name: str, last_name: str) -> None:  # noqa
        self.first_name = first_name
        self.last_name = last_name

    @property
    def email(self):  # noqa
        print("Getting email.")
        return self.first_name + "_" + self.last_name + "@gmail.com"

    @email.setter
    def set_email(self, email: str):  # noqa
        print("Setting email")
        self.email = email

    def full_name(self):
        """For getting full name."""
        return self.first_name + " " + self.last_name


p1: Person = Person("Temirbolat", "Maratuly")
print(p1.email)
