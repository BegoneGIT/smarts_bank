from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.models import User
from django.views.generic import DetailView, UpdateView, FormView, ListView, View, DeleteView, CreateView

from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.roles import assign_role

from ..forms import UserForm




class AddUserView(HasPermissionsMixin, CreateView):
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

        return redirect("user-create")
        
        



    '''do we really need this? do we need to hide built-in?
    kind of yes, all users will have some kind of permission'''