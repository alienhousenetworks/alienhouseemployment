from django.core.management.base import BaseCommand
from apps.organization.models import EmployeeProfile


class Command(BaseCommand):
    help = 'Generate employee_id for existing EmployeeProfile records that do not have one'

    def handle(self, *args, **options):
        employees_without_id = EmployeeProfile.objects.filter(employee_id__isnull=True)
        
        count = employees_without_id.count()
        if count == 0:
            self.stdout.write(
                self.style.SUCCESS('All employee records already have employee IDs.')
            )
            return

        self.stdout.write(f'Found {count} employee records without IDs. Generating...')
        
        for emp in employees_without_id:
            emp.generate_employee_id()
            emp.save()
            self.stdout.write(f'Generated ID for {emp.user.email}: {emp.employee_id}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated IDs for {count} employees.')
        )

