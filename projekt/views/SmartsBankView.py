from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.db.models import F



# from django.views import View, ListView
from django.views.generic import DetailView, UpdateView, FormView, ListView, View, DeleteView, CreateView

from rolepermissions.mixins import HasPermissionsMixin

# from djmoney.money import Money
from ..models import Smart, Tag, ApplicationField, PriceRange, SmartsVoting, CorpoTeam, CorpoVoteCounter
from ..forms import SmartForm
# import projekt.models     # this causes an error, check how to properly import models
# from .forms import YourModelForm

class SmartsBankView(ListView):
    template_name = 'SmartsBankTemplate.html'
    model = Smart
    context_object_name = 'smarts'
    # model = YourModel
    # form_class = YourModelForm

    # def get(self, request):     #https://docs.djangoproject.com/en/5.1/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object
    #     objects = self.model.objects.all()
    #     return render(request, self.template_name, {'objects': ['stuff','stuff','stuff']})

    # def get_queryset(self):
    #     return super().get_queryset()
    
    def get_context_data(self, **kwargs):        #  request, smart_id
        context = super(SmartsBankView, self).get_context_data(**kwargs)

        # context['info'] = "fghjasvghjasfjhvfasdjhvfasvhj"

        # context['price_dict'] = {"element1": "123", "ele2": 547}
        context['username'] = self.request.user.username

        context['smarts_list'] = Smart.objects.all()

        return context
    # def post(self, request):
    #     form = self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(reverse('your_list_view'))
    #     return render(request, self.template_name, {'form': form})

    # def put(self, request, pk):
    #     obj = get_object_or_404(self.model, pk=pk)
    #     form = self.form_class(request.PUT, instance=obj)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponse(status=204)
    #     return HttpResponse(status=400)

    # def delete(self, request, pk):
    #     obj = get_object_or_404(self.model, pk=pk)
    #     obj.delete()
    #     return HttpResponse(status=204)

@method_decorator(login_required, name='dispatch')
class SmartDisplayView(DetailView):
    template_name = 'SmartDisplayTemplate.html'
    model = Smart

    def get_context_data(self, **kwargs):        #  request, smart_id
        context = super(SmartDisplayView, self).get_context_data(**kwargs)

        context['smart'] = get_object_or_404(Smart, slug=kwargs['object'].slug)
        # print(context['smart'].created_by)
        context['price_range'] = context['smart'].price_range
        own_c_team = CorpoTeam.objects.filter(team_members=self.request.user)
        context['team_votes'] = CorpoVoteCounter.objects.filter(corpo_team__in=own_c_team)
        # for v in context['team_votes']:
        #     print('v)
        print(context['team_votes'])

        if self.request.user.is_superuser:
            context['all_votes'] = CorpoVoteCounter.objects.filter(related_proj=context['smart'])
            print(context['all_votes'])
        # subquery = CorpoTeam.
        # print([f for f in User._meta.get_fields()
        #     if f.auto_created and not f.concrete])
        # print(own_c_team)
        # user = self.request.user
        # subquery = own_c_team.filter(team_members) #..objects.corpoteam_set.filter(corpo_team__id=self.request.user)
        # print(subquery)
        # Publication.objects.filter(article__headline__startswith="NASA")
        # context['votes'] = SmartsVoting.objects(voter__in, voted_project=context['smart'])
        # print(context['price_range'].price_start.amount, type(context['price_range'].price_start))

        return context
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            messages.info(self.request, "You have to log in to see the details")
        
        return super().dispatch(request, *args, **kwargs)
    

class SmartCreateView(HasPermissionsMixin, CreateView):
    """Responsible for creating single 'smarts'. Creates price range automatically.
    If user decided to create new Tag or ApplicationField the view will also create new
    objects in database to represent them.

    Args:
        HasPermissionsMixin (_type_): _description_
        CreateView (_type_): _description_

    Returns:
        _type_: _description_
    """
    required_permission = 'create_smart'
    template_name = 'SmartCreateTemplate.html'
    model = Smart
    form_class = SmartForm

    def form_valid(self, form):
        # form.save(commit=False)

        # smart = form.instance
        with transaction.atomic():
            # print(smart)
            # print(smart.how_it_works)
            
            smart = form.save(commit=False)
            smart.created_by = self.request.user
            # quit()
            # print(form.cleaned_data['price_range_start'].amount)
            # input_price_start = form.cleaned_data['price_range_start_0'][0], form.cleaned_data['price_range_start_1'][0]
            # input_price_end = form.cleaned_data['price_range_end_0'][0], form.cleaned_data['price_range_end_1'][0]
            # print(input_price_start[0])
            # print(input_price_end)
            real_range, _ = PriceRange.objects.get_or_create(price_start=form.cleaned_data['price_range_start'], price_end=form.cleaned_data['price_range_end'])
            smart.price_range = real_range
            smart.save()

            # NOTE we would love to use form.cleaned_data, but it will make our inputs a str
            form_cont = dict(self.request.POST)
            input_tags = self.no_dupe_lowercase(form_cont['tag'])   #form_cont['Ttag']     # lower case and remove duplicates
            input_fields = self.no_dupe_lowercase(form_cont['application_field'])


            tags=[]
            for name in input_tags:
                tag, created = Tag.objects.get_or_create(tag_name=name)
                tags.append(tag)
            smart.tag.set(tags)
            # print(tag)
            # tag.save()
            # smart.tag.set(tag)        # this should work, else https://stackoverflow.com/questions/4959499/how-to-add-multiple-objects-to-manytomany-relationship-at-once-in-django

            # ap = [ApplicationField(field_name=field_name) for field_name in input_fields]
            # app_field = ApplicationField.objects.bulk_create(ap, batch_size=8, ignore_conflicts=True)
            # print(app_field)
            # app_field.save()
            a_fields = []
            for name in input_fields:
                a_field, created = ApplicationField.objects.get_or_create(field_name=name)
                a_fields.append(a_field)
            smart.application_field.set(a_fields)
            messages.success(self.request, "Smart created successfully!")


            # smart.save()
        # return HttpResponseRedirect(reverse("bank-main"))#self.get_success_url()
        return redirect("bank-main")#super(SmartCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):        #  request, smart_id
        context = super(SmartCreateView, self).get_context_data(**kwargs)

        context['Tag'] = Tag.objects.all()

        return context

    def no_dupe_lowercase(self, records: list)->set:
            return set([r.lower() for r in records])

class RegisterSmartVoteView(DetailView):
    """Saves information about user voting on specific 'smart'.
    Updates counter for that 'smart' to represent current vote count.
    If any kind of error happens, the appopriate non-persistent message is sent to inform user.

    Args:
        DetailView (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = Smart
    template_name = 'SmartDisplayTemplate.html'

    # def get_context_data(self, **kwargs):
    # def get(self, request, **kwargs):
    def get(self, request, *args, **kwargs):        #  request, smart_id
        # context = super(RegisterSmartVoteView, self).get(request, **kwargs)
        # self.object = self.get_object()
        # context=super().get_context_data(**kwargs)
        smrt = get_object_or_404(Smart, slug=kwargs['slug'])
        user = self.request.user

        # smart = Smart.objects.get(slug=slug)

        own_c_team = CorpoTeam.objects.filter(team_members=self.request.user)
        if not own_c_team:
            messages.error(self.request, "For some reason voting did not work properly. Check if you are logged in.")
            return redirect('bank-smart', slug=kwargs['slug'])  #context

        # try:
        vote, created = SmartsVoting.objects.get_or_create(voter=user, voted_project=smrt)
        if created:
            # print('TEAM\n\t',own_c_team, '\n')
            for team in own_c_team:
                obj, created = CorpoVoteCounter.objects.get_or_create(corpo_team=team, related_proj=smrt)
                if not created:
                    obj.counter = F("counter") + 1
                    obj.save(update_fields=["counter"])
        else:
            messages.warning(self.request, "You already voted for that project.")

        messages.info(self.request, "You successfully voted for a project.")
        # except Exception:
        #     messages.error(self.request, "For some reason voting did not work properly. Check if you are logged in.")
        #     raise Exception
        return redirect('bank-smart', slug=kwargs['slug'])  #context
        

class SmartAssignTeamView(UpdateView):
    model = Smart
    template_name = ".html"

    def get(self, request, *args, **kwargs):        #  request, smart_id
        smrt = get_object_or_404(Smart, slug=kwargs['slug'])
        team = get_object_or_404(CorpoTeam, id=kwargs['team'])
        print('???')
        
        smrt.working_team = team
        smrt.save()
        messages.success(self.request, "Project was assignet to a team.")

        return redirect('bank-smart', slug=kwargs['slug'])


        
