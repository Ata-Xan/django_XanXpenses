from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name="expenses"),
    path('add-expenses', views.add_expense, name="add-expenses"),
    path('edit-expense/<int:id>', views.edit_expense, name="edit-expense"),
    path('delete_expense/<int:id>', views.delete_expense, name="delete-expense"),
    path('search-expenses/', csrf_exempt(views.search_expenses), name="search-expenses"),


]
