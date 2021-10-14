from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Subscriptions


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('email', 'username', )


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(User, UserAdmin)




