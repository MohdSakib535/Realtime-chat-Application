from django.contrib import admin
from Notification.models import Notification
# Register your models here.



class NotificationAdmin(admin.ModelAdmin):
    list_display = ['verb','read']
    # readonly_fields = ['user',]

    class Meta:
        model = Notification


admin.site.register(Notification, NotificationAdmin)