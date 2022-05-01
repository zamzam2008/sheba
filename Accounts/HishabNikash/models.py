# Create your models here.
from django.db import models
import datetime
# Create your models here.

class Transection(models.Model):
    date = models.DateField()
    oilLeft = models.DecimalField(max_digits=19, decimal_places=3,verbose_name= 'Oil in Stock')
    totalOilSale = models.DecimalField(max_digits=19, decimal_places=3,verbose_name= 'Total Oil Sale')
    price = models.DecimalField(max_digits=19, decimal_places=3,verbose_name= 'Price')
    totalRevenue = models.DecimalField(max_digits=19, decimal_places=3,verbose_name= 'Total Sale(Taka)')
    cashDeposited =models.DecimalField(max_digits=19, decimal_places=3,verbose_name= 'Total Cash')
    overdue = models.DecimalField(max_digits=19, decimal_places=3,verbose_name= 'Total Due')
    oilType = models.CharField(max_length=10,verbose_name= 'Oil Type')
    comments = models.TextField(verbose_name = 'Comments', default='')
    dipReading = models.DecimalField(max_digits=19, decimal_places=3, default=0,verbose_name= 'DIP Reading')
    twoPercent = models.DecimalField(max_digits=19, decimal_places=3,default=0,verbose_name= 'Two Percent')
    validTransection = models.BooleanField(default=True, verbose_name= 'Valid Transection')
    date_added = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.date)+'  ,  '+ str(self.oilLeft)+'  ,  '+str(self.totalOilSale)+'  ,  '+str(self.price)+'  ,  '+ str(self.totalRevenue)+'  ,  '+str(self.cashDeposited)+'  ,  '+ str(self.overdue)+'  ,  '+self.oilType+'  ,  '+ str(self.comments)+'  ,  '+str(self.validTransection)+'  ,  '+str(self.dipReading)+'  ,  '+str(self.twoPercent)
    
    # class Meta:
    #     db_table = 'Transection'
    #     # Add verbose name
    #     verbose_name = 'Transection'
    
# class OilStoced(models.Model):
class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100,default='NA')
    phone = models.CharField(max_length=15)
    totalDue = models.DecimalField(max_digits=19, decimal_places=3,default=0)
    lastPayment = models.DecimalField(max_digits=19, decimal_places=3,default=0)
    date_added = models.DateTimeField(auto_now=True)
    active_customer = models.BooleanField(default=True)
    
    def __str__(self):
        # return str(self.name)+'  ,  '+ str(self.phone)+'  ,  '+str(self.lastPayment)+'  ,  '+str(self.totalDue)+'  ,  '+str(self.active_customer)
        return str(self.name)
class OilStock(models.Model):
    deliveryDate = models.DateField()
    oilQuantity = models.DecimalField(max_digits=19, decimal_places=3)
    # oilUnitPrice = models.DecimalField(max_digits=19, decimal_places=3)
    # payOderFee = models.DecimalField(max_digits=19, decimal_places=3)
    # governmentFee = models.DecimalField(max_digits=19, decimal_places=3)
    # totalFee = models.DecimalField(max_digits=19, decimal_places=3)
    oilType = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.deliveryDate)+'  ,  '+ str(self.oilQuantity)+'  ,  ' +self.oilType
    
    
    # def __str__(self):
    #     return str(self.deliveryDate)+'  ,  '+ str(self.oilQuantity)+'  ,  '+str(self.oilUnitPrice)+'  ,  '+ str(self.payOderFee)+'  ,  '+str(self.governmentFee)+'  ,  '+ str(self.totalFee)+'  ,  '+self.oilType
    
    
class StockLeft(models.Model):
    date = models.DateField()
    oilQuantity = models.DecimalField(max_digits=19, decimal_places=3)
    oilType = models.CharField(max_length=10)
    date_added = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.date)+'  ,  '+ str(self.oilQuantity)+'  ,  '+self.oilType+'  ,  '+str(self.id)

# class StockLeftOctane(models.Model):
#     date = models.DateField()
#     oilQuantity = models.DecimalField(max_digits=19, decimal_places=3)
#     oilType = models.CharField(max_length=10,default='Octane')
#     date_added = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return str(self.date)+'  ,  '+ str(self.oilQuantity)+'  ,  '+self.oilType

class DebitToCustomer(models.Model):
    date = models.DateField()
    oilQuantity = models.DecimalField(max_digits=19, decimal_places=3)
    oilType = models.CharField(max_length=10)
    customerID = models.ForeignKey('Customer', on_delete=models.RESTRICT)
    TodayDue = models.DecimalField(max_digits=19, decimal_places=3,default=0)
    totalAmountDue = models.DecimalField(max_digits=19, decimal_places=3,default=0)
    totalAmountPaid = models.DecimalField(max_digits=19, decimal_places=3,default=0)
    oilUnitPrice = models.DecimalField(max_digits=19, decimal_places=3,default=0)
    date_added = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.date)+' , '+ str(self.oilQuantity)+' ,  '+str(self.TodayDue) +'  ,  '+str(self.totalAmountDue) +'  ,  '+str(self.totalAmountPaid) +' ,  '+str(self.TodayDue) +'  ,  '+' ,  '+str(self.oilUnitPrice) +'  ,  '+str(self.oilType) 
    
class GASTransection(models.Model):
    inDate = models.DateField()
    quantity = models.DecimalField(max_digits=19, decimal_places=3)
    totalSale = models.DecimalField(max_digits=19, decimal_places=3)
    cashDeposited = models.DecimalField(max_digits=19, decimal_places=3)
    perQubicLiter = models.DecimalField(max_digits=19, decimal_places=3)
    date_added = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.inDate)+'  ,  '+ str(self.quantity)+'  ,  '+str(self.totalSale) +'  ,  '+str(self.cashDeposited) +'  ,  '+str(self.perQubicLiter) 
    
class GASLastReading(models.Model):
    date_added = models.DateTimeField(auto_now=True)
    quantity = models.DecimalField(max_digits=19, decimal_places=3)
    
    def __str__(self):
        return  str(self.quantity)