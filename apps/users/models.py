from __future__ import unicode_literals

from django.db import models
from ..login.models import User


class MessageManager(models.Manager):
    def post_message(self, postData, messageReceiver, loggedUser):
        errors = []
        if len(postData['content']) < 2:
            errors.append("Message must be longer than two characters.")

        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            message = self.create(content=postData['content'], author=loggedUser.firstname)
            message.user.add(messageReceiver)
            message.save()
            response_to_views['status'] = True
            response_to_views['message'] = message
        return response_to_views

    def get_messages(self):
        response_to_views = Message.objects.all()
        return response_to_views



class Message(models.Model):
    content = models.TextField()
    author = models.TextField()
    user = models.ManyToManyField(User, related_name="all_user_messages")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

class CommentManager(models.Manager):
    def post_comment(self, postData, commentReceiver, loggedUser, currentMessage):
        errors = []
        if len(postData['content']) < 2:
            errors.append("Comment must be longer than two characters.")

        response_to_views = {}
        if errors:
            response_to_views['status'] = False
            response_to_views['error'] = errors
        else:
            comment = self.create(content=postData['content'], author=loggedUser.firstname)
            comment.user.add(commentReceiver)
            comment.message.add(currentMessage)
            comment.save()
            print("Comment presumably saved successfully")
            response_to_views['status'] = True
            response_to_views['comment'] = comment
        return response_to_views

    def get_comments(self):
        response_to_views = Message.objects.all()
        return response_to_views

class Comment(models.Model):
    content = models.TextField()
    author = models.TextField()
    user = models.ManyToManyField(User, related_name="all_user_comments")
    message = models.ManyToManyField(Message, related_name="all_message_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
