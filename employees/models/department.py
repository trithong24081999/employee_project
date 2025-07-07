from django.db import models
from .employee import Employee

class Department(models.Model):

    class Meta:
        db_table = "hr_department"
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        managed = False


    name = models.CharField(verbose_name="Name", blank=True, null=True)
    manager = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='manager_id',  verbose_name="Manager")
    parent = models.ForeignKey('self', on_delete=models.CASCADE,null=True, blank=True
                               ,related_name='child_ids', verbose_name="Parent")
    
