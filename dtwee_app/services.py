from django.contrib.auth.models import User

from .models import Tweet, UserAction


def _tweet_action_generic(
        t: Tweet,
        user: User,
        action_type: str,
        tweet_metric_name: str
):
    assert hasattr(t, tweet_metric_name)
    assert action_type in (UserAction.LIKE, UserAction.RETWEET, UserAction.REPLY)

    deleted_count, _ = UserAction \
        .objects \
        .filter(user=user, tweet=t, action_type=action_type) \
        .delete()

    if deleted_count:
        setattr(t, tweet_metric_name, getattr(t, tweet_metric_name) - 1)
        t.save()
    else:
        setattr(t, tweet_metric_name, getattr(t, tweet_metric_name) + 1)
        t.save()
        UserAction.objects.create(
            user=user,
            tweet=t,
            action_type=action_type
        )


def like(t: Tweet, user: User):
    """Like tweet as a user. Remove like if liked already"""
    return _tweet_action_generic(
        t=t,
        user=user,
        action_type=UserAction.LIKE,
        tweet_metric_name='like_count')


def retweet(t: Tweet, user: User):
    """Retweet as a user. Remove retweet if done already"""
    return _tweet_action_generic(
        t=t,
        user=user,
        action_type=UserAction.RETWEET,
        tweet_metric_name='retweet_count'
    )


def reply_to(t: Tweet, user: User, reply_t: Tweet):
    UserAction.objects.create(
        user=user,
        tweet=t,
        action_type=UserAction.REPLY
    )
    t.reply_count += 1
    t.save()

    # feels weird. Should action contain several tweets?
    reply_t.reply_to = t
    reply_t.save()
