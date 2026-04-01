class User:
    ##simple user class to hold email and interests
    ##this is easy to update by adding any needed elements or fields to init and the class itself
    def __init__(self, email: str, interests: list[str]):
        self.email = email
        self.interests = interests
