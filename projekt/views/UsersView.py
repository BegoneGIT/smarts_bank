from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.views.generic import DetailView, UpdateView, FormView, ListView, View, DeleteView, CreateView
from django.contrib import messages

from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.roles import assign_role

from ..forms import UserForm        #, LoginForm



class UserLoginView(LoginView):
    """Simple view to allow for a login

    Args:
        LoginView (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = User
    template_name = "login.html"
    # form = LoginForm

    # def redirect_authenticated_user(self):
    # def get_context_data(self, **kwargs):        #  request, smart_id
    #     context = super(AddUserView, self).get_context_data(**kwargs)

    #     messages.success(self.info, "You have to log in to see the details")
        
    #     return context

    def get_success_url(self):
        return reverse("bank-main")

class UserLogoutView(View):
    """Logout view. We redirect to it and after logging them out
    we redirect to another view instantly. Therefore user should never
    see a template loaded.

    Args:
        View (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = User
    template_name = "login.html"
    # form = LoginForm

    # def redirect_authenticated_user(self):
    def get(self, request):
        logout(request)
        messages.info(self.request, "You have been logged out.")
        return redirect("bank-main")
        


class AddUserView(HasPermissionsMixin, CreateView):
    """This is view supposed to be used by admins and managers.
    It will add an user to 'Smart' suggestion system. Be careful as 
    manager can create another manager accounts (by design).

    Args:
        HasPermissionsMixin (_type_): _description_
        CreateView (_type_): _description_

    Returns:
        _type_: _description_
    """
    required_permission = 'create_user'
    template_name = 'AddUserTemplate.html'
    model = User
    context_object_name = 'user'
    # fields = '__all__'
    form_class = UserForm
 
    def __init__(self, *args, **kwargs):
        super(AddUserView, self).__init__(*args, **kwargs)

        self.PERMISSIONS_DICT = {
            'REG': 'employee',
            'MAN': 'manager',
            }

    def get_context_data(self, **kwargs):        #  request, smart_id
        context = super(AddUserView, self).get_context_data(**kwargs)

        # context['info'] = "fghjasvghjasfjhvfasdjhvfasvhj"
        return context
    
    def form_valid(self, form):
        # user = self.get_object()    #????
        user = form.save(commit=False)
        user.save()

        role = form.cleaned_data['assign_role']
        assign_role(user, self.PERMISSIONS_DICT[role])      #TODO if error here EMIT an error message

        messages.success(self.request, f"New User {user.username} added.")
        return redirect("user-create")
        