from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import Http404
from django.contrib import messages

from .models import Operator
from django.contrib.auth.models import User, Permission

from.forms import PersonalDataProfileForm, AddOperator

def list_operators():
    """list all operators"""
    pass

def get_operator_profile(operator_id):
    """get all operator profile data """
    operator_data = Operator.objects.filter(user=operator_id).first()

    fulldata = {
        'operator': operator_data,
        'operator_info': {
            'id': operator_data.user.id,
            'department': operator_data.department,
            }
    }

    return fulldata

def get_all_operators_profile():
    """Return List of Dict with all operator profiles."""
    all_operators = Operator.objects.all()
    operators_profile = []
    
    for operator in all_operators:
        operator = get_operator_profile(operator.user)
        operators_profile.append(operator)
    
    return operators_profile

def edit_operator_profile(operator_id, can_edit_operator, can_edit_permissions, postdata):
    form = PersonalDataProfileForm(can_edit_operator, 
                                   can_edit_permissions,
                                   postdata)
    if form.is_valid():
        result = form.save()

def operator_profile(request, operator_id=None):
    """control interact with operator profile"""
    
    # Verify whether the URL contains the operator ID and retrieve their data.
    if operator_id == None:
        operator_id = request.user.id
    operator = get_operator_profile(operator_id)
    user = User.objects.get(id=operator_id)

    # The user is trying view his own profile?
    if operator_id != request.user.id:
        # If the user dont trying view his own profile, Does he have the permission to see other profiles?
        if not request.user.has_perm('dbb_accounts.dbb_view_operators'):
            # If the user dont have the permission to see other profiles, Does he have permission to edit other profiles?
            if not request.user.has_perm('dbb_accounts.dbb_edit_operators'):
                raise Http404
    
    can_edit_operator=False
    can_edit_permissions=False

    if request.user.has_perm('dbb_accounts.dbb_edit_operators') or operator_id == request.user.id:
        can_edit_operator=True
        if request.user.has_perm('dbb_accounts.dbb_edit_permissions'):
            can_edit_permissions=True

    # If request isn't a POST, the initial form will be populated with Operator Profile Data.
    if request.method != 'POST':
        form = PersonalDataProfileForm(can_edit_operator, can_edit_permissions,
                                       initial={
                                                'username' : operator['operator'],
                                                'first_name' : operator['operator'].user.first_name,
                                                'last_name' : operator['operator'].user.last_name,
                                                'email' : operator['operator'].user.email,
                                                'department' : operator['operator_info']['department'],
                                                'permissions' : operator['operator'].user.user_permissions.all()
                                                })
        # Send data to the Template
        context = {'form' : form, 'operator' : operator}
        return render(request, 'dbb_accounts/operator_profile.html', context)
    else:
        postdata = request.POST
        save = edit_operator_profile(operator_id, can_edit_operator, can_edit_permissions, postdata)
        return redirect('dbb_accounts:operator_profile', operator_id=operator_id)
    
def operators(request):
    """List all operators of system."""
    # Current Operator (request user)
    operator = get_operator_profile(request.user.id)

    if request.method != 'POST':
        add_form = AddOperator()
        pass
    
    elif request.method == 'POST' and request.POST['action'] == 'add':
        # If is POST request, call the function add_operator with request data
        add_form = add_operator(request)
        if isinstance(add_form, str):
            # Use messages from django to send error message to page
            messages.error(request, add_form)
            # Repopulate the form with values
            add_form = AddOperator(request.POST)
        else:
            return redirect('dbb_accounts:operator_profile', operator_id=add_form)

    # Default return when page loaded without POST
    operators = get_all_operators_profile()
    context = {'operators' : operators, 'operator' : operator, 'add_form' : add_form}
    return render(request, 'dbb_accounts/operators.html', context)

def add_operator(request):
    """Add Operator"""
    # Send the request POST data to form AddOperator
    add_form = AddOperator(request.POST)

    if not request.user.has_perm('dbb_accounts.dbb_add_operators'):
        return "Error: You dont have permission to Add new Operators."
    # If form is valid, init create process.
    if add_form.is_valid():
        # Before create user, verify if username or email already exists
        if User.objects.filter(username=add_form.cleaned_data.get('username')).exists() or User.objects.filter(email=add_form.cleaned_data.get('email')).exists():
           return "Error: Username or email already exists. Please try again."
        else:
            # Create user
            userCreated = User.objects.create_user(username=add_form.cleaned_data.get('username'),
                                                   email=add_form.cleaned_data.get('email'),
                                                   password=add_form.cleaned_data.get('password'))
            # Create Operator Profile for user
            operatorCreate = Operator.objects.create(user=userCreated,department="")
            return userCreated.id
    return str(add_form.errors)

            