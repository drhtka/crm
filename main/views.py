from django.shortcuts import render, redirect
# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic.base import View
from main.models import Users

class MainPageView(View):
    # page registration
    def get(self, request):
        return render(request, 'main/main.html')

class UsersSiteView(View):
    # registration users with site
    def post(self, request):
        role_id = request.POST.get('role')
        site_users = request.POST.get('username')
        site_email = request.POST.get('user_email')
        site_pass = request.POST.get('user_pass')
        seve_site = Users(username=site_users, user_email=site_email, user_pass=site_pass, role=role_id)
        seve_site.save()
        #return redirect('/main')
        return render(request, 'main/user.html')

"""        for site_users_s in site_users:
            test = site_users_s
            print('test')
            print(test)"""

