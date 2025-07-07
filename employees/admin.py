from django.contrib import admin
from .models.employee import Employee
initialize_list = ['id', 'name', 'age']
list_employee_display = initialize_list + [field.name for field in Employee._meta.fields if field.name not in initialize_list]
class EmployeeAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Basic Information', {'fields': ['first_name', 'last_name', 'active']}),
        ('Employment Details', {'fields': ['phone', 'birthday']}),
    ]
    list_filter = ['joining_date', 'active']

    list_display = list_employee_display
admin.site.register(Employee, EmployeeAdmin)


from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin  import UserAdmin
from .models.user import EmployeeUser
from .models.department import Department

class EmployeeInline(admin.TabularInline):
    model = EmployeeUser
    can_delete = False
    verbose_name_plural = "Employee Information"
    fk_name = 'user'
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "employee":
            kwargs["queryset"] = kwargs.get("queryset", EmployeeUser._meta.get_field('employee').related_model.objects.filter(active=True))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class CusAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_employee', )
    inlines = (EmployeeInline, )

   
    def get_employee(self, obj):
       try:return obj.profile.employee.name
       except: return ''

    get_employee.short_description = 'Employee Name'

class CusDepartment(admin.ModelAdmin):
    model = Department
    can_delete = False
    verbose_name_plural = "Department Information"


admin.site.unregister(User)
admin.site.register(User, CusAdmin)
admin.site.register(Department, CusDepartment)
