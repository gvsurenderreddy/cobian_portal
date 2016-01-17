from django.http import HttpResponseRedirect

__all__ = ['admin_required', 'customer_service_required', 'eula_required']


def admin_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/")

        user_profile = request.user.userprofile
        if user_profile.user_type == "ADMIN":
            return f(request, *args, **kwargs)
        return HttpResponseRedirect("/")
    wrap.__doc__ = f.__doc__
    wrap.__name__= f.__name__
    return wrap


def customer_service_required(f):
    def wrap(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return HttpResponseRedirect("/")

        user_profile = request.user.userprofile
        if user_profile.user_type == "ADMIN" or user_profile.user_type == "CUSTOMER_SERVICE":
            return f(request, *args, **kwargs)
        return HttpResponseRedirect("/")
    wrap.__doc__ = f.__doc__
    wrap.__name__= f.__name__
    return wrap


def eula_required(f):
    def wrap(request, *args, **kwargs):
        user_profile = request.user.userprofile

        user_info_accepted = False
        if user_profile.user.first_name and user_profile.user.last_name and user_profile.user.email:
            user_info_accepted = True

        if user_profile.eula_accepted and user_info_accepted:
            return f(request, *args, **kwargs)
        elif not user_profile.eula_accepted:
            return HttpResponseRedirect("/eula/")
        else:
            return HttpResponseRedirect("/accounts/profile/")

    wrap.__doc__ = f.__doc__
    wrap.__name__= f.__name__
    return wrap