from django.urls import path
from . import views
app_name = 'HishabNikash'
urlpatterns = [
    path('', views.home, name='hnHome'),
    path('transection/<str:oilType>', views.viewTransection, name='hnTransection'),
    path('addtransection/', views.addTransection, name='hnAddTransection'),
    path('statement/', views.viewTransMonthStatement,
         name='hnTranStatementDetails'),

    path('addstock/', views.addStock, name='hnAddStock'),
    path('seestock/<str:oilType>', views.viewStock, name='hnStockDetails'),
    path('stockStatement/', views.viewMonthStockStatement, name='hnStockStatement'),

    path('customerList/', views.viewAllCustomer, name='hnCustomerList'),
    path('custmerDue/<int:id>', views.customerDueDetails,
         name='hnStatementDetails'),
    path('newcustomerdue/<int:id>',
         views.customerNewTransection, name='hnNewCustomerDue'),

    path('addcngtransection/', views.CNGaddTransection,
         name='hnAddCNGTransection'),
    path('cngtransection/', views.viewCNGTransection, name='hnCNGTransection'),
    path('cngMonthlystatement/', views.viewCNGMonthlyTransection,
         name='hnCNGMonthlyStatement'),
]
