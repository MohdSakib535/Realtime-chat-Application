from django.db import models
from useraccount.models import CustomUser

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="created_rooms")
    participants = models.ManyToManyField(CustomUser, related_name="rooms")
    is_video_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Call(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="calls")
    caller = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="calls_initiated")
    callee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="calls_received")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Call between {self.caller.username} and {self.callee.username} in {self.room.name}"



class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications")
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} at {self.timestamp}"
