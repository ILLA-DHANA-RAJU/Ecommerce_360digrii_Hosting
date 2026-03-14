from django.shortcuts import redirect
from functools import wraps

def customer_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get("customer_id"):
            return view_func(request, *args, **kwargs)
        elif request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        return redirect('login')
    return wrapper


def vendor_login_reqired(login_func):
    @wraps(login_func)
    def vendor(request, *args, **kwargs):
        if request.session.get('vendor_id'):
            return login_func(request, *args, **kwargs)
        return redirect('vendor_login')
    return vendor