import random
import string


def random_string_generator(size=4, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def get_random_code():
    return "{rand_letters}{rand_digits}".format(rand_letters=random_string_generator(4, string.ascii_uppercase),
                                                rand_digits=random.randint(100, 999))


def unique_random_code(instance, random_code=None):

    if random_code is None:
        random_code = get_random_code()

    klass = instance.__class__

    qs_exists = klass.objects.filter(prescription_id=klass.random_code).exists()
    if qs_exists:
        new_random_code = get_random_code()
        return unique_random_code(instance, random_code=new_random_code)
    return random_code
