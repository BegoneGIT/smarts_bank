from django import forms
from django.forms import MultiWidget
from .models import Smart, Tag, ApplicationField, PriceRange
from djmoney.forms.widgets import MoneyWidget
from djmoney.forms.fields import MoneyField

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# class SmartForm(forms.Form):
#     project_name = forms.CharField(max_length=100)
#     details = forms.TextField()        # nullable?
#     how_it_works = models.TextField()
#     similiar_software = models.TextField(null=True)     # we expect comma separated list here
#     userbase = models.TextField()
#     marked_for_del_by  = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.SET_NULL,        #we don't want to lose stuff when user is deleted
#         related_name="deleting_person",
#         null=True,
#         blank=True
#         )
#     delete_order_date = models.DateField(null=True, blank=True)
#     Tag = models.ManyToManyField(Tag)
#     application_field = models.ManyToManyField(ApplicationField)
#     price_range

#     message = forms.CharField(widget=forms.Textarea)
#     sender = forms.EmailField()
#     cc_myself = forms.BooleanField(required=False)



# class Tagelect(forms.SelectMultiple):
#     def create_option(self, name, label, selected, index, subindex=None, attrs=None):
#         option = super().create_option(self,
#             name=name, label=label, selected=selected, index=index, subindex=subindex, attrs=attrs
#         )
#         # if value:
#         #     option["attrs"]["data-price"] = value.instance.price
#         return option

# class PriceRangeSelectorWidget(forms.widgets.MultiWidget):
#     def __init__(self, attrs=None, dt=None, mode=0):  
#         _widgets = (
#             MoneyWidget(amount_widget=forms.TextInput(attrs={'class': 'form-control'}), currency_widget=forms.Select(attrs={'class': 'form-control'})),
#             MoneyWidget(amount_widget=forms.TextInput(attrs={'class': 'form-control'})),
#             )
#         super(PriceRangeSelectorWidget, self).__init__(_widgets, attrs)

#     def decompress(self, value):
#         if value:
#             return [value.start, value.end, value.currency]
#         return [None, None, None]

#     def format_output(self, rendered_widgets):
#         return u''.join(rendered_widgets)

class SmartForm(forms.ModelForm):
    # https://django-autocomplete-light.readthedocs.io/en/master/index.html
    # https://tom-select.js.org/
    # project_name = forms.CharField(max_length=100)
    # how_it_works = forms.CharField(max_length=300)
    # userbase = forms.CharField(max_length=100)
    # similiar_software = forms.CharField(max_length=100)
    # details = forms.CharField(max_length=2000)  
    # price_range = forms.ModelChoiceField(queryset=PriceRange.objects.all())
    # tag_options = 
    tag_options = [('', 'None')] + [(tag.tag_name, tag.tag_name) for tag in Tag.objects.all()]
    field_options = [('', 'None')] + [(field.field_name, field.field_name) for field in ApplicationField.objects.all()]

    # currency_widget = forms.Select(attrs={'class': 'form-control'})
    # price_range = MoneyField(default_currency='PLN',
    #     widget = MultiWidget(attrs={'class': 'mx-2 col-4 mb-2'},
    #         widgets={'start': MoneyWidget, 'end': MoneyWidget}
    #     )
    # )

    price_range_start = MoneyField(widget=MoneyWidget(attrs={'class': 'col-4 textarea half-form-control mx-2 mb-2'}),max_digits=14, decimal_places=2, default_currency='PLN')
    price_range_end = MoneyField(widget=MoneyWidget(attrs={'class': 'textarea half-form-control mx-2 col-4 mb-2'}), max_digits=14, decimal_places=2, default_currency='PLN')
    tag = forms.CharField(widget=forms.SelectMultiple(attrs={'rows': 1, 'class': 'tom-tag', "novalidate": ''}, choices=tag_options),#ListTextWidget(data_list=(('a', 'a'), ('b', 'b')), name='country-list', attrs={'class': 'tom-Tag'}),
                )       # queryset=Tag.objects.all(),| , label=lambda instance: instance.tag_name
    application_field = forms.CharField(widget=forms.SelectMultiple(choices=field_options, attrs={'rows': 1, 'class': 'tom-tag', "novalidate": ''}),#ListTextWidget(data_list=(('a', 'a'), ('b', 'b')), name='country-list', attrs={'class': 'tom-Tag'}),
                )    #, label=lambda instance: instance.field_name
    

    def __init__(self, *args, **kwargs):
        super(SmartForm, self).__init__(*args, **kwargs)
        self.fields['tag'].label_from_instance = lambda instance: instance.tag_name # this simply uses chosen field as label
        self.fields['application_field'].label_from_instance = lambda instance: instance.field_name
        # self.fields['price_range_start'].label_classes = "f_sized"
        
    class Meta:
        model = Smart
        fields = ['project_name', 'how_it_works',  'userbase', 'similiar_software', 'details', 'price_range']   #'tag', 'application_field',

        widgets = {
            'project_name': forms.Textarea(attrs={'rows': 1, 'cols': 5}),
            'how_it_works': forms.Textarea(attrs={'rows': 2}),
            # 'tag': forms.SelectMultiple(attrs={'rows': 1, 'class': 'tom-Tag', 'background-color': 'red'}),
            # 'application_field': forms.Textarea(attrs={'rows': 1, 'id': 'tom-Tag'}),
            'price_range': forms.HiddenInput(),
            'userbase': forms.Textarea(attrs={'rows': 1}),
            'similiar_software': forms.Textarea(attrs={'rows': 1}),
            'details': forms.Textarea(attrs={'rows': 8}),
        }

'''
interesting: https://stackoverflow.com/questions/46877213/django-create-customuser-model?rq=3
'''
class UserForm(UserCreationForm):   #forms.ModelForm, 

    CHOICES = (
        ('REG', 'reagular user'),
        ('MAN', 'manager'),
    )
    assign_role = forms.ChoiceField(choices=CHOICES, required=False)      # or use Select

    class Meta:
        model = User
        fields = ('username', 'first_name' , 'last_name', 'email')


class LoginForm(forms.ModelForm):
    '''Simple login form'''
    class Meta:
        model = User
        fields = ('username', 'password')