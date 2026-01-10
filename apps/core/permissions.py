def is_admin(user):
    return user.is_authenticated and (user.role == 'ADMIN' or user.is_superuser)

def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

def is_employee(user):
    return user.is_authenticated and user.role == 'EMPLOYEE'
