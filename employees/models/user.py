from django.contrib.auth.models import AbstractUser, User
from .employee import Employee
from django.db import models


class EmployeeUser(models.Model):

    employee = models.OneToOneField(Employee, verbose_name="Employee", on_delete=models.CASCADE, related_name="profile", null=True,
                                    blank=True)
    user = models.OneToOneField(User, verbose_name="User", on_delete=models.CASCADE, related_name="profile", null=True)

    def __str__(self):
        emp_name = self.employee.first_name if self.employee else "No employee"
        dept_name = (
            self.employee.department.name
            if self.employee and self.employee.department
            else "No department"
        )
        return f"{emp_name} - {dept_name}"