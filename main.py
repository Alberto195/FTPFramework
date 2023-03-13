from PyTealCodeGenerator import parse_and_generate_code


if __name__ == '__main__':
    print(parse_and_generate_code("""from Annotations import XOnServer, XAll
from Wrappers import XWrapper


@XAll
class Profile:

    secretId = 5

    def __init__(self, name, age):
        self.name = name
        self.age = age

    @XOnServer
    def test(self):
        self.age = 5
    """))
