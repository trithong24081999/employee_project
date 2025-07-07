from django.contrib.auth.models import AbstractUser, User
from .employee import Employee
from django.db import models


class EmployeeUser(models.Model):

    employee = models.OneToOneField(Employee, verbose_name="Employee", on_delete=models.CASCADE, related_name="profile", null=True,
                                    blank=True)
    user = models.OneToOneField(User, verbose_name="User", on_delete=models.CASCADE, related_name="profile", null=True)
