from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models.users import User
from django.utils.translation import gettext_lazy as _
from django.db.models import Count


@admin.register(User)
class UserAdmin(UserAdmin):
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('email',)}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff',  'is_superuser', 'groups', 'user_permissions',),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','username'),
        }),
    )
    list_display = ('id', 'email','first_name','last_name','username' )

    list_display_links = ('id',)
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
    search_fields = ('first_name', 'last_name', 'id', 'email',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)