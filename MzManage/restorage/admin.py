from django.contrib import admin
from restorage.models import (
                       UserType,
                       Role,
                       Department,
                       User
                      )

# Register your models here.
admin.site.register(UserType)
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Department)
