from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from app.models import Supplier, Category, Product, Employee, Process, Certification, Batch, QualityCheck
from random import choice, randint
from datetime import timedelta

fake = Faker()

class Command(BaseCommand):
    help = 'Generates fake data for all models'

    def handle(self, *args, **kwargs):
        self.create_suppliers()
        self.create_categories()
        self.create_products()
        self.create_employees()
        self.create_processes()
        self.create_certifications()
        self.create_batches()
        self.create_quality_checks()

        self.stdout.write(self.style.SUCCESS('Successfully generated fake data'))

    def create_suppliers(self):
        for _ in range(10):
            Supplier.objects.create(
                supplier_name=fake.company(),
                contact_info=fake.phone_number(),
                country=fake.country(),
                partnership_details=fake.text(max_nb_chars=200)
            )

    def create_categories(self):
        categories = ['Ovins', 'Caprins', 'Porcins']
        for category in categories:
            Category.objects.create(
                category_name=category,
                description=fake.text(max_nb_chars=200)
            )

    def create_products(self):
        categories = list(Category.objects.all())
        for _ in range(20):
            Product.objects.create(
                product_name=fake.word(),
                category=choice(categories),
                origin=fake.country(),
                description=fake.text(max_nb_chars=200),
                packaging_type=fake.word(),
                unit_weight=round(fake.random.uniform(0.1, 10.0), 2),
                stock_quantity=randint(100, 1000),
                price=round(fake.random.uniform(10, 100), 2),
                expiry_date=fake.future_date()
            )

    def create_employees(self):
        departments = ['Production', 'Quality Control', 'Maintenance', 'Administration']
        for _ in range(50):
            Employee.objects.create(
                name=fake.name(),
                position=fake.job(),
                department=choice(departments),
                contact_info=fake.phone_number(),
                training_status=choice(['Trained', 'In Training', 'Pending'])
            )

    def create_processes(self):
        processes = ['Trempage', 'Dégraissage', 'Retournage', 'Pré calibrage', 'Attache', 'Calibrage', 'Salage', 'Emballage']
        for process in processes:
            Process.objects.create(
                process_name=process,
                description=fake.text(max_nb_chars=200),
                duration=timedelta(minutes=randint(30, 180)),
                equipment_used=fake.text(max_nb_chars=100)
            )

    def create_certifications(self):
        certifications = ['ISO 22000:2005', 'ISO 9001:2015', 'HACCP', 'BRC', 'IFS']
        for cert in certifications:
            Certification.objects.create(
                certification_name=cert,
                issuing_authority=fake.company(),
                issue_date=fake.past_date(),
                expiry_date=fake.future_date()
            )

    def create_batches(self):
        products = list(Product.objects.all())
        suppliers = list(Supplier.objects.all())
        for _ in range(100):
            Batch.objects.create(
                product=choice(products),
                supplier=choice(suppliers),
                production_date=fake.past_date(),
                received_date=fake.past_date(),
                expiry_date=fake.future_date(),
                batch_quantity=randint(100, 1000),
                batch_status=choice(['In Production', 'Completed', 'Shipped', 'On Hold'])
            )

    def create_quality_checks(self):
        batches = list(Batch.objects.all())
        employees = list(Employee.objects.filter(department='Quality Control'))
        for _ in range(200):
            QualityCheck.objects.create(
                batch=choice(batches),
                employee=choice(employees),
                check_date=fake.date_time_between(start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone()),
                result=choice(['Pass', 'Fail', 'Pending']),
                remarks=fake.text(max_nb_chars=200)
            )