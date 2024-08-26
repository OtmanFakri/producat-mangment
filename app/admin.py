from .models import Supplier, Category, Product, Employee, Process, Certification, Batch, QualityCheck
from django.contrib import admin
from django.db.models import Count
from django.http import JsonResponse
from django.urls import path
from django.db.models.functions import TruncDate, Cast
from django.db.models import DateField


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('batch_id', 'product', 'production_date', 'batch_quantity', 'batch_status')
    list_filter = ('product', 'batch_status')
    date_hierarchy = 'production_date'
    list_per_page = 10  # record 10 per page


@admin.register(QualityCheck)
class QualityCheckAdmin(admin.ModelAdmin):
    list_display = ('qc_id', 'batch', 'employee', 'check_date', 'result')
    list_filter = ('result', 'check_date')
    date_hierarchy = 'check_date'
    list_per_page = 10  # record 10 per page

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('qc_chart_data/', self.admin_site.admin_view(self.qc_chart_data_view)),
        ]
        return custom_urls + urls

    def qc_chart_data_view(self, request):
        chart_data = (
            QualityCheck.objects.annotate(date=Cast('check_date', DateField()))
            .values('date')
            .annotate(count=Count('qc_id'))
            .order_by('date')
        )
        return JsonResponse(list(chart_data), safe=False)


class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'country', 'contact_info')
    list_per_page = 10
    search_fields = ('supplier_name', 'country')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'description')
    list_per_page = 10
    search_fields = ('category_name',)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'department', 'training_status')
    list_per_page = 10
    list_filter = ('department', 'training_status')
    search_fields = ('name', 'position')


class ProcessAdmin(admin.ModelAdmin):
    list_display = ('process_name', 'description', 'duration')
    list_per_page = 10
    search_fields = ('process_name',)


class CertificationAdmin(admin.ModelAdmin):
    list_display = ('certification_name', 'issuing_authority', 'issue_date', 'expiry_date')
    list_per_page = 10
    list_filter = ('issuing_authority',)
    search_fields = ('certification_name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'origin', 'stock_quantity', 'price')
    list_filter = ('category', 'origin')
    search_fields = ('product_name', 'description')
    list_per_page = 10  # record 10 per page

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('chart_data/', self.admin_site.admin_view(self.chart_data_view)),
        ]
        return custom_urls + urls

    def chart_data_view(self, request):
        chart_data = (
            Category.objects.annotate(product_count=Count('product'))
            .values('category_name', 'product_count')
        )
        return JsonResponse(list(chart_data), safe=False)


admin.site.register(Supplier)
admin.site.register(Category)
admin.site.register(Process)
admin.site.register(Certification)
