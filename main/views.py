import hashlib
import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic.base import View, TemplateView
from main.models import Users, CreatreTasks, Roles
from .forms import UploadFileForm
#from somewhere import where #handle_uploaded_file


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
        return render(request, 'main/user.html')

class LkView(View):
    # вывели имя юзера в лк
    def get(self, request):
        from datetime import datetime
        user_lk = (request.session['my_list'])
        #print('user_lk')
        #print(user_lk)
        lk_email = Users.objects.filter(user_email=user_lk).values_list('username',
                                                                        'role', 'id')
        #print(lk_email)
        #print(lk_email[0]['username'])
        #print(lk_email[0][0], lk_email[0][1])
        user_name = lk_email[0][0]
        user_role = lk_email[0][1]
        user_id = lk_email[0][2]
        #print('user_id')
        #print(user_id)


        data = [] # чтоб не вызывать ошибок для тех кто входит под номером роли
        layout = ''
        data = CreatreTasks.objects.filter(id_users=user_id).values_list('inputtitle',
                                                                         'textarea',
                                                                         'id_users',
                                                                         'id',
                                                                         'status_task',
                                                                         'answear',
                                                                         'data_dedline',
                                                                         'time_task',
                                                                         'answear_comment',
                                                                         'upload_file_name')
        data_task = CreatreTasks.objects.filter(id_users=user_id).values_list('answear')
        general_arr_task = []
        for data_task_s in data_task:
            #print('data_task_s')
            tmp_data_task = list(data_task_s)
            #print(tmp_data_task[0].split(','))
            spechial_ar_task = []
            for data_task_s_s in data_task_s[0].split(','):
                spechial_ar_task.append(data_task_s_s)
            general_arr_task.append(spechial_ar_task)
        #print(general_arr_task)
        #print('general_arr_task')

        #comment_task = []
        #my_data = 'data'
        #for data05 in data[0][5].split(','):
            # коменты не в строчку а в столбик
            #print('data05')
            #print(data05)
            #comment_task.append(data05)
        #print('comment_task')
        #print(comment_task)

        all_task = '' # инициализировали переменную для избежния ошибок, чтоб не было конфликтов
        all_task = CreatreTasks.objects.values_list('id', 'id_users', 'inputtitle',
                                                    'textarea', 'created', 'answear',
                                                    'status_task', 'answear_comment',
                                                    'data_dedline', 'time_task',
                                                    'upload_file_name')
        final_array = []
        i = 0
        for all_task_s in all_task:
            #print('data_dedline')
            #print(all_task_s[8])
            tmp_dedline = all_task_s[8].split('-')
            #print('tmp_dedline')
            #print(tmp_dedline)
            year = tmp_dedline[0]
            month = tmp_dedline[1]
            day = tmp_dedline[2]

            if (month[0] == '0'):
                month = month[1]

            if (day[0] == '0'):
                day = day[1]
            #print(year, month, day)
            now = datetime.now()

            deadline = datetime(2020, int(month), int(day))
            #print(now)
            #print(deadline)
            #print('deadline')
            #color_task = 'green'
            if now > deadline:
                #print("Срок сдачи проекта прошел")
                color_task = 'red'
            else:
                period = deadline - now
                #print(period.days)
                if period.days == 0:
                    #print("Срок сдачи проекта сегодня")
                    color_task = 'blue'
                else:
                    #print("Осталось {} дней".format(period.days))
                    color_task = 'green'
            #print('all_task_s[9]')
            #print(all_task_s[9])
            user_id_name = Users.objects.filter(id=all_task_s[1]).values('username')  # приравнивем айди к пользователю
            username_lk = user_id_name[0]['username']
            #print(general_arr_task[i])
            #print('general_arr_task')
            tmp_list = [all_task_s[0], all_task_s[1], all_task_s[2], all_task_s[3], all_task_s[4], all_task_s[5],
                        all_task_s[6], all_task_s[7], username_lk, all_task_s[8], color_task, all_task_s[9], all_task_s[10]] # здесь соединяем две таблицы
            final_array.append(tmp_list)
            #i = i + 1
            #print('final_array')
            #print(final_array[0][7])
        if user_role == 1:
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

        # выбираем имя и id  для передачи в шаблон и создания задачи динамически
        task_list_users = Users.objects.values_list('username', 'id')
        # выбираем для подсчета времени затраченную на задачу
        users_distinct_task = CreatreTasks.objects.filter(status_task=2).values('id_users').order_by('id_users').distinct('id_users')
        #print('users_distinct_task')
        #print(users_distinct_task)
        sum_time_users = []
        sum_time_users2 = []

        for users_distinct_task_s in users_distinct_task:
            u_distr = users_distinct_task_s['id_users']# номера пользователей которые выполнили задачи
            user_time_task = CreatreTasks.objects.filter(status_task=2).filter(id_users=u_distr).values_list('time_task')# все часы котрые потратил польз на выполнение задачи
            time_task_us = 0
            for user_time_task_s in user_time_task:
                time_task_us = str(u_distr) + ',' + user_time_task_s[0]
                #print('time_task_us')
                id_user_count = time_task_us.split(',')[0]
                time_task_all = time_task_us.split(',')[1]
                #print(sum_time_users, sum_time_users2)
                id_user_count = Users.objects.filter(id=id_user_count).values('username')
                #print('id_user_count')
                #print(id_user_count)
                id_user_count_name = id_user_count[0]['username']
                sum_time_users = [id_user_count_name, time_task_all]
                print('sum_time_users')
                print(sum_time_users)





        return render(request, 'main/' + layout, context={'lk_email': user_name,
                                                          'user_role': user_role,
                                                          'task_list_users': task_list_users,
                                                          'data': data,
                                                          'all_task': all_task,
                                                          'final_array': final_array,
                                                          'general_arr_task': general_arr_task,
                                                          'i': i,
                                                          })

    def post(self, request):
        request.session['my_list'] = []
        return redirect('/')

class LogginView(TemplateView):
    #authorization loggin
    template_name = 'main/outh.html'
    def post(self, request):
        hashed_password = hashlib.md5(request.POST.get('pass').encode())
        final_ph = hashed_password.hexdigest()
        find_user = Users.objects.filter(user_email=request.POST.get('loggin'),
                                         user_pass=final_ph).values('user_email')
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

    def get(self, request):
    # статус задачи stat_task
        CreatreTasks.objects.filter(id=request.GET.get('task_idd')).update(status_task=request.GET.get('stat_task'))
        # print_stat =
        #print('print_stat')
        #print(print_stat)
        #print(request.GET.get('task_idd'), request.GET.get('stat_task'))
        return redirect('/lk/')

    # запись в базу поставлененой задачи  id=request.POST.get('id_task'),
    def post(self, request):
        print(request.POST.get('input_file'))
        # upload file
        myfile = request.FILES['input_file']
        myfile_split = str(myfile).split('.') #отсекаем все что по точки например .png

        if myfile_split[1] != 'txt':
            return HttpResponse('Формат файла не txt <a href="http://127.0.0.1:8000/lk/">Личный кабинет</a>')
        else:
            #если .txt тогда загрузить
            #print(myfile_split)
            #print(myfile_split[1])
            last_id_task = CreatreTasks.objects.latest('id').id + 1  # вывели последний айди

            fs = FileSystemStorage()
            filename = fs.save(str(last_id_task)+'.txt', myfile)
            uploaded_file_url = fs.url(filename)
            #print('myfile')
            #print(myfile)
            #print(uploaded_file_url)

            #print(last_id_task.id+1)


            test_create = CreatreTasks(id_users=request.POST.get('role'),
                                       inputtitle=request.POST.get('title_task'),
                                       textarea=request.POST.get('desk_task'),
                                       data_dedline=request.POST.get('task_date'),
                                       status_task=4,
                                       upload_file_name=str(last_id_task)+'.txt')
            test_create.save()
            #print('test_create')
            #print(test_create)
            return HttpResponse('Задача поставлена  <a href="http://127.0.0.1:8000/lk/">Личный кабинет</a>')

class RolesView(View):
    #смена ролей на шаблоне из выпадающего списка
    def get(self, request):
        roles_edit = Users.objects.all().values_list('username', 'user_email', 'id')
        #print(roles_edit)
        rolis_list = Roles.objects.values_list('id_roles', 'roles')
        #print('rolis_list')
        #print(rolis_list)
        return render(request, 'main/roles.html', {'roles_edit': roles_edit,
                                                   'rolis_list': rolis_list})

    def post(self, request):
        #print('user_hidddd')
        #print(request.POST.get('rolless'))
        id_up = request.POST.get('rolless')
        #print(request.POST.get('user_hid'))
        email_up = request.POST.get('user_hid')
        #print('user_hid')
        update_user = Users.objects.filter(user_email=email_up).update(role=id_up)
        #print(update_user)
        return redirect('/roles/')

class CommentView(View):
    # отправка комента в базу
    def post(self, request):
        #print('mayak')
        #print(request.POST.get('comment'))
        #print(request.POST.get('user_id'))
        #print(request.POST.get('task_id'))
        time_tisk = request.POST.get('time_tisk')
        print('post_time')
        print(time_tisk)
        filter_coment = CreatreTasks.objects.filter(id=request.POST.get('task_id')).values('answear')
        print('filter_coment')
        temp_com = (filter_coment[0]['answear'])
        temp_com = temp_com + ',' + request.POST.get('comment')
        print(temp_com)
        com_create = CreatreTasks.objects.filter(id=request.POST.get('task_id'))\
                                    .update(answear=temp_com, time_task=time_tisk)
        print('com_create')
        print(com_create)
        #com_create.save()
        return redirect('/lk/')

class TasskCardView(View):
    # ловим айдишник задачи и выводим все данные о ней
    def get(self, request):
        id_task = CreatreTasks.objects.filter(id=request.GET.get('task')).values_list('id', 'id_users', 'inputtitle', 'textarea', 'created',  'answear', 'status_task', 'answear_comment', 'time_task')
       # print(id_task)
        for id_task_s in id_task:
            #print('id_task_s')
            #print(id_task_s[1])
            final_array = []
            all_task7 = []
            for all_task_s in id_task:
                #print(all_task_s[1])
                user_id_name = Users.objects.filter(id=all_task_s[1]).values('username') #приравнивем айди задачи к пользователю
                username_lk = user_id_name[0]['username']
                #x = all_task_s[7]
                #print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                #print(x)

                for all_task7 in all_task_s[7].split(','):
                    #  выводим сколько ушло времени в шаблон
                #print('\n '.join(map(str, x)))
                    print('all_task7')
                    print(all_task7)
                    tmp_list = [all_task_s[0], all_task_s[1], all_task_s[2], all_task_s[3],
                                all_task_s[4], all_task_s[5], all_task_s[6], all_task7, username_lk, all_task_s[8]]
                    final_array.append(tmp_list)
                #print('final_array')
                #print(final_array)
        return render(request, 'main/taskcard.html', {'id_task': id_task, 'final_array': final_array})

    def post(self, request):
        print(request.POST.get('id_state_task'), request.POST.get('stat_task'))
        print('id_state_task')
        CreatreTasks.objects.filter(id=request.POST.get('id_state_task')).update(status_task=request.POST.get('stat_task'))
        referer = self.request.META.get('HTTP_REFERER')
        return redirect(referer)


#answer_comment
class AnswerCommentView(View):
    #print('answer')
    def post(self, request):
        post_comment = request.POST.get('comment')
        #print('post_comment')
        #print(post_comment)

        id_task = request.POST.get('task_idd')
        filter_coment = CreatreTasks.objects.filter(id=id_task).values('answear_comment')
        temp_comment = filter_coment[0]['answear_comment']
        temp_comment = temp_comment + ',' + post_comment
        update_coment = CreatreTasks.objects.filter(id=id_task).update(answear_comment=temp_comment)
        #print(update_coment)
        #print('update_coment')
        referer = self.request.META.get('HTTP_REFERER')#  вернуться на предыдущую страницу на тот жу урл
        return redirect(referer)

"""        now = datetime.now()
        deadline = datetime(2020, 5, 3)
        print(now)
        print(deadline)
        color_task = 'green'
        if now > deadline:
            print("Срок сдачи проекта прошел")
            color_task = 'brown'
        else:
            period = deadline - now
            print(period.days)
            if period.days == 0:
                print("Срок сдачи проекта сегодня")
                color_task = 'red'
            else:
                print("Осталось {} дней".format(period.days))
                color_task = 'green'""" # вырезал с 151 сстроки перед return