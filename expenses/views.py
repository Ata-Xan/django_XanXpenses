from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# by doing this we don't let user's go back and forth with back bottom to the expenses page.
@login_required(login_url='/authentication/login')
def index(request):
    return render(request, 'expenses/index.html')
def add_expense(request):
    return render(request, 'expenses/add_expense.html')