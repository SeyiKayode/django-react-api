from django.contrib import admin
from .models import Tutorial, CustomUser
# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser

admin.site.register(Tutorial)
admin.site.register(CustomUser, CustomUserAdmin)