from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.html import escape

from dtwee_app.models import Tweet
from dtwee_app.render import render_macro
from dtwee_app.services import like, retweet, reply_to


@login_required(login_url='login/')
def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse(login_view))

    ts = Tweet.objects.prefetch_related('author').order_by('-created_at')
    return render(request, 'home.html', context={'tweets': ts})


def login_view(request):
    if request.method == 'POST':
        if 'login_username' not in request.POST:
            return HttpResponse('`login_username` is a required param', 'text/plain', 400)
        if 'login_password' not in request.POST:
            return HttpResponse('`login_password` is a required param', 'text/plain', 400)

        username = request.POST['login_username']
        password = request.POST['login_password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse(home))
    return render(request, 'register.html')


@login_required(login_url='login/')
def logout_view(request):
    if request.method != 'GET':
        return HttpResponse(f'{request.method} method is not allowed', 'text/plain', 405)
    logout(request)
    return redirect(reverse(login_view))


@login_required(login_url='login/')
def add_tweet(request):
    if request.method == 'POST':
        if 'tweet_input' not in request.POST:
            return HttpResponse('`tweet_input` is a required param', 'text/plain', 400)
    print(request.POST)
    reply = Tweet.objects.create(
        text=escape(request.POST['tweet_input']),
        author=request.user
    )
    if 'reply_to_tweet_id' in request.POST:
        original_tweet = Tweet.objects.get(pk=request.POST['reply_to_tweet_id'])
        reply_to(original_tweet, request.user, reply)
    return redirect(reverse(home))


@login_required(login_url='login/')
def like_tweet_view(request):
    if not request.method == 'POST':
        return HttpResponse(f'{request.method} method is not allowed', 'text/plain', 405)
    if 'tweet_id' not in request.POST:
        return HttpResponse('`tweet_id` is a required param', 'text/plain', 400)
    t = Tweet.objects.get(id=request.POST['tweet_id'])
    like(t, request.user)
    return render_macro(
        request, 'home.html', 'tweet', t=t
    )


@login_required(login_url='retweet/')
def retweet_view(request):
    if not request.method == 'POST':
        return HttpResponse(f'{request.method} method is not allowed', 'text/plain', 405)
    if 'tweet_id' not in request.POST:
        return HttpResponse('`tweet_id` is a required param', 'text/plain', 400)
    t = Tweet.objects.get(id=request.POST['tweet_id'])
    retweet(t, request.user)
    return render_macro(
        request, 'home.html', 'tweet', t=t
    )

