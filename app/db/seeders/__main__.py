import asyncio
from app.db.seeders.user_seeder import UserSeeder
from app.dependencies.faker import get_faker
from app.models import *
from app.db.seeders.applicant_seeder import ApplicantSeeder
from app.db.database import async_session_maker


async def main():
    faker = get_faker()
    session = async_session_maker()
    async with session as db:
        user_seeder = UserSeeder.create_seeder(db, faker)
        users = await user_seeder.run(number_of_applicants=10)
        users_for_applicants = [user for user in users if user.user_role_id == 2]
        applicant_seeder = ApplicantSeeder.create_seeder(db)
        await applicant_seeder.run(users_for_applicants)


if __name__ == "__main__":
    asyncio.run(main())
