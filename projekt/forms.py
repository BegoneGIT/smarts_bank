from django import forms
from django.forms import MultiWidget
from .models import Smart, Tag, ApplicationField, PriceRange
from djmoney.forms.widgets import MoneyWidget
from djmoney.forms.fields import MoneyField

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

    # price_range_start = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')
    # price_range_end = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')
    price_range = MoneyField(widget = MultiWidget(attrs={'class': 'mx-2 col-4 mb-2'},
        widgets={'start': MoneyWidget(default_currency='PLN'), 'end': MoneyWidget(default_currency='PLN')}))
    # currency_widget = forms.Select(attrs={'class': 'form-control'})

    tag = forms.CharField(widget=forms.SelectMultiple(attrs={'rows': 1, 'class': 'tom-tag', "novalidate": ''}, choices=tag_options),#ListTextWidget(data_list=(('a', 'a'), ('b', 'b')), name='country-list', attrs={'class': 'tom-Tag'}),
                )       # queryset=Tag.objects.all(),| , label=lambda instance: instance.tag_name
    application_field = forms.CharField(widget=forms.SelectMultiple(choices=field_options, attrs={'rows': 1, 'class': 'tom-tag', "novalidate": ''}),#ListTextWidget(data_list=(('a', 'a'), ('b', 'b')), name='country-list', attrs={'class': 'tom-Tag'}),
                )    #, label=lambda instance: instance.field_name
    

    def __init__(self, *args, **kwargs):
        super(SmartForm, self).__init__(*args, **kwargs)
        self.fields['tag'].label_from_instance = lambda instance: instance.tag_name # this simply uses chosen field as label
        self.fields['application_field'].label_from_instance = lambda instance: instance.field_name
        
    class Meta:
        model = Smart
        fields = ['project_name', 'how_it_works',  'userbase', 'similiar_software', 'details']   #'tag', 'application_field',

        widgets = {
            'project_name': forms.Textarea(attrs={'rows': 1, 'cols': 5}),
            'how_it_works': forms.Textarea(attrs={'rows': 2}),
            # 'tag': forms.SelectMultiple(attrs={'rows': 1, 'class': 'tom-Tag', 'background-color': 'red'}),
            # 'application_field': forms.Textarea(attrs={'rows': 1, 'id': 'tom-Tag'}),
            'userbase': forms.Textarea(attrs={'rows': 1}),
            'similiar_software': forms.Textarea(attrs={'rows': 1}),
            'details': forms.Textarea(attrs={'rows': 8}),
        }

    # def save(self, *args, **kwargs): 
    #     # if not commit: 
    #     #     raise NotImplementedError("Can't create User and Userextended without database save") 
    #     smart = super().save(*args, **kwargs)

    #     # create many2many records
    #     print(smart.how_it_works)
    #     input_tags = self.no_dupe_lowercase(smart.tag.all())     # lower case and remove duplicates
    #     input_fields = self.no_dupe_lowercase(smart.application_field.all())
    #     # price_range = smart.price_range
    #     smart.tag.clear()#= None#.delete()
    #     smart.application_field.clear()#= None#.delete()
    #     # price_range.delete()

    #     # smart.save()  # sum,ting wong

    #     # print(self.request.user)
    #     # raise Exception()
    #     print('input_tags',input_tags)
    #     print('input_fields',input_fields)
    #     tag = Tag.objects.bulk_create(input_tags, batch_size=8, ignore_conflicts=True)
    #     print(tag)
    #     tag.save()
    #     smart.tag.set(tag)        # this should work, else https://stackoverflow.com/questions/4959499/how-to-add-multiple-objects-to-manytomany-relationship-at-once-in-django

    #     app_field = ApplicationField.objects.bulk_create(input_fields, batch_size=8, ignore_conflicts=True)
    #     print(app_field)
    #     app_field.save()
    #     smart.application_field.set(app_field)

    #     print('ARE THOSE THINGS CALLED EVEN?')

    #     return smart
    
    # def no_dupe_lowercase(self, records: list)->set:
    #     return set([r.lower() for r in records])     