
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync


# def send_notification_to_user(user_id, message):
#     channel_layer = get_channel_layer()
#     print('channel layer utils----------',channel_layer)
#     async_to_sync(channel_layer.group_send)(
#         f"notifications_{user_id}",  # Group name based on user ID
#         {
#             "type": "send_notification",  # This calls `send_notification` in the consumer
#             "notification": message,
#         }
#     )














# import threading
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

# def send_notification_to_user(user_id, message):
#     # Start a new thread to handle notification
#     notification_thread = threading.Thread(target=_send_notification_thread, args=(user_id, message))
#     notification_thread.start()

# def _send_notification_thread(user_id, message):
#     # Function to send notification to WebSocket in a separate thread
#     channel_layer = get_channel_layer()
#     print('channel layer utils----------',channel_layer)
#     print(f"friend_request_user_{user_id}")
#     async_to_sync(channel_layer.group_send)(
#         f"friend_request_user_{user_id}",  # Group name based on user ID
#         {
#             "type": "send_notification",  # This calls `send_notification` in the consumer
#             "notification": message,
#         }
#     )
