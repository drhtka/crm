from django.shortcuts import render, redirect
# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic.base import View
from main.models import Users

class MainPageView(View):
    def get(self, request):
        return render(request, 'main/main.html')

class UsersSiteView(View):

    def post(self, request):
        print(31)
        #print(request.GET.get('role'))
        role_id = request.POST.get('role')
        site_users = request.POST.get('username')
        site_email = request.POST.get('user_email')
        site_pass = request.POST.get('user_pass')
        print(site_users, site_email, site_email)
        seve_site = Users(username=site_users, user_email=site_email, user_pass=site_pass, role=role_id)
        seve_site.save()
        print(seve_site)
        #return redirect('/main')
        return render(request, 'main/user.html')

"""        for site_users_s in site_users:
            test = site_users_s
            print('test')
            print(test)"""

