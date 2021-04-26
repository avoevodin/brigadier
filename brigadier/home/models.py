from django.db import models
from django.utils.translation import gettext_lazy as _


class Home(models.Model):
    """todo

    """
    class Meta:

        managed = False

        default_permissions = ()

        permissions = [
            ('view_home', _('Can view home page'))
        ]
