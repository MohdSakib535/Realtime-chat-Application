from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from useraccount.models import CustomUser


class CustomUserAdmin(UserAdmin):
	list_display = ('email','username','date_joined', 'last_login', 'is_admin','is_staff')
	search_fields = ('email','username',)
	readonly_fields=('id', 'date_joined', 'last_login')

	filter_horizontal = ()
	list_filter = ()
	fieldsets = ()


admin.site.register(CustomUser, CustomUserAdmin)


# admin.site.register(CustomUser)