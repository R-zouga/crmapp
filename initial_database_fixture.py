import os
import traceback
import django
from django.db import transaction

from faker import Faker
from datetime import date, timedelta

# Set the environment variable for Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRMProject.settings")

# Initialize Django setup BEFORE importing the models!
# Otherwise, an Exception will be thrown.
django.setup()

from user import models
from service.models import Service

fake = Faker()


def return_user_dictionary(status=""):
    """
    A helper function that returns a user dictionary.
    :param string status: the status of the user. See UserHistory for further explanation
    :return: user dictionary.
    :rtype: User instance

    """

    # The reason for this is fake.name could return more than 2 strings after splitting
    # like ["Adam", "Beau", "Spencer"].
    # By the way, the "unique" before the name makes sure that the instances are unique in each generation.
    first_name, last_name = fake.unique.name().split(" ")[:2]

    user = {
        "email": f"{first_name.lower()}{last_name.lower()}@gmail.com",
        "first_name": first_name,
        "last_name": last_name,
        "password": "SamePassword123",
        "phone_number": fake.unique.numerify("############"),
        "current_status": status,
    }

    return user


# Using transaction will make sure either ALL database operations are made
# or revert changes if Exception occurred in the middle of the transaction.
try:
    with transaction.atomic():
        for _ in range(2):
            group = models.Group.objects.create(name=fake.unique.street_name())
            models.BranchGroup.objects.create(
                group=group, max_members=fake.random_int(min=20, max=50)
            )

        group = models.Group.objects.create(name=fake.unique.street_name())
        department = models.DepartmentBoard.objects.create(group=group)

        admin1 = models.User.objects.create_superuser(**return_user_dictionary())

        group = models.Group.objects.create(name=fake.unique.street_name())
        manager_group = models.ManagerGroup.objects.create(group=group, admin=admin1)

        for _ in range(4):
            user = models.User.objects.create_user(**return_user_dictionary("Salesman"))
            models.Salesman.objects.create(
                user=user, max_enrolled_branches=fake.random_int(1, 4)
            )

        branches = models.BranchGroup.objects.all()
        for i in range(2):
            user = models.User.objects.create_user(
                **return_user_dictionary("Supervisor")
            )
            models.Supervisor.objects.create(user=user, branch_group=branches[i])

        user = models.User.objects.create_user(**return_user_dictionary("Manager"))
        manager = models.Manager.objects.create(user=user, department=department)

        salesmen = models.Salesman.objects.all()
        for i in range(2):
            branches[i].salesmen_set.add(*salesmen[2 * i : 2 * i + 2])

        department.supervisor_set.add(*models.Supervisor.objects.all())
        manager_group.manager_set.add(manager)

        for _ in range(5):
            user = models.User.objects.create_user(**return_user_dictionary("Client"))
            models.Client.objects.create(user=user)

        for _ in range(3):
            user = models.User.objects.create_user(
                **return_user_dictionary("Representative")
            )
            models.Representative.objects.create(user=user)

        for _ in range(5):
            models.Company.objects.create(
                email=fake.unique.company_email(),
                name=fake.unique.company(),
                location=fake.address(),
                phone_number=fake.unique.numerify("############"),
            )

        for salesman in salesmen:
            models.UserHistory.objects.create(
                join_date=date(2023, 1, 1),
                status="Salesman",
                belonging_to=salesman.branches.first().group,
                user=salesman.user,
            )

        for supervisor in models.Supervisor.objects.all():
            models.UserHistory.objects.create(
                join_date=date(2023, 1, 1),
                status="Supervisor",
                belonging_to=department.group,
                responsible_for=supervisor.branch_group.group,
                user=supervisor.user,
            )

        models.UserHistory.objects.create(
            join_date=date(2023, 1, 1),
            status="Manager",
            belonging_to=manager_group.group,
            responsible_for=manager.department.group,
            user=manager.user,
        )

        clients = models.Client.objects.all()

        for salesman in salesmen:
            attributed_to = salesman.branches.first()
            for _ in range(1_000):
                service_seeker = fake.random_element(clients).user
                service = Service.objects.create(
                    name=fake.unique.sentence(nb_words=5),
                    description=fake.paragraph(),
                    price=fake.random_int(min=500, max=32_000),
                )
                status_date = fake.date_between(date(2024, 1, 1), date(2024, 5, 1))
                models.Deal.objects.create(
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    service=service,
                    date_of_state=status_date,
                )
                status_date += timedelta(fake.random_int(min=2, max=20))
                models.Deal.objects.create(
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    service=service,
                    date_of_state=status_date,
                    status=1,
                )
                status_date += timedelta(fake.random_int(min=2, max=20))
                models.Deal.objects.create(
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    service=service,
                    date_of_state=status_date,
                    status=100,
                )

        for salesman in salesmen:
            attributed_to = salesman.branches.first()
            for _ in range(3):
                service_seeker = fake.random_element(clients).user
                service = Service.objects.create(
                    name=fake.unique.sentence(nb_words=5),
                    description=fake.paragraph(),
                    price=fake.random_int(min=500, max=32_000),
                )
                status_date = fake.date_between(date(2024, 1, 1), date(2024, 5, 1))
                models.Deal.objects.create(
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    service=service,
                    date_of_state=status_date,
                )
                status_date += timedelta(fake.random_int(min=2, max=20))
                models.Deal.objects.create(
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    service=service,
                    date_of_state=status_date,
                    status=1,
                )
                status_date += timedelta(fake.random_int(min=2, max=20))
                models.Deal.objects.create(
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    service=service,
                    date_of_state=status_date,
                    status=-1,
                )
except:
    # If ANY Exception is thrown then transaction is canceled and the traceback is printed
    # to locate the error
    traceback.print_exc()
else:
    print("Prepopulating database done successfully with no errors :)")
