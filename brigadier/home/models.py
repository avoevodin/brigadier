from django.db import models


class Home(models.Model):
    """Not managed model of home page view that contains view
    permission.

    """

    class Meta:
        managed = False

        default_permissions = ()

        permissions = [
            ('view_home', 'Can view home page')
        ]
