import random
from string import ascii_letters
from string import punctuation


def __generate_random_secret(k: int = 10):
    """

    :param k: integer depicting number of character in string
    :return: string of length k with ascii letters, punctuation and numbers
    """
    return "".join(random.choices(ascii_letters
                                  + punctuation
                                  + "".join(map(str, range(10))),
                                  k=k)
                   )


SECRET = __generate_random_secret()

AUTH_KEY = "auth-key"
AUTH_KEY_VALUE = __generate_random_secret(30)
