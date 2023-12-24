from account.models import Role


def is_user_or_admin(user):
    return any([user.has_permission_user('Teacher'), user.has_permission_user('Admin')])
