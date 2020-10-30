from notification.models import Notification
from accounts.models import User

def send(msg,users):
    for user in users:
        notification = Notification(notification=msg,to=user)
        notification.save()
