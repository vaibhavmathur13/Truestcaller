from truestcaller import models as truestcaller_models

from random import randint as rn


def generate_name_phone_number_pair():
    """
    Mapping of random names with random phone numbers.
    :return:
    """
    test_numbers_file = open("truestcaller/numbers.txt", "r")
    test_names_file = open("truestcaller/names.txt", "r")
    numbers = []
    names = []
    for i in range(500):
        numbers.append(test_numbers_file.readline().strip())
        names.append(test_names_file.readline().strip())
    test_names_file.close()
    test_numbers_file.close()
    contact_count = rn(0, 150)
    number_indexes = set()
    name_indexes = set()
    while len(number_indexes) < contact_count:
        number_indexes.add(rn(0, 499))
    while len(name_indexes) < contact_count:
        name_indexes.add(rn(0, 499))
    contacts = []
    for nameIndexesIterator in name_indexes:
        contacts.append([names[nameIndexesIterator]])
    i = 0
    for numberIndexesIterator in number_indexes:
        contacts[i].append(numbers[numberIndexesIterator])
        i += 1
    return contacts


def add_user_contact_book(user_obj):
    """
    Creating instances of random phonebook contacts of a registered
    user.
    :param user_obj:
    :return:
    """
    contacts = generate_name_phone_number_pair()
    for contact in contacts:
        if contact[1] != user_obj.phone_number:
            truestcaller_models.Directory.objects.create(
                added_by=user_obj, name=contact[0], phone_number=contact[1]
            )


def get_people_for_email(phone_number):
    """
    returns the list of phone numbers of registered users whose contact book
    contains the mentioned parameter.
    :param phone_number:
    :return:
    """
    return truestcaller_models.Directory.objects.filter(
        phone_number=phone_number, added_by__isnull=False
    ).values_list('added_by__phone_number', flat=True)
