from django.contrib import admin

from .models import Subscriptions, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('email', 'username', )


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.register(Subscriptions, SubscriptionsAdmin)
admin.site.register(User, UserAdmin)
