from django.db import models
from django.contrib.auth.models import User

class Operator(models.Model):
    """This model control the Operator's profile."""
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    department = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'operators'

    def __str__(self):
        """Return a string representation of the model."""
        return self.user.username

class Permission(models.Model):
    """This model create custom permissions."""

class SystemPermissions(Permission):

    class Meta:
        verbose_name = 'System Permission'
        verbose_name_plural = 'System Permissions'
        permissions = (
            ("dbb_edit_permissions", "Can change permissions of Operators."),
            ("dbb_edit_operators", "Can edit profiles from others Operators."),
            ("dbb_view_operators", "Can view all Operators Profile."),
            ("dbb_add_operators", "Can view add new Operators.")
            )