from datetime import timedelta
from django.utils import timezone

def create_access_token(user):
    import oauth2_provider.models
    Application = oauth2_provider.models.get_application_model()
    AccessToken = oauth2_provider.models.get_access_token_model()
    token_expiration_time = timezone.now() + timedelta(minutes=60)
    token = AccessToken.objects.create(
        user=user,
        scope='read write packages',
        token='test{}{}'.format(
            user.id,
            int(token_expiration_time.timestamp()),
        ),
        application=Application.objects.first(),
        expires=token_expiration_time,
    )
    return token

def auth_header(token):
    return { 'HTTP_AUTHORIZATION': 'Bearer {}'.format(token) }

def assign_perms(group_permissions):
    """
    Assigns permissions to a set of groups.

    `group_permissions` looks like: { 'group_name': ['app.permission'] }
    """
    from django.contrib.auth.models import Group
    from guardian.shortcuts import assign_perm

    for name, permissions in group_permissions.items():
        group = Group.objects.get(name=name)
        for permission in permissions:
            assign_perm(permission, group)

def group_has_perm(group, perm, obj):
    """
    Returns true if the group named `group` has permission `perm` for
    the given model instance `obj`.

    `group` can be an instance of Group or a string
    """
    from django.contrib.auth.models import Group
    from guardian.shortcuts import get_objects_for_group

    if isinstance(group, str):
        g = Group.objects.get(name=group_name)
    else:
        g = group

    return get_objects_for_group(
        g, perm
    ).filter(id=obj.id).exists()

def user_has_group_perm(user, perm, obj):
    """
    Returns true if one of the groups that the `user is part of has the
    given permission `perm` for the given model instance `obj`.
    """
    from guardian.shortcuts import get_objects_for_group

    for g in user.groups.all():
        if group_has_perm(g, perm, obj):
            return True
    return False
