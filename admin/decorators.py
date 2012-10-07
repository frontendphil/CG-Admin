from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from functools import wraps

from models import User

def login_required(fn):

    def decorator(request, *args, **kwargs):
        user_id = request.session.get("user")

        if user_id:
            user = User.objects.get(pk=user_id)

            if user:
                return fn(request, *args, **kwargs)

        return HttpResponseRedirect(reverse("login"))

    return wraps(fn)(decorator)

def anonymous_only(fn):
    def decorator(request, *args, **kwargs):
        user_id = request.session.get("user")

        if user_id:
            return HttpResponseRedirect(reverse("index"))

        return fn(request, *args, **kwargs)

    return wraps(fn)(decorator)