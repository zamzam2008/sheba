from django.contrib import admin
from .models import *
# Register your models here
# admin.site.register(Transection)
class TransectionAdmin(admin.ModelAdmin):
    list_display = ('date', 'oilLeft','totalOilSale', 'price', 'totalRevenue', 'cashDeposited', 'overdue','oilType', 'dipReading', 'twoPercent', 'comments', 'validTransection',)
    list_filter = ('date','totalOilSale',)
    ordering = ('date','totalRevenue','totalOilSale',)
    search_fields = ('date',)
admin.site.register(Transection,TransectionAdmin)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone','lastPayment', 'totalDue', 'active_customer')
    list_filter = ('name',)
    ordering = ('name','totalDue',)
    search_fields = ('name',)

admin.site.register(Customer,CustomerAdmin)
class StockLeftAdmin(admin.ModelAdmin):
    list_display = ('id','date', 'oilQuantity','oilType')
    list_filter = ('id','date','oilQuantity','oilType')
    ordering = ('id','date',)
    search_fields = ('id','date',)

admin.site.register(StockLeft,StockLeftAdmin)

class OilStockAdmin(admin.ModelAdmin):
    list_display = ('deliveryDate', 'oilQuantity','oilType')
    list_filter = ('deliveryDate','oilType',)
    ordering = ('deliveryDate',)
    search_fields = ('deliveryDate',)

admin.site.register(OilStock,OilStockAdmin)
# admin.site.register(StockLeftOctane)

class DebitToCustomerAdmin(admin.ModelAdmin):
    list_display = ('date', 'oilQuantity','customerID','TodayDue','totalAmountPaid','totalAmountDue' ,'oilType')
    list_filter = ('customerID','oilQuantity','oilType',)
    ordering = ('date',)
    search_fields = ('customerID',)
admin.site.register(DebitToCustomer,DebitToCustomerAdmin)
class GASTransectionAdmin(admin.ModelAdmin):
    list_display = ('inDate', 'quantity','totalSale','cashDeposited','perQubicLiter')
    list_filter = ('inDate','perQubicLiter')
    ordering = ('inDate',)
    search_fields = ('inDate',)

admin.site.register(GASTransection,GASTransectionAdmin)