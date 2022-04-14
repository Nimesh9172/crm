from pathlib import Path
import re
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Customer,ListUpload,ExcelFormat
from .forms import CustomerForm,CreateUserform,ListUploadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count,Sum,Case,When
from django.conf import settings
import pandas as pd

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request,'index.html')

def loginuser(request):
    if request.user.is_authenticated and request.user.is_user:
        return redirect('customerform')
    elif request.user.is_authenticated and request.user.is_admin:
        return redirect('adminpage')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request,username=username,password=password)
            if user is not None and user.is_user:
                login(request,user)
                request.session['userid'] = request.user.id
                return redirect('customerform')
            elif user is not None and user.is_admin:
                request.session['userid'] = request.user.id 
                login(request,user)
                return redirect('adminpage')
        return render(request,'login.html')

def registeruser(request):
    if request.user.is_authenticated:
        return redirect('customerform')
    else:
        if request.method == 'POST':
            form = CreateUserform(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request,'Successfully created account')
                return redirect('login')

        form = CreateUserform
        return render(request,'register.html',{'form':form})

@login_required(login_url='login')
def logoutuser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def createCustomer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    form = CustomerForm()
    context = {'form':form}
    return render(request,'customerform.html',context)

@login_required(login_url='login')
def updatecustomer(request,pk):
    get = Customer.objects.get(id=pk)
    form = CustomerForm(instance=get)
    if request.method == 'POST':
        form = CustomerForm(request.POST,instance=get)
        if form.is_valid():
            form.save()
            return redirect('adminpage')
    return render(request,'customerform.html',{'form':form})

@login_required(login_url='login')
def deletecustomer(request,pk):
    obj = Customer.objects.get(id=pk)
    obj.delete()
    return redirect('adminpage')    


@login_required(login_url='login')
def userpage(request):
    if request.user.is_user:
        f = request.session.get('userid')
        query = Customer.objects.filter(created_by=f)
        if request.method == 'POST':
            fil = request.POST['fil']
            if fil == 'contact':
                query = Customer.objects.filter(created_by=f,disposition='contact')
            elif fil == 'all':
                query = Customer.objects.filter(created_by=f)
            elif fil == 'new':
                query = Customer.objects.filter(created_by=f,disposition='')
            elif fil == 'no-contact':
                query = Customer.objects.filter(created_by=f,disposition='No-contact')
                
        context = {'read':query}
        return render(request,'userpage.html',context)
    else:
        return redirect('adminpage')      


@login_required(login_url='login')
def adminpage(request):
    if request.user.is_admin:
        read = Customer.objects.all()   
        if request.method == 'POST':

            if 'fil' in request.POST:
                fil = request.POST['fil']
                if fil != "":
                    total_contact = Customer.objects.all().values('created_by').annotate(Count('id',distinct=True)).annotate(contact=Sum(Case(When( disposition = 'contact',then=1),default=0
                        ))).annotate(nocontact=Sum(Case(
                        When( disposition = 'No-contact',then=1),default=0
                        )))
        
                    read = Customer.objects.filter(created_by=fil)
                    context = {'data':read,'total_contact':total_contact}  
                    return render(request,'adminpage.html',context)
                

            if 'exp_excel' in request.POST:
                read = []
                exp = request.POST['exp_excel']
                if exp == "all":
                    read = Customer.objects.all()   
                else:
                    read = Customer.objects.filter(created_by=exp)
                   
                data = []
                for i in read:
                    data.append({
                        "name":i.name,
                        'phone':i.phone,
                        'productid':i.productid,
                        'price':i.price,
                        'address':i.address,
                        'city':i.city,
                        'disposition':i.disposition,
                        'sub_disposition':i.sub_disposition,
                        'remarks':i.remarks,
                        'created_by':i.created_by
                    })
                path = f'{settings.BASE_DIR}\\media\\report.xlsx'
                print(path)
                pd.DataFrame(data).to_excel(path)
                print(data)       

        total_contact = Customer.objects.all().values('created_by').annotate(Count('id',distinct=True)).annotate(contact=Sum(Case(When(disposition = 'contact',then=1),default=0
                    ))).annotate(nocontact=Sum(Case(
                    When(disposition = 'No-contact',then=1),default=0
                    )))
        context = {'data':read,'total_contact':total_contact}  
        return render(request,'adminpage.html',context)
    else:
        return redirect('customerform')

@login_required(login_url='login')
def dataupload(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            listname = request.POST['listname']
            listid = request.POST['listid']
            file = request.FILES['listfile']
            form = ListUpload(listid=listid,listname=listname,files=file)
            form.save()
            excel_file_path = ListUpload.objects.filter(listid=listid)
            for i in excel_file_path:   
                excel_file = i.files.url
            path = f'{settings.BASE_DIR}{excel_file}'
            print(path)
            df = pd.read_excel(path)
            for i in  (df.values.tolist()):
                obj=Customer.objects.create(name=i[0],phone=i[1],productid=i[2],price=i[3],address=i[4],city=i[5],disposition='',sub_disposition='',remarks="",created_by=i[6])
                obj.save()
            return redirect('dataupload')
        
        form1 = ExcelFormat.objects.all()
        form = ListUploadForm
        read = ListUpload.objects.all()
        context = {'form':form,'read':read,'form1':form1}
        return render(request,'dataupload.html',context)
    return redirect('customerform')

@login_required(login_url='login')
def formatUpload(request):
    if request.user.is_authenticated and request.user.is_admin:
        if request.method == 'POST':
            file = request.FILES['fil']
            form = ExcelFormat.objects.create(dataformat=file)
            form.save()
            return redirect('adminpage')
        else:
            return render(request,'excelformat.html')
    else:
        return redirect('login')

# def readUpload(request):

