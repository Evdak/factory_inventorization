# coding: utf-8
import codecs
from django.contrib import admin
from django.http import HttpResponse

from .models import Import, Export, Defect, Trash, Product, Company, HeatExchanger
from rangefilter.filters import DateRangeFilter, DateTimeRangeFilter
import csv
from import_export.admin import ExportActionMixin


# Register your models here.


@admin.register(Product)
class FilterProduct(ExportActionMixin, admin.ModelAdmin):

    list_display = (
        'product_name',
        'product_number',
        'product_count',
        'product_unit',
        'product_consumption',
        'product_reserves',
        # 'product_type',
        # 'product_export_only'
    )
    list_filter = (
        'product_name',
        'product_number',
        'product_count',
        'product_unit',
        'product_consumption',
        'product_reserves',
        # 'product_type',
        # 'product_export_only'
    )


@admin.register(Import)
class FilterImport(admin.ModelAdmin):
    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        print()
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        response.write(u'\ufeff'.encode('utf8'))
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                  for field in field_names])

        return response

    list_display = (
        "import_date",
        "import_shift",
        "import_name",
        "import_name_heat",
        "import_count",
        "import_unit",
        "import_from",
        "import_document"
    )
    list_filter = (
        "import_date",
        ("import_date", DateRangeFilter),
        "import_shift",
        "import_name",
        "import_name_heat",
        "import_count",
        "import_unit",
        "import_from",
        "import_document"
    )


@admin.register(Export)
class FilterExport(admin.ModelAdmin):

    list_display = (
        "export_date",
        "export_shift",
        "export_name",
        "export_count",
        "export_unit",
        "export_from",
        "export_document",
        "export_duration",
        "export_receive_date",
        # "export_price"
    )
    list_filter = (
        "export_date",
        ("export_date", DateRangeFilter),
        "export_shift",
        "export_name",
        "export_count",
        "export_unit",
        "export_from",
        "export_document",
        "export_duration",
        ("export_receive_date", DateRangeFilter),
        # "export_price"
    )


@admin.register(Defect)
class FilterDefect(admin.ModelAdmin):

    # actions = [export_csv]
    list_display = (
        "defect_date",
        "defect_shift",
        "defect_name",
        "defect_name_heat",
        "defect_count",
        "defect_unit"
    )
    list_filter = (
        "defect_date",
        ("defect_date", DateRangeFilter),
        "defect_shift",
        "defect_name",
        "defect_name_heat",
        "defect_count",
        "defect_unit"
    )


@admin.register(Trash)
class FilterTrash(admin.ModelAdmin):

    # actions = [export_csv]
    list_display = (
        "trash_date",
        "trash_shift",
        "trash_name_str",
        "trash_count",
        "trash_unit"
    )
    list_filter = (
        "trash_date",
        ("trash_date", DateRangeFilter),
        "trash_shift",
        "trash_name_str",
        "trash_count",
        "trash_unit"
    )


@admin.register(Company)
class FilterCompany(admin.ModelAdmin):

    list_display = (
        "company_name",
        "company_inn"
    )
    list_filter = (
        "company_name",
        "company_inn"
    )


@admin.register(HeatExchanger)
class FilterCompany(admin.ModelAdmin):

    list_display = (
        "heatExchanger_name",
        "heatExchanger_number",
        "heatExchanger_count"
    )
    list_filter = (
        "heatExchanger_name",
        "heatExchanger_number",
        "heatExchanger_count"
    )
# admin.site.register(Product, FilterProduct)
# admin.site.register(Import, FilterImport)
# admin.site.register(Export)
# admin.site.register(Defect)
# admin.site.register(Trash)
# admin.site.register(Company)
