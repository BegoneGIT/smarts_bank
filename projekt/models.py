from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from djmoney.models.fields import MoneyField

class Tag(models.Model):
    tag_name = models.CharField(max_length=50, unique=True)

class ApplicationField(models.Model):       # what fields (management, mining, construction) use this software
    field_name = models.CharField(max_length=50, unique=True)

class PriceRange(models.Model):
    price_start = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')
    price_end = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')
    updated = models.DateTimeField(auto_now=True)

class CorpoTeam(models.Model):
    """Team will allow for simpler notification sending

    Args:
        models (_type_): _description_
    """
    team_name = models.CharField(max_length=50)
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="members")
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="manager",
        null=True
    )


class Smart(models.Model):
    project_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,        #we don't want to lose stuff when user is deleted
        related_name="author",
        null=True
        )
    details = models.TextField()        # nullable?
    how_it_works = models.TextField()
    similiar_software = models.TextField(null=True)     # we expect comma separated list here
    userbase = models.TextField()
    marked_for_del_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,        #we don't want to lose stuff when user is deleted
        related_name="deleting_person",
        null=True,
        blank=True
        )
    delete_order_date = models.DateField(null=True, blank=True)
    tag = models.ManyToManyField(Tag)
    application_field = models.ManyToManyField(ApplicationField)
    price_range = models.ForeignKey(PriceRange, on_delete=models.CASCADE)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(str(self.id)[-1]+self.project_name)
        super().save(*args, **kwargs)

class Notification(models.Model):
    notification_type = models.CharField(
        max_length=30,
        choices={
            'DEL': 'Marked for delete',
            'ACC': 'Accepted',
            'PERM': 'Deleted'
        }
    )
    text = models.TextField(null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,        #we don't want to lose stuff when user is deleted
        related_name="notification_author"
        )
    
    recipient = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="recipient")        # is it really cheaper than reference by Teams?
    refers = models.ForeignKey(Smart, on_delete=models.CASCADE)

class SmartsVoting(models.Model):
    voter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,        #we don't want to lose stuff when user is deleted
        related_name="voter"
        )
    voted_project = models.ForeignKey(
        Smart,
        on_delete=models.CASCADE,        #we don't want to lose stuff when user is deleted
        related_name="voted_project"
        )
    
