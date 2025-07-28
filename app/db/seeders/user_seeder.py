from app.utils.faker import generate_unique_ukr_phone_number
from app.db.factories.user_factory import UserFactory
from app.dependencies.user import get_user_repository
from app.models.user import User
from app.repositories.user_repo import UserRepository



class UserSeeder:
    def __init__(
        self,
        user_factory: UserFactory,
        user_repo: UserRepository
    ):
        self.user_factory = user_factory
        self.user_repo = user_repo
        

    async def run(self, 
            number_of_applicants: int = 0, 
            number_of_employers: int = 0, 
            number_of_admins: int = 0
        ):
        number = number_of_applicants + number_of_employers + number_of_admins
        user_roles = [1 for i in range(number_of_admins)] +\
            [2 for i in range(number_of_applicants)] +\
            [3 for i in range(number_of_employers)]
        users = []

        phone_numbers = list(generate_unique_ukr_phone_number(number, self.user_factory.faker))

        for i in range(number):
            user = self.user_factory.create(
                user_role_id=user_roles[i], 
                phone_number=phone_numbers[i]
            )
            users.append(user)
        users = await self.user_repo.create_many(users)

        return users


    @staticmethod
    def create_seeder(session, faker):
        user_factory = UserFactory(faker)
        user_repo = get_user_repository(session)
        return UserSeeder(user_factory, user_repo)