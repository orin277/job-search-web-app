from faker import Faker
from app.models.user import User


from app.utils.auth import get_password_hash


class UserFactory:
    def __init__(self, faker: Faker):
        self.faker = faker

    def create(
        self,
        user_role_id: int = None,
        city_id: int = None,
        phone_number: str = None,
    ) -> User:
        if phone_number is None:
            phone_number = self.faker.numerify('+38096#######')
        return User(
            name=self.faker.first_name(),
            surname=self.faker.last_name(),
            email=self.faker.unique.email(),
            phone=phone_number,
            hashed_password=get_password_hash("password123"),
            city_id=city_id,
            user_role_id=user_role_id,
        )