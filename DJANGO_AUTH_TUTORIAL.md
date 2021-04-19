* 
User.objects.create()
User.objects.create_user()
user1.save()
*
user1.check_password()
user1.set_password()
user1.save()
* pprint
```python
from pprint import pprint
pprint(user2.__dict__)
```

* auth
```python
from django.contrib.auth import authenticate
log = authenticate(username='john', password='123') # if is_active=True
```
* logout
```python
from django.contrib.auth import logout
```
* ContentType
```python
from django.contrib.auth.models import ContentType
cts = ContentType.objects.all()
pprint([(c.app_label, c.model) for c in cts.all().order_by('app_label')])
```
* Permissions
```python
from pprint import pprint
log = authenticate(username='john', password='123') # if is_active=True
perms = Permission.objects.all()
pprint([(p.content_type.app_label, p.content_type.model, p.codename) 
        for p in perms.order_by('content_type__app_label', 'content_type__model')])
p_view = Permission.objects.filter(codename__startswith='view_')
log.user_permissions.set(p_view)
log.is_staff = True
log.save()

p_add = Permission.objects.filter(codename__startswith='add_')
log.user_permissions.add(*p_add)
log.user_permissions.remove(*p_add)
log.user_permissions.clear()
log.user_permissions.add(*p_add,*p_view)
```

* Group
```python
gr_view = Group.objects.create(name='Readonly')
gr_view.permissions.add(*p_view)
log.groups.add(gr_view)
gr_view.user_set.add(log) # or, with no duplicate
```
*
```python
p_usr = Permission.objects.filter(content_type=ContentType.objects.get_for_model(User))

ct_auth = ContentType.objects.filter(app_label='auth')
p_auth = Permission.objects.filter(content_type__in=ct_auth)

gr_auth = Group.objects.create(name='Edit users, groups, permissions')
gr_auth.permissions.set(p_auth)
log.groups.add(gr_auth)

log.has_perm('auth.add_user')
pprint([f'{p.content_type.app_label}.{p.codename}' for p in gr_auth.permissions.all()])
log.has_perms([f'{p.content_type.app_label}.{p.codename}' for p in gr_auth.permissions.all()])
```

* Login required mixin
* Permission required mixin
* Access mixin for 403 redirect
* Include native login views and create templates
* Start app accounts
* Create AccountsLoginView from LoginView model of auth
* urls.py of accounts import LoginView and
```python
app_name = 'accounts'
urlpatterns = [
    path('login/', AccountsLoginView.asView(), name='login')
]
```

* instruction for docker-compose