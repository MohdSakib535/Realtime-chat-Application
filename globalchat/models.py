from django.db import models
from useraccount.models import CustomUser
# Create your models here.


class PublicChatRoom(models.Model):

	# Room title
	title = models.CharField(max_length=255, unique=True, blank=False)
	

	def __str__(self):
		return self.title


	def connect_user(self, user):
		"""
		return true if user is added to the users list
		"""
		is_user_added = False
		if not user in self.users.all():
			self.users.add(user)
			self.save()
			is_user_added = True
		elif user in self.users.all():
			is_user_added = True
		return is_user_added 


	def disconnect_user(self, user):
		"""
		return true if user is removed from the users list
		"""
		is_user_removed = False
		if user in self.users.all():
			self.users.remove(user)
			self.save()
			is_user_removed = True
		return is_user_removed 


	@property
	def group_name(self):
		"""
		Returns the Channels Group name that sockets should subscribe to to get sent
		messages as they are generated.
		"""
		return "PublicChatRoom-%s" % self.id

class PublicRoomChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = PublicRoomChatMessage.objects.filter(room=room).order_by("-timestamp")
        return qs


class PublicRoomChatMessage(models.Model):
    """
    Chat message created by a user inside a PublicChatRoom
    """
    user   = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room   = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
    timestamp  = models.DateTimeField(auto_now_add=True)
    content   = models.TextField(unique=False, blank=False,)

    objects = PublicRoomChatMessageManager()

    def __str__(self):
        return self.content
