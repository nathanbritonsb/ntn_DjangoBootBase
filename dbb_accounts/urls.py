"""Defines URL patterns for db_accounts app."""

from django.urls import path, include

from . import views


app_name = 'dbb_accounts'
urlpatterns = [
    # Include default auth urls.
    path('', include('django.contrib.auth.urls')),
    path('operators/', views.operators, name='operators'),
    path('operator/<int:operator_id>/', views.operator_profile, name='operator_profile'),
]