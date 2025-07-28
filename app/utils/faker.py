import random
from faker import Faker


def generate_unique_ukr_phone_number(number, faker) -> set[str]:
    generated_phone_numbers = set()
    codes = ['+38096', '+38098', '+38067', '+38095', '+38063', '+38073']
    i = 0
    while i < number:
        phone_number = faker.numerify(random.choice(codes) + '#########')

        if phone_number not in generated_phone_numbers:
            generated_phone_numbers.add(phone_number)
            i += 1
        else:
            i -= 1

    return generated_phone_numbers
