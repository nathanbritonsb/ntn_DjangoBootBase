from django import forms
from .models import Operator
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

class PersonalDataProfileForm(forms.Form):
    """"This is the form used on an operator's profile to edit their information."""

    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.HiddenInput()
    )

    first_name = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    email = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    department = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(
            attrs={'class': 'form-control'}
        )
    )

    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'custom-checkbox'}),
        required=False,
    )

    def __init__(self, can_edit_operator, can_edit_permissions, *args, **kwargs):
        """This is called on initial forms populate."""

        self.can_edit_operator = can_edit_operator
        self.can_edit_permissions = can_edit_permissions

        super().__init__(*args, **kwargs)
        content_type = ContentType.objects.get(app_label='dbb_accounts', model="systempermissions")
        self.fields['permissions'].queryset = Permission.objects.filter(content_type=content_type, codename__startswith='dbb')
        self.fields['permissions'].disabled = not self.can_edit_permissions
        self.fields['first_name'].disabled = not self.can_edit_operator
        self.fields['last_name'].disabled = not self.can_edit_operator
        self.fields['email'].disabled = not self.can_edit_operator
        self.fields['department'].disabled = not self.can_edit_operator
        

    def save(self, commit=True):
        """Function used to save the form."""
        """To make tests, set commit=False"""

        user = User.objects.get(username=self.cleaned_data['username'])
        operator = Operator.objects.get(user__username=self.cleaned_data['username'])

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        operator.department = self.cleaned_data['department']
        selected_permissions = self.cleaned_data['permissions']
        # If Operator has permissions to alter permissions, save!
        if self.can_edit_operator and self.can_edit_permissions:
            user.user_permissions.set(selected_permissions)
        else:
            #TODO: Report incident!
            pass

        if commit:
            if self.can_edit_operator:
                operator.save()
                user.save()
            else:
                #TODO: Report incident!
                pass

        return operator

class AddOperator(forms.Form):

    username = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Username'
                   }
            
        )
    )

    email = forms.CharField(
        max_length=50, 
        required=True, 
        widget=forms.TextInput(
            attrs={'class': 'form-control',
                   'placeholder': 'Email'
                   }
            
        )
    )

    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ''
        })
    )

    def __init__(self, *args, **kwargs):
        """This is called on initial forms populate."""
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        """Function used to save the form."""
        """To make tests, set commit=False"""
        pass