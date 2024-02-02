from django.contrib.admin import ModelAdmin, register

from .models import CustomUser, Following

# TODO: написать админку и выполнить все по списку из notes.txt!

@register(CustomUser)
class UserAdmin(ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email']
    list_filter = ['email', 'username']

@register(Following)
class FollowingAdmin(ModelAdmin):
    pass
