from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from restaurant.models import Order, MenuItem, Category

class Command(BaseCommand):
    help = 'Creates a staff group and assigns permissions'

    def handle(self, *args, **options):
        staff_group, created = Group.objects.get_or_create(name='Staff')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created "Staff" group'))
        else:
            self.stdout.write('Staff group already exists')

        # Models to give permissions for
        models = [Order, MenuItem, Category]
        
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            for perm in permissions:
                staff_group.permissions.add(perm)
                self.stdout.write(f'Added permission {perm.codename} for {model.__name__}')
        
        self.stdout.write(self.style.SUCCESS('Successfully assigned all permissions to "Staff" group'))
