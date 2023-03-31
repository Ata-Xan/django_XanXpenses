from django.conf import settings
from django.shortcuts import render
from .models import UserPreferences
from django.contrib import messages
import json
# for debugging
import pdb
from pathlib import Path
import os


# Create your views here.
def index(request):
    file_path = os.path.join(settings.BASE_DIR, 'userpreferences/static/currencies.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
    context = {'currencies': data}
    exists = UserPreferences.objects.filter(user=request.user).exists()
    user_preferences = None

    if request.method == 'GET':
        context = {'currencies': data, 'user_preferences':user_preferences}
        return render(request, 'preferences/index.html', context)
    if exists:
        user_preferences = UserPreferences.objects.get(user=request.user)

        # print(request.POST[''])
    currency = request.POST['currency']
        # pdb.set_trace()
    if exists:
        user_preferences.currency = currency
        user_preferences.save()
        messages.success(request, "Changes saved.")
        print("exits")
    else:
        UserPreferences.objects.create(user=request.user, currency=currency)
        messages.success(request, "Your preference saved")
        print("not exists")
        # pdb.set_trace()
    context = {'currencies': data, 'user_preferences': user_preferences}
    return render(request, 'preferences/index.html', context)
