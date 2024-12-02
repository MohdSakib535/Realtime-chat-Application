from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


# from chat.utils import find_or_create_private_chatf
from Notification.models import Notification


class FriendList(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friend_list")
	friends = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="friends_set") 

	# set up the reverse relation to GenericForeignKey
	notifications= GenericRelation(Notification)

	def __str__(self):
		return self.user.username

	
	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "FriendList"

	def is_mutual_friend(self, friend):
		"""
		Is this a friend?
		"""
		if friend in self.friends.all():
			return True
		return False



class FriendRequest(models.Model):
	"""
	A friend request consists of two main parts:
		1. SENDER
			- Person sending/initiating the friend request
		2. RECIVER
			- Person receiving the friend friend
	"""

	sender 	= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="sender")
	receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="receiver")
	is_active= models.BooleanField(blank=False, null=False, default=True)  #once accept request or reject  it is false
	timestamp = models.DateTimeField(auto_now_add=True)
	notifications= GenericRelation(Notification)

	def __str__(self):
		return self.sender.username

	def accept(self):
		"""
		Accept a friend request.
		Update both SENDER and RECEIVER friend lists.
		"""
		receiver_friend_list = FriendList.objects.get(user=self.receiver)
		if receiver_friend_list:
			content_type = ContentType.objects.get_for_model(self)

			# Update notification for RECEIVER
			receiver_notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
			receiver_notification.is_active = False
			receiver_notification.redirect_url = f"{settings.BASE_URL}/account/{self.sender.pk}/"
			receiver_notification.verb = f"You accepted {self.sender.username}'s friend request."
			receiver_notification.timestamp = timezone.now()
			receiver_notification.save()

			receiver_friend_list.add_friend(self.sender)

			sender_friend_list = FriendList.objects.get(user=self.sender)
			if sender_friend_list:

				# Create notification for SENDER
				self.notifications.create(
					target=self.sender,
					from_user=self.receiver,
					redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
					verb=f"{self.receiver.username} accepted your friend request.",
					content_type=content_type,
				)

				sender_friend_list.add_friend(self.receiver)
				# sender_friend_list.save()
				self.is_active = False
				self.save()
			return receiver_notification # we will need this later to update the realtime notifications


	def decline(self):
		"""
		Decline a friend request.
		Is it "declined" by setting the `is_active` field to False
		"""
		self.is_active = False
		self.save()

		content_type = ContentType.objects.get_for_model(self)

		# Update notification for RECEIVER
		notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
		notification.is_active = False
		notification.redirect_url = f"{settings.BASE_URL}/account/{self.sender.pk}/"
		notification.verb = f"You declined {self.sender}'s friend request."
		notification.from_user = self.sender
		notification.timestamp = timezone.now()
		notification.save()

		# Create notification for SENDER
		self.notifications.create(
			target=self.sender,
			verb=f"{self.receiver.username} declined your friend request.",
			from_user=self.receiver,
			redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
			content_type=content_type,
		)

		return notification


	def cancel(self):
		"""
		Cancel a friend request.
		Is it "cancelled" by setting the `is_active` field to False.
		This is only different with respect to "declining" through the notification that is generated.
		"""
		self.is_active = False
		self.save()

		content_type = ContentType.objects.get_for_model(self)

		# Create notification for SENDER
		self.notifications.create(
			target=self.sender,
			verb=f"You cancelled the friend request to {self.receiver.username}.",
			from_user=self.receiver,
			redirect_url=f"{settings.BASE_URL}/account/{self.receiver.pk}/",
			content_type=content_type,
		)

		notification = Notification.objects.get(target=self.receiver, content_type=content_type, object_id=self.id)
		notification.verb = f"{self.sender.username} cancelled the friend request sent to you."
		#notification.timestamp = timezone.now()
		notification.read = False
		notification.save()

	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "FriendRequest"



@receiver(post_save, sender=FriendRequest)
def create_notification(sender, instance, created, **kwargs):
	if created:
		content_type = ContentType.objects.get_for_model(instance)
		notification = Notification.objects.create(
            target=instance.receiver,
            from_user=instance.sender,
            redirect_url=f"{settings.BASE_URL}/account/{instance.sender.pk}/",
            verb=f"{instance.sender.username} sent you a friend request.",
            content_type=content_type,
			object_id=instance.id
        )
		