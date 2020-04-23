import hashlib
from django.http import HttpResponse
from django.shortcuts import render, redirect
# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic.base import View, TemplateView
from main.models import Users, CreatreTasks, Roles

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
        lk_email = Users.objects.filter(user_email=user_lk).values_list('username', 'role', 'id')
        print(lk_email)
        #print(lk_email[0]['username'])
        #print(lk_email[0][0], lk_email[0][1])
        user_name = lk_email[0][0]
        user_role = lk_email[0][1]
        user_id = lk_email[0][2]
        print('user_id')
        print(user_id)
        data = [] # чтоб не вызывать ошибок для тех кто входит под номером роли
        layout = ''
        data = CreatreTasks.objects.filter(id_users=user_id).values_list('inputtitle', 'textarea')
        print('data')
        print(data)
        if user_role == 1:
            print('Администратор')
            layout = 'lk_admin.html'
        if user_role == 2:
            print('Бухгалтер')
            layout = 'lk_buh.html'
        if user_role == 3:
            print('Менеджер')
            layout = 'lk_manager.html'
        if user_role == 4:
            print('Оператор интернет')
            layout = 'lk_oper_inet.html'
        if user_role == 5:
            print(data)
            print('Оператор ктв')
            layout = 'lk_oper_ktv.html'
        # выбераем имя и id  для передачи в шаблон и создания задачи динамически
        task_list_users = Users.objects.values_list('username', 'id')

        return render(request, 'main/' + layout, context={'lk_email': user_name, 'user_role': user_role, 'task_list_users': task_list_users, 'data': data})

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

class LkTaskView(View):
    # запись в базу поставлененой задачи  id=request.POST.get('id_task'),
    def post(self, request):
        test_create = CreatreTasks(id_users=request.POST.get('role'), inputtitle=request.POST.get('title_task'), textarea=request.POST.get('desk_task'))
        test_create.save()
        print('test_create')
        print(test_create)
        return HttpResponse('Задача поставлена  <a href="http://127.0.0.1:8000/lk/">Личный кабинет</a>')

class RolesView(View):

    def get(self, request):
        roles_edit = Users.objects.all().values_list('username', 'user_email', 'id')
        #print(roles_edit)
        rolis_list = Roles.objects.values_list('id_roles', 'roles')
        #print('rolis_list')
        #print(rolis_list)
        return render(request, 'main/roles.html', {'roles_edit': roles_edit, 'rolis_list': rolis_list})

    def post(self, request):
        #print('user_hidddd')
        #print(request.POST.get('rolless'))
        id_up = request.POST.get('rolless')
        #print(request.POST.get('user_hid'))
        email_up = request.POST.get('user_hid')
        print('user_hid')
        update_user = Users.objects.filter(user_email=email_up).update(role=id_up)
        print(update_user)
        return redirect('/roles/')

class CommentView(View):
    def post(self, request):
        print(request.POST.get('comment'))
        return redirect('/lk/')


"""class RolesRosView(View):
    template_name = 'main/roles.html'
    print('RolessView')
    def get(self, request):
        print('user_hidddd')
        print(request.GET.get('rolless'))
        print(request.GET.get('user_hid'))
        print('user_hid')
        return HttpResponse('role')"""
    
"""  class LkView(View):
    def get(self, request):
        return render(request, 'main/lk.html')

     for site_users_s in site_users:
            test = site_users_s
            print('test')
            print(test)"""
