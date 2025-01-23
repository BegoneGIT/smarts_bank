from django.db import models
from django.conf import settings
from django.template.defaultfilters import slugify
from djmoney.models.fields import MoneyField

class Tag(models.Model):
    """Simple model holding tags

    Args:
        models (_type_): _description_
    """
    tag_name = models.CharField(max_length=50, unique=True)

class ApplicationField(models.Model):       # what fields (management, mining, construction) use this software
    """This model contains ApplicationFields that are supposed to describe
    what kind of business field the project relates to

    Args:
        models (_type_): _description_
    """
    field_name = models.CharField(max_length=50, unique=True)

class PriceRange(models.Model):
    """This model says what is supposed market price of the similiar software

    Args:
        models (_type_): _description_
    """
    price_start = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')
    price_end = MoneyField(max_digits=14, decimal_places=2, default_currency='PLN')
    updated = models.DateTimeField(auto_now=True)

class CorpoTeam(models.Model):
    """Team will allow for simpler notification sending
    Corpo teams are created from admin panel as only admins should have access to this action

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
    """Project ideas are named 'smarts' and contain all usefull information about project

    Args:
        models (_type_): _description_
    """
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
    price_range = models.ForeignKey(PriceRange, on_delete=models.CASCADE, blank=True)
    slug = models.SlugField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(str(self.id)[-1]+self.project_name)
        super().save(*args, **kwargs)

class Notification(models.Model):
    """Persistent, database-driven notifications are 
    responsible for manager-employee communication when it comes to project ideas

    Args:
        models (_type_): _description_
    """
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
    """Simple connection between voting user and project they voted for

    Args:
        models (_type_): _description_
    """
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

class CorpoVoteCounter(models.Model):
    """Vote counter simplifies vote counting for specific teams
    and reduces overhead.

    Args:
        models (_type_): _description_
    """
    corpo_team = models.ForeignKey(
        CorpoTeam,
        on_delete=models.CASCADE,        #we don't want to lose stuff when user is deleted
        related_name="counter"
        )
    
    related_proj = models.ForeignKey(
        Smart,
        on_delete=models.CASCADE,        #we don't want to lose stuff when user is deleted
        related_name="related_proj"
        )

    counter = models.IntegerField(default=1)
    
