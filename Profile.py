from Annotations import XOnServer, XAll


@XAll
class Profile:

    secretId = 5

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @XOnServer
    def test(self):
        self.age = 5
