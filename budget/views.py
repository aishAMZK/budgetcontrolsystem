from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,ExpenseCreateForm
from django.contrib.auth import authenticate,login,logout
from .models import Expense
# Create your views here.
# registration
# login
# logout


def signin(request):
    if request.method=="POST":
        uname=request.POST.get("uname")
        pwrd=request.POST.get("password")
        #authenticate user with this username password
        #user model authenticate
        user=authenticate(username=uname,password=pwrd)
        if user is not None:
            login(request,user)
            return render(request,"budget/home.html")
        else:
            return render(request,"budget/login.html",{"message":"invalid credentials"})
    return render(request,"budget/login.html")

def registration(request):
    form=UserRegistrationForm()
    context={}
    context["form"]=form
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print("user created")
            return redirect("signin")
        else:
            context["form"]=form
    return render(request,"budget/registration.html",context)


def signout(request):
    logout(request)
    return redirect("signin")


def expense_create(request):
    form=ExpenseCreateForm(initial={'user':request.user})
    context={}
    context["form"]=form
    if request.method=="POST":
        form=ExpenseCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("addexpense")
    return render(request,"budget/addexpense.html",context)

def view_expenses(request):
    # form =DateSearchForm()
    context = {}
    expenses = Expense.objects.filter(user=request.user)
    # context['form'] = form
    context["expenses"] = expenses
    return render(request, 'budget/viewexpenses.html',context)

def edit_expense(request,id):
    expense=Expense.objects.get(id=id)
    form=ExpenseCreateForm(instance=expense)
    context={}
    context['form']=form
    if request.method=="POST":
        form=ExpenseCreateForm(request.POST,instance=expense)
        if form.is_valid():
            form.save()
            return redirect('viewexpenses')
        else:
            form=ExpenseCreateForm(request.POST,instance=expense)
            context['form']=form
            return render(request, 'budget/expenseedit.html', context)
    return render(request,'budget/expenseedit.html',context)

def delete_expense(request,id):
    expense=Expense.objects.get(id=id)
    expense.delete()
    return redirect("viewexpenses")
