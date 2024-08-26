from django.db import models

class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=100)
    contact_info = models.TextField()
    country = models.CharField(max_length=50)
    partnership_details = models.TextField()

    def __str__(self):
        return self.supplier_name

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    origin = models.CharField(max_length=50)
    description = models.TextField()
    packaging_type = models.CharField(max_length=50)
    unit_weight = models.FloatField()
    stock_quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField()

    def __str__(self):
        return self.product_name

class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    department = models.CharField(max_length=50)
    contact_info = models.TextField()
    training_status = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Process(models.Model):
    process_id = models.AutoField(primary_key=True)
    process_name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField()
    equipment_used = models.TextField()

    def __str__(self):
        return self.process_name

class Certification(models.Model):
    certification_id = models.AutoField(primary_key=True)
    certification_name = models.CharField(max_length=100)
    issuing_authority = models.CharField(max_length=100)
    issue_date = models.DateField()
    expiry_date = models.DateField()

    def __str__(self):
        return self.certification_name

class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    production_date = models.DateField()
    received_date = models.DateField()
    expiry_date = models.DateField()
    batch_quantity = models.IntegerField()
    batch_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Batch {self.batch_id} - {self.product.product_name}"

class QualityCheck(models.Model):
    qc_id = models.AutoField(primary_key=True)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_date = models.DateField()
    result = models.CharField(max_length=50)
    remarks = models.TextField()

    def __str__(self):
        return f"QC {self.qc_id} for Batch {self.batch.batch_id}"