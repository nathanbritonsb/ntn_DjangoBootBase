## Reusing the Project

1 - In new project, create the directory “ntn_DjangoBootBase”
2 - Copy the dbb_accounts and dbb_design to this new directory
3 - On project settings, add this on top:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / 'ntn_DjangoBootBase'))
```

4 - On project settings, install the apps adding this on installed apps:

```python
INSTALLED_APPS = [
'dbb_design', # All design files
'dbb_accounts', # Accounts of operators of system. Dont control user consumers.
```

5 - On settings on end of file, add this:

```python
#-------------------------------#
#      Authentication Config    #
#-------------------------------#
LOGIN_REDIRECT_URL = 'new_project:index'
LOGOUT_REDIRECT_URL = 'new_project:index'
LOGIN_URL = 'dbb_accounts:login'
AUTHENTICATION_BACKENDS = [
"django.contrib.auth.backends.ModelBackend",
]
```

6 - Now, we need configure urls to assign /accounts to app dbb_accounts. For this, add the follow code on [urls.py](http://urls.py) of main project:

```python
path('accounts/', include('dbb_accounts.urls')),
```