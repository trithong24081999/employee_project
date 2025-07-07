from django.db import models
from datetime import datetime, date, timedelta
class Employee(models.Model):
    first_name = models.CharField(max_length=30, verbose_name='First Name')
    last_name = models.CharField(max_length=30, verbose_name='Last Name')
    email = models.EmailField(unique=True, verbose_name='Email Address')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name='Phone Number')
    birthday = models.DateField(blank=True, null=True, verbose_name='Date of Birth')
    joining_date = models.DateField( verbose_name='Date Joined')
    active = models.BooleanField(default=True, verbose_name='Active Status')
    department = models.ForeignKey("employees.Department", on_delete=models.CASCADE, related_name="employees")

    class Meta:
        db_table = "hr_employee"
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        ordering = ['joining_date', 'active']
        managed = False

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        if self.birthday:
            today = date.today()
            age = today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
            return age

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    