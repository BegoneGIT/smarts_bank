from rolepermissions.roles import AbstractUserRole

class Manager(AbstractUserRole):
    available_permissions = {
        'delete_others_proj': True,
    }

class Employee(AbstractUserRole):
    available_permissions = {
        'create_proj': True,
    }