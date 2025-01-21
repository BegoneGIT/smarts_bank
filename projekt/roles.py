from rolepermissions.roles import AbstractUserRole

class Manager(AbstractUserRole):
    available_permissions = {
        'delete_others_proj': True,
        'create_smart': True,
        'create_user': True,
    }

class Employee(AbstractUserRole):
    available_permissions = {
        'create_smart': True,
        'create_user': False,
    }