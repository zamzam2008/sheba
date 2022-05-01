from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
from datetime import *
from django.db.models import Q, Sum, Avg
from decimal import Decimal


# Create your views here.
app_name = 'HishabNikash'


def home(req):
    # return HttpResponse('<h1> FILLING STATION</h1>')
    displayData = True
    return render(req, 'index.html', {'dd': displayData})


def viewTransection(req, oilType=''):
    oilType = oilType.capitalize()
    context = {}
    currentMonth = datetime.now().month
    if oilType == 'Diesel':
        dieselStock = models.Transection.objects.filter(
            Q(date__month=currentMonth) & Q(oilType=oilType)).all()
        totalDiesel = models.Transection.objects.filter(Q(date__month=currentMonth) & Q(oilType=oilType)).aggregate(
            Sum('totalOilSale'), Sum('totalRevenue'), Sum('cashDeposited'), Sum('overdue'), Sum('twoPercent'))
        if totalDiesel['totalOilSale__sum']:
            context = {
                'trans': dieselStock,
                'oilType': oilType,
                'total': True,
                'totalOilSale': round(totalDiesel['totalOilSale__sum'], 3),
                'totalSale': round(totalDiesel['totalRevenue__sum'], 3),
                'totalCash': round(totalDiesel['cashDeposited__sum'], 3),
                'totalDue': round(totalDiesel['overdue__sum'], 3),
                'totalTwoPercent': round(totalDiesel['twoPercent__sum'], 3),
            }
        else:
            context = {
                'trans': dieselStock,
                'oilType': oilType,
                'total': False,
            }
    else:
        octaneStock = models.Transection.objects.filter(
            Q(date__month=currentMonth) & Q(oilType=oilType)).all()
        totalOctane = models.Transection.objects.filter(Q(date__month=currentMonth) & Q(oilType=oilType)).aggregate(
            Sum('totalOilSale'), Sum('totalRevenue'), Sum('cashDeposited'), Sum('overdue'), Sum('twoPercent'))
        if totalOctane['totalOilSale__sum']:
            context = {
                'trans': octaneStock,
                'oilType': oilType,
                'total': True,
                'totalOilSale': round(totalOctane['totalOilSale__sum'], 3),
                'totalSale': round(totalOctane['totalRevenue__sum'], 3),
                'totalCash': round(totalOctane['cashDeposited__sum'], 3),
                'totalDue': round(totalOctane['overdue__sum'], 3),
                'totalTwoPercent': round(totalOctane['twoPercent__sum'], 3),
            }
        else:
            context = {
                'trans': octaneStock,
                'oilType': oilType,
                'total': False,
            }

    return render(req, 'transection.html', context=context)


def addTransection(req):
    octaneStock = models.StockLeft.objects.filter(id=1).values('oilQuantity')
    diesel = models.StockLeft.objects.filter(id=2).values('oilQuantity')
    # octaneStock = models.StockLeft.objects.get(id=3)
    # diesel = models.StockLeft.objects.get(id=4)
    ds = float(diesel[0]['oilQuantity'])
    ot = float(octaneStock[0]['oilQuantity'])
    print(ot, octaneStock)
    print(ds, diesel)
    comment = 'নাই'
    if req.POST:
        inDate = req.POST['inDate']
        # stock = req.POST.get('stored', False)
        oilAmount = float(req.POST['oilAmount'])
        price = float(req.POST['price'])
        totalAmount = float(req.POST['takaAmount'])
        # cash = float(req.POST['cash'])
        due = float(req.POST['due'])
        cash = totalAmount - due
        dip = float(req.POST['dip'])
        oilType = req.POST['oilType'].capitalize()
        if oilType == 'Diesel':
            if ((oilAmount * price == totalAmount) and (totalAmount / price == oilAmount)) and (ds - oilAmount == dip):
                validEntry = True
            else:

                validEntry = False
                twoPercent = oilAmount*.02
                stck = ds - oilAmount
                stck += twoPercent
                s = round((oilAmount * price), 3)
                st = round(stck, 3)
                dp = round(dip, 3)
                tkDiff = s - totalAmount
                oilDiff = round((stck - dp), 3)
                totalAmount = round(totalAmount, 3)
                comment = 'মোট বিক্রয় (টাকায়):' + str(s) + ', ' + 'আমরা পেয়েছি: ' + str(totalAmount)+', পার্থক্য(টাকায়): '+str(
                    tkDiff) + ', Stock থাকা উচিত: ' + str(st)+', ' + 'আমরা পেয়েছি: ' + str(dip)+', পার্থক্য(স্টক): '+str(oilDiff)
            models.Transection.objects.create(date=inDate, oilLeft=ds, totalOilSale=oilAmount,
                                              price=price, totalRevenue=totalAmount, cashDeposited=cash, overdue=due,
                                              oilType=oilType, validTransection=validEntry, dipReading=dip, twoPercent=twoPercent, comments=comment)

            models.StockLeft.objects.filter(id=2).update(oilQuantity=stck)
        else:
            if ((oilAmount * price == totalAmount) and (totalAmount / price == oilAmount)) and (ds - oilAmount == dip):
                validEntry = True
            else:
                validEntry = False
                twoPercent = oilAmount*.02
                stck = ot - oilAmount
                stck += twoPercent
                s = round((oilAmount * price), 3)
                st = round(stck, 3)
                dp = round(dip, 3)
                tkDiff = round((s - totalAmount), 3)
                oilDiff = round((stck - dp), 3)
                comment = 'মোট বিক্রয় (টাকায়):' + str(s) + ', ' + 'আমরা পেয়েছি: ' + str(totalAmount)+', পার্থক্য(টাকায়): '+str(
                    tkDiff) + ', Stock থাকা উচিত: ' + str(st)+', ' + 'আমরা পেয়েছি: ' + str(dip)+', পার্থক্য(স্টক): '+str(oilDiff)

            models.Transection.objects.create(date=inDate, oilLeft=ot, totalOilSale=oilAmount,
                                              price=price, totalRevenue=totalAmount, cashDeposited=cash, overdue=due,
                                              oilType=oilType, validTransection=validEntry, dipReading=dip, twoPercent=twoPercent, comments=comment)

            models.StockLeft.objects.filter(id=1).update(oilQuantity=stck)

        url = '/transection/'+oilType
        return redirect(url)

    return render(req, 'addTransection.html')


def viewTransMonthStatement(req):
    # return HttpResponse('<h1> FILLING STATION</h1>')
    displayData = False
    No_Data = False
    context = {
        'displayData': displayData,
    }
    if req.POST:
        startDate = req.POST['sDate']
        endDate = req.POST['eDate']
        oilType = req.POST['oilType']
        trans = models.Transection.objects.filter(
            date__range=[startDate, endDate], oilType=oilType).all()
        calculation = models.Transection.objects.filter(Q(date__range=[startDate, endDate]) & Q(oilType=oilType)).aggregate(
            Sum('totalOilSale'), Sum('totalRevenue'), Sum('cashDeposited'), Sum('overdue'), Sum('twoPercent'))
        print(trans)
        if len(trans) == 0:
            No_Data = True
            context = {
                'displayData': True,
                'No_Data': No_Data,
                'trans': trans,
                'oilType': oilType,
            }
        else:
            context = {
                'displayData': True,
                'No_Data': No_Data,
                'trans': trans,
                'oilType': oilType,
                'total': True,
                'totalOilSale': round(calculation['totalOilSale__sum'], 3),
                'totalSale': round(calculation['totalRevenue__sum'], 3),
                'totalCash': round(calculation['cashDeposited__sum'], 3),
                'totalDue': round(calculation['overdue__sum'], 3),
                'totalTwoPercent': round(calculation['twoPercent__sum'], 3),
            }
    return render(req, 'viewMonth.html', context=context)


def viewMonthStockStatement(req):
    # return HttpResponse('<h1> FILLING STATION</h1>')
    # displayData = True
    displayData = False
    No_Data = False
    context = {
        'displayData': displayData,

    }
    if req.POST:
        startDate = req.POST['sDate']
        endDate = req.POST['eDate']
        oilType = req.POST['oilType']
        trans = models.OilStock.objects.filter(
            deliveryDate__range=[startDate, endDate], oilType=oilType).all()
        total = models.Transection.objects.filter(date__range=[startDate, endDate], oilType=oilType).annotate(TotalOilSale=Sum(
            'totalOilSale'), TotalTaka=Sum('totalRevenue'), TotalTakaGiven=Sum('cashDeposited'), TotalTakaBaki=Sum('overdue'))
        print(trans)
        if len(trans) == 0:
            No_Data = True
        else:
            displayData = True
        context = {
            'displayData': displayData,
            'No_Data': No_Data,
            'trans': trans,
            'oilType': oilType,
            'total': total
        }
    return render(req, 'viewMonthStock.html', context=context)


def addStock(req):
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    octaneStock = models.StockLeft.objects.filter(id=1).values('oilQuantity')
    diesel = models.StockLeft.objects.filter(id=2).values('oilQuantity')
    ds = float(diesel[0]['oilQuantity'])
    ot = float(octaneStock[0]['oilQuantity'])
    if req.POST:
        oilType = req.POST['oilType'].capitalize()
        date = req.POST['inDate']
        oilAmount = float(req.POST['oilAmount'])

        if oilType == 'Diesel':
            models.OilStock.objects.create(
                deliveryDate=date, oilQuantity=oilAmount, oilType=oilType)
            oilAmount += ds
            models.StockLeft.objects.filter(id=2).update(oilQuantity=oilAmount)
            # models.StockLeft.objects.create(date=date,oilQuantity = oilAmount,oilType = oilType)
        else:
            models.OilStock.objects.create(
                deliveryDate=date, oilQuantity=oilAmount, oilType=oilType)
            oilAmount += ot
            models.StockLeft.objects.filter(id=1).update(oilQuantity=oilAmount)
        url = '/seestock/'+oilType
        return redirect(url)
    else:
        return render(req, 'addStock.html')


def viewStock(req, oilType=''):
    oilType = oilType.capitalize()
    context = {}
    currentMonth = datetime.now().month
    if oilType == 'Diesel':
        dieselStock = models.OilStock.objects.filter(
            Q(deliveryDate__month=currentMonth) & Q(oilType=oilType)).all()
        context = {
            'trans': dieselStock,
            'oilType': oilType
        }
    else:
        octaneStock = models.OilStock.objects.filter(
            Q(deliveryDate__month=currentMonth) & Q(oilType=oilType)).all()
        context = {
            'trans': octaneStock,
            'oilType': oilType,
        }
    return render(req, 'stockDetails.html', context=context)


def viewAllCustomer(req):
    if req.POST:
        pass
    customer = models.Customer.objects.all()
    context = {
        'customer': customer
    }
    return render(req, 'allCustomer.html', context=context)


def customerDueDetails(req, id):
    # trans = models.DebitToCustomer.objects.filter(customerID=id).order_by('date')
    # cus = models.Customer.objects.filter(id=id).all()
    cusInfo = getCustomerINFO(id)
    trans = cusInfo[0]
    cus = cusInfo[1]
    cusID = cus[0].id
    context = {
        'CusName': cus[0].name,
        'cusID': cusID,
        'totalDue': cus[0].totalDue,
        'lastPayment': cus[0].lastPayment,
        'trans': trans,
        'customer': cus,
    }
    return render(req, 'customerTransDetails.html', context=context)


def customerNewTransection(req, id):
    customerInfo = models.Customer.objects.filter(id=id).values('totalDue')
    customerInfo = customerInfo[0]['totalDue']
    if req.POST:
        date = req.POST['inDate']
        oilAmount = req.POST['oilAmount']
        price = req.POST['price']
        takaAmount = int(req.POST['takaAmount'])
        oilType = req.POST['oilType']
        joma = int(req.POST['cash'])
        if joma > 0:
            totalDue = customerInfo - joma
            models.Customer.objects.filter(id=id).update(
                totalDue=totalDue, lastPayment=joma)
            cust = models.Customer.objects.get(id=id)
            models.DebitToCustomer.objects.create(date=date, oilQuantity=oilAmount, oilType=oilType, customerID=cust,
                                                  TodayDue=takaAmount, totalAmountDue=totalDue, totalAmountPaid=joma, oilUnitPrice=price)
        else:
            totalDue = customerInfo + takaAmount
            models.Customer.objects.filter(id=id).update(totalDue=totalDue)
            cust = models.Customer.objects.get(id=id)
            models.DebitToCustomer.objects.create(date=date, oilQuantity=oilAmount, oilType=oilType, customerID=cust,
                                                  TodayDue=takaAmount, totalAmountDue=totalDue, totalAmountPaid=joma, oilUnitPrice=price)
        url = 'http://127.0.0.1:8000/custmerDue/'+str(id)
        return redirect(url)

    return render(req, 'newCustomerDue.html')


def getCustomerINFO(id):

    trans = models.DebitToCustomer.objects.filter(
        customerID=id).order_by('date')
    cus = models.Customer.objects.filter(id=id).all()
    return [trans, cus]


def viewCNGTransection(req):

    month = datetime.now().month
    mydate = datetime.now()
    month_name = mydate.strftime("%B")
    trans = models.GASTransection.objects.filter(inDate__month=month).all()
    cal = models.GASTransection.objects.filter(inDate__month=month).aggregate(
        Sum('totalSale'), Sum('cashDeposited'), Avg('perQubicLiter'))
    if cal['totalSale__sum']:
        context = {
            'total': True,
            'SaleTotal': round(cal['totalSale__sum'], 3),
            'totalCash': round(cal['cashDeposited__sum'], 3),
            'AverageSale': round(cal['perQubicLiter__sum'], 3)
        }
    context = {
        'trans': trans,
        'month_name': month_name
    }

    return render(req, 'cngSales.html', context=context)


def CNGaddTransection(req):
    # today = datetime.today()
    # yesterday = datetime.strftime(today - timedelta(days=1), '%d-%m-%Y')
    yesterdayCMS = models.GASLastReading.objects.filter(
        id=1).values('quantity').all()
    lastCMS = yesterdayCMS[0]['quantity']

    if req.POST:
        inDate = req.POST['inDate']
        meterReading = Decimal(req.POST['meterReading'])
        totalGasSale = meterReading - Decimal(lastCMS)
        cashDeposited = Decimal(req.POST['cash'])
        percentage = round((cashDeposited/totalGasSale), 3)
        per = Decimal(percentage)
        print(percentage, type(per))
        models.GASTransection.objects.create(
            inDate=inDate, quantity=meterReading, totalSale=totalGasSale, cashDeposited=cashDeposited, perQubicLiter=per)
        models.GASLastReading.objects.filter(
            id=1).update(quantity=meterReading)
        return redirect(reverse('HishabNikash:hnCNGTransection'))
    return render(req, 'addCNGTransection.html')


def viewCNGMonthlyTransection(req):
    displayData = False
    No_Data = False
    context = {
        'displayData': displayData,
    }
    if req.POST:
        sDate = req.POST['sDate']
        eDate = req.POST['eDate']
        trans = models.GASTransection.objects.filter(
            inDate__range=[sDate, eDate]).order_by('inDate')
        if len(trans) == 0:
            No_Data = True
            context = {
                'displayData': displayData,
                'No_Data': No_Data,
                'trans': trans,
            }
        else:
            displayData = True
            cal = models.GASTransection.objects.filter(inDate__range=[sDate, eDate]).aggregate(
                Sum('totalSale'), Sum('cashDeposited'), Avg('perQubicLiter'))
            if cal['totalSale__sum']:
                context = {
                    'total': True,
                    'SaleTotal': round(cal['totalSale__sum'], 3),
                    'totalCash': round(cal['cashDeposited__sum'], 3),
                    'AverageSale': round(cal['perQubicLiter__avg'], 3),
                    'displayData': displayData,
                    'No_Data': No_Data,
                    'trans': trans,
                }

    return render(req, 'viewMonthCNG.html', context=context)
