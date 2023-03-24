from django.contrib.auth.models import User
from django.db import models


class Tweet(models.Model):
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    text = models.CharField(max_length=2048)
    like_count = models.IntegerField(default=0)

    reply_to = models.ForeignKey('Tweet', null=True, on_delete=models.SET_NULL)

    # or it should be re-counted on render?
    reply_count = models.IntegerField(default=0)
    retweet_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now=True)

    def _get_user_action_by_type(self, user: User, action: str):
        return self.user_actions.filter(user=user, action_type=action).first()

    def liked_by_user(self, user: User) -> bool:
        return self._get_user_action_by_type(user, UserAction.LIKE) is not None

    def retweeted_by_user(self, user: User) -> bool:
        return self._get_user_action_by_type(user, UserAction.RETWEET) is not None


class UserAction(models.Model):
    LIKE = 'like'
    RETWEET = 'retweet'
    REPLY = 'reply'

    user = models.ForeignKey(
        User, related_name='user_actions',
        null=True, on_delete=models.SET_NULL)
    tweet = models.ForeignKey(
        Tweet, related_name='user_actions',
        null=True, on_delete=models.SET_NULL)
    action_type = models.CharField(
        choices=[(LIKE, 'Like'),
                 (RETWEET, 'Retweet'),
                 (REPLY, 'Reply')],
        max_length=16)
