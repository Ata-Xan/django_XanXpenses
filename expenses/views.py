from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from expenses.models import Category, Expense
from django.core.paginator import Paginator


# Create your views here.
# by doing this we don't let user's go back and forth with back bottom to the expenses page.
@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator,page_number)
    context={
        'expenses':expenses,
        'page_obj':page_obj
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values':request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)
    if request.method =='POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not description:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner= request.user, amount=amount, date=date, category=category, description = description)
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')
    return render(request, 'expenses/add_expense.html', context)

def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context={
        'expense':expense,
        'values':expense,
        'categories':categories
    }
    if request.method=='GET':

        return render(request, 'expenses/edit-expense.html', context)
    if request.method =='POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']
        if not description:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner_id = request.user
        expense.amount = amount
        expense.description = description
        expense.date = date
        expense.category = category

        expense.save()

        # Expense.objects.create(owner= request.user, amount=amount, date=date, category=category, description = description)
        messages.success(request, 'Expense Updated successfully')
        return redirect('expenses')

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')



