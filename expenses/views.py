from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from expenses.models import Category, Expense
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from datetime import datetime
import json
from django.http import JsonResponse
from django.db.models import Q
from .models import Expense
from django.http import JsonResponse


# def search_expenses(request):
#     query = request.GET.get('q')
#     if not query:
#         expenses = Expense.objects.none()
#     else:
#         expenses = Expense.objects.filter(
#             Q(amount__icontains=query) |
#             Q(category__icontains=query) |
#             Q(description__icontains=query) |
#             Q(date__icontains=query)
#         )
#     paginator = Paginator(expenses, 3)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, 'expenses/search_expenses.html', {'page_obj': page_obj})


def search_expenses(request):
    query = request.POST.get('search')
    if query:
        expenses = Expense.objects.filter(
            Q(amount__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query) |
            Q(date__icontains=query)
        )
    else:
        expenses = Expense.objects.all()
        # Set the number of items per page
    per_page = 5
    # Create a Paginator object
    paginator = Paginator(expenses, per_page)
    # Get the current page number from the request
    page_number = request.GET.get('page')
    # Get the Page object for the current page
    page_obj = paginator.get_page(page_number)

    expense_list = []
    for expense in page_obj:
        date_obj = datetime.strptime(str(expense.date), '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')
        expense_list.append({
            'amount': expense.amount,
            'category': expense.category,
            'description': expense.description,
            'date': formatted_date,
            'id':expense.id

        })
    response_data = {
        'page_number': page_obj.number,
        'page_range': list(paginator.page_range),
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'has_next': page_obj.has_next(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'results': expense_list,
    }
    return JsonResponse(response_data, safe=False)


# def search_expenses(request):
#     if request.method == 'POST':
#         search_str = json.loads(request.body).get('searchText')
#
#         expenses = Expense.objects.filter(amount__istartswith=search_str, owner=request.user) | Expense.objects.filter(
#             date__istartswith=search_str, owner=request.user) | Expense.objects.filter(
#             description__icontains=search_str, owner=request.user) | Expense.objects.filter(
#             category__icontains=search_str, owner=request.user)
#
#         data = expenses.values()
#         return JsonResponse(list(data), safe=False)


# Create your views here.


# by doing this we don't let user's go back and forth with back bottom to the expenses page.
@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    user_preference = UserPreferences.objects.get(user_id=request.user)
    # print("user_pref"+str(user_preference))
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    # context = {
    #     'expenses': expenses,
    #     'page_obj': page_obj
    # }
    context = {
        'page_obj': page_obj,
        'page_number': page_obj.number,
        'page_range': list(paginator.page_range),
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'has_next': page_obj.has_next(),
        'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
        'expenses': expenses,
        'user_pref': user_preference
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)
    if request.method == 'POST':
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

        Expense.objects.create(owner=request.user, amount=amount, date=date, category=category, description=description)
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')
    return render(request, 'expenses/add_expense.html', context)


def edit_expense(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
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
