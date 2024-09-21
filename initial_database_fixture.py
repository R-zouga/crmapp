import os
import traceback
import django
from django.db import transaction

from faker import Faker
from datetime import date, datetime, timedelta
from django.utils.timezone import make_aware

# Set the environment variable for Django settings module.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CRMProject.settings")

# Initialize Django setup BEFORE importing the models!
# Otherwise, an Exception will be thrown.
django.setup()

from User import models as UserModel
from Client import models as ClientModel
from Salesman import models as SalesmanModel
from Supervisor import models as SupervisorModel
from Manager import models as ManagerModel
from Service.models import Service

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


def create_deal(**kwargs):
    SalesmanModel.Deal.objects.create(**kwargs)


# Using transaction will make sure either ALL database operations are made
# or revert changes if Exception occurred in the middle of the transaction.
try:
    with transaction.atomic():
        for _ in range(2):
            group = UserModel.Group.objects.create(name=fake.unique.street_name())
            SalesmanModel.BranchGroup.objects.create(
                group=group, max_members=fake.random_int(min=6, max=10)
            )

        group = UserModel.Group.objects.create(name=fake.unique.street_name())
        department = SupervisorModel.DepartmentBoard.objects.create(group=group)

        admin = UserModel.User.objects.create_superuser(**return_user_dictionary())

        group = UserModel.Group.objects.create(name=fake.unique.street_name())
        manager_group = ManagerModel.ManagerGroup.objects.create(
            group=group, admin=admin
        )

        for _ in range(10):
            user = UserModel.User.objects.create_user(
                **return_user_dictionary("Salesman")
            )
            SalesmanModel.Salesman.objects.create(
                user=user, max_enrolled_branches=fake.random_int(1, 4)
            )

        branches = SalesmanModel.BranchGroup.objects.all()
        for i in range(2):
            user = UserModel.User.objects.create_user(
                **return_user_dictionary("Supervisor")
            )
            SupervisorModel.Supervisor.objects.create(
                user=user, branch_group=branches[i]
            )

        user = UserModel.User.objects.create_user(**return_user_dictionary("Manager"))
        manager = ManagerModel.Manager.objects.create(user=user, department=department)

        salesmen = SalesmanModel.Salesman.objects.all()
        branches[0].salesmen_set.add(*salesmen[:6])
        branches[1].salesmen_set.add(*salesmen[6:])

        department.supervisor_set.add(*SupervisorModel.Supervisor.objects.all())
        manager_group.manager_set.add(manager)

        for _ in range(5):
            user = UserModel.User.objects.create_user(
                **return_user_dictionary("Client")
            )
            ClientModel.Client.objects.create(user=user)

        for salesman in salesmen:
            UserModel.UserHistory.objects.create(
                join_date=date(2023, 1, 1),
                status="Salesman",
                belonging_to=salesman.branches.first().group,
                user=salesman.user,
            )

        for supervisor in SupervisorModel.Supervisor.objects.all():
            UserModel.UserHistory.objects.create(
                join_date=date(2023, 1, 1),
                status="Supervisor",
                belonging_to=department.group,
                responsible_for=supervisor.branch_group.group,
                user=supervisor.user,
            )

        UserModel.UserHistory.objects.create(
            join_date=date(2023, 1, 1),
            status="Manager",
            belonging_to=manager_group.group,
            responsible_for=manager.department.group,
            user=manager.user,
        )

        for client in ClientModel.Client.objects.all():
            UserModel.UserHistory.objects.create(
                join_date=date(2023, 1, 1),
                status="Client",
                user=client.user,
            )

        clients = ClientModel.Client.objects.all()

        for salesman in salesmen:
            attributed_to = salesman.branches.first()
            for _ in range(200):
                service_seeker = fake.random_element(clients).user
                service = Service.objects.create(
                    name=fake.unique.sentence(nb_words=5),
                    description=fake.paragraph(),
                    price=fake.random_int(min=50, max=150),
                )
                status_time = fake.date_time_between(
                    datetime(2024, 1, 1), datetime(2024, 8, 1)
                )
                create_deal(
                    service=service,
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    time_of_state=make_aware(status_time),
                )

                status_time += timedelta(fake.random_int(min=2, max=20))
                create_deal(
                    service=service,
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    time_of_state=make_aware(status_time),
                    status=1,
                )
                status_time += timedelta(fake.random_int(min=2, max=20))
                create_deal(
                    service=service,
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    time_of_state=make_aware(status_time),
                    status=100,
                )

        for salesman in salesmen:
            attributed_to = salesman.branches.first()
            for _ in range(5):
                service_seeker = fake.random_element(clients).user
                service = Service.objects.create(
                    name=fake.unique.sentence(nb_words=5),
                    description=fake.paragraph(),
                    price=fake.random_int(min=20, max=45),
                )
                status_time = fake.date_time_between(
                    datetime(2024, 4, 1), datetime(2024, 8, 1)
                )
                create_deal(
                    service=service,
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    time_of_state=make_aware(status_time),
                    status=0,
                )
                status_time += timedelta(fake.random_int(min=2, max=20))
                create_deal(
                    service=service,
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    time_of_state=make_aware(status_time),
                    status=1,
                )
                status_time += timedelta(fake.random_int(min=2, max=20))
                create_deal(
                    service=service,
                    salesman=salesman,
                    attributed_to=attributed_to,
                    service_seeker=service_seeker,
                    time_of_state=make_aware(status_time),
                    status=-1,
                )
except:
    # If ANY Exception is thrown then transaction is canceled and the traceback is printed
    # to locate the error
    traceback.print_exc()
else:
    print("Prepopulating database done successfully with no errors :)")
