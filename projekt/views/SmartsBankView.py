from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# from django.views import View, ListView
from django.views.generic import DetailView, UpdateView, FormView, ListView, View, DeleteView, CreateView

from rolepermissions.mixins import HasPermissionsMixin

# from djmoney.money import Money
from ..models import Smart, Tag, ApplicationField, PriceRange, SmartsVoting, CorpoTeam
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
        # print(context['price_range'].price_start.amount, type(context['price_range'].price_start))

        return context
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.info, "You have to log in to see the details")
        
        return super().dispatch(request, *args, **kwargs)
    

class SmartCreateView(HasPermissionsMixin, CreateView):
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
    model = Smart
    template_name = 'SmartDisplayTemplate.html'

    # def get_context_data(self, **kwargs):
    # def get(self, request, **kwargs):
    def get_context_data(self, **kwargs):        #  request, smart_id
        context = super(RegisterSmartVoteView, self).get_context_data(**kwargs)
        # self.object = self.get_object()
        # context=super().get_context_data(**kwargs)
        user = self.request.user
        slug = self.request.GET.get('slug')
        print("SLUG:", slug)
        smart = get_object_or_404(Smart, slug=kwargs['object'].slug)
        # smart = Smart.objects.get(slug=slug)

        try:
            SmartsVoting.objects.get_or_create(voter=user, voted_project=smart)
            messages.info(self.request, "You successfully voted for a project.")
        except Exception:
            messages.error(self.request, "For some reason voting did not work properly. Check if you are logged in.")

        redirect('bank-smart', slug=slug)
        return context

class CorpoTeamAssignView(CreateView):
    model = CorpoTeam
    template_name = ".html"
