import random
import string


def random_string_generator(size=4, chars=string.ascii_uppercase + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def get_prescription_id():
    return "{rand_letters}{rand_digits}".format(rand_letters=random_string_generator(4, string.ascii_uppercase),
                                                rand_digits=random.randint(100, 999))


def unique_prescription_id(instance, prescription_id=None):

    if prescription_id is None:
        prescription_id = get_prescription_id()

    klass = instance.__class__

    qs_exists = klass.objects.filter(prescription_id=klass.prescription_id).exists()
    if qs_exists:
        new_prescription_id = get_prescription_id()
        return unique_prescription_id(instance, prescription_id=new_prescription_id)
    return prescription_id
