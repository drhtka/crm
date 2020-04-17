import hashlib
from django.http import HttpResponse
from django.shortcuts import render, redirect
# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic.base import View, TemplateView
from main.models import Users

class MainPageView(View):
    # page registration
    def get(self, request):
        return render(request, 'main/main.html')

    def post(self, request):
        print('post')

class UsersSiteView(View):
    # registration users with site

    def post(self, request):
        #hash

        #mystring = input('Enter String to hash: ')
        #hash_object = hashlib.md5(mystring.encode())
        #print(hash_object.hexdigest())

        role_id = request.POST.get('role')
        print(role_id)
        site_users = request.POST.get('username')
        print(site_users)
        site_email = request.POST.get('user_email')

        hashed_password = hashlib.md5(request.POST.get('user_pass').encode())
        final_ph = hashed_password.hexdigest()
        seve_site = Users(username=site_users, user_email=site_email, user_pass=final_ph, role=role_id)# заносим в базу

        seve_site.save()
        #return redirect('/main')
        return render(request, 'main/user.html')

class LkView(View):
    # вывели имя юзера в лк
    def get(self, request):
        user_lk = (request.session['my_list'])
        print(user_lk)
        lk_email = Users.objects.filter(user_email=user_lk).values_list('username', 'role')
        print(lk_email)
        #print(lk_email[0]['username'])
        print(lk_email[0][0], lk_email[0][1])
        user_name = lk_email[0][0]
        user_role = lk_email[0][1]
        layout = ''
        if user_role == 1:
            print('Администратор')
            layout = 'lk_admin.html'
        if user_role == 2:
            print('Бухгалтер')
            layout = 'lk_buh.html'
        if user_role == 3:
            print('Аmenag')
            layout = 'lk_buh.html'
        if user_role == 4:
            print('oper')
            layout = 'lk_buh.html'
        if user_role == 5:
            print('oper2')
            layout = 'lk_buh.html'

        return render(request, 'main/' + layout, context={'lk_email': user_name, 'user_role': user_role})

    def post(self, request):
        request.session['my_list'] = []
        return redirect('/')

class LogginView(TemplateView):
    #authorization loggin
    template_name = 'main/outh.html'
    def post(self, request):
        hashed_password = hashlib.md5(request.POST.get('pass').encode())
        final_ph = hashed_password.hexdigest()
        find_user = Users.objects.filter(user_email=request.POST.get('loggin'), user_pass=final_ph).values('user_email')
        #request.session['my_list'] = []
        if len(find_user) > 0:
            #request.session.get('find_us')
            request.session['my_list'] = request.POST.get('loggin')# записали емаил пользователя в сессию
            return redirect('/lk/')
        else:
            return HttpResponse('Данные не верны <a href="http://127.0.0.1:8000/loggin/">Вернуться назад</a>')

        #request.session.modified = True

        return render(request, 'main/outh.html')

class RolesView(View):
    pass
"""  class LkView(View):
    def get(self, request):
        return render(request, 'main/lk.html')

     for site_users_s in site_users:
            test = site_users_s
            print('test')
            print(test)"""
