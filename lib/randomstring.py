import random, string

def random_string(length):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for i in range(length))


if __name__ == '__main__':
    pass
