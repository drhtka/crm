import hashlib
import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
# -*- coding: utf-8 -*-
# Create your views here.
from django.views.generic.base import View, TemplateView
from main.models import Users, CreatreTasks, Roles, DayTask, Comments
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


        all_task = '' # инициализировали переменную для избежния ошибок, чтоб не было конфликтов
        all_task = CreatreTasks.objects.values_list('id', 'id_users', 'inputtitle',
                                                    'textarea', 'created', 'answear',
                                                    'status_task', 'answear_comment',
                                                    'data_dedline', 'time_task',
                                                    'upload_file_name')
        final_array = []
        #i = 0
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
            #new_tsk_tmp_array = final_array[0][7].split(',')
            #print(new_tsk_tmp_array)
            #for new_tsk_tmp_array_s in new_tsk_tmp_array:
                #print('new_tsk_tmp_array_s')
                #print(new_tsk_tmp_array_s)

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
            #print(data)
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
        all_array = []
        for users_distinct_task_s in users_distinct_task:
            u_distr = users_distinct_task_s['id_users']# номера пользователей которые выполнили задачи
            user_time_task = CreatreTasks.objects.filter(status_task=2).filter(id_users=u_distr).values_list('time_task')# все часы котрые потратил польз на выполнение задачи
            time_task_us = 0
            arr_time_user = []
            tmp_time = 0
            tmp_username = ''

            for user_time_task_s in user_time_task:
                time_task_us = str(u_distr) + ',' + user_time_task_s[0]

                id_user_count = time_task_us.split(',')[0]
                time_task_all = time_task_us.split(',')[1]
                id_user_count = Users.objects.filter(id=id_user_count).values('username')
                #print('id_user_count')
                #print(id_user_count)
                id_user_count_name = id_user_count[0]['username']
                tmp_object = [id_user_count_name, time_task_all]
                arr_time_user.append(tmp_object)
                #print('tmp_username')
                #print(tmp_username)
                time_task_all = time_task_all.split(':')
                time_task_h = time_task_all[0]
                time_task_m = int(time_task_all[1]) / 60
                time_task_all_all = int(time_task_h) + time_task_m
                #print('time_task_all_all')
                #print(time_task_all_all)
                #sum_time_users = [id_user_count_name, (time_task_all_all)]
                #print('sum_time_users ')
                #print(sum_time_users )
            my_sum = ''
            tmp_ar2 = []
            tmp_ar3 = [id_user_count_name, '']
            #print('tmp_ar3')
            #print(tmp_ar3)
            for arr_time_user_s in arr_time_user:
                my_sum = my_sum + ',' + arr_time_user_s[1]
                tmp_ar3[1]=my_sum
            #print('tmp_ar3')
            #print(tmp_ar3)
            all_array.append(tmp_ar3)
        #print('all_array')
        #print(all_array)
        all_array_end = []
        for all_array_s in all_array:
            split_time = all_array_s[1].split(',')
            hours = 0
            minuts = 0
            our_time = 0
            all_array_time = [all_array_s[0], '', '']
            for split_time_s in split_time:
                if split_time_s != '': #36 min 28 urok
                    split_two = split_time_s.split(':')
                    hours = int(hours) + int(split_two[0])
                    minuts = int(minuts) + round(int(split_two[1]) / 60)
                    our_time = hours + minuts
                    all_array_time[1] = our_time
                    zp_user = Users.objects.filter(username=all_array_time[0]).values_list('zp')
                    all_zp = our_time * int(zp_user[0][0])
                    all_array_time[2] = all_zp
            all_array_end.append(all_array_time)
            #print('all_array_end')
            #print(all_array_end)

        return render(request, 'main/' + layout, context={'lk_email': user_name,
                                                          'user_role': user_role,
                                                          'task_list_users': task_list_users,
                                                          'data': data,
                                                          'all_task': all_task,
                                                          'final_array': final_array,
                                                          'general_arr_task': general_arr_task,
                                                          'all_array_end': all_array_end,

                                                          #'zp_user': zp_user, 'new_tsk_tmp_array_s': new_tsk_tmp_array_s,

                                                          })
    #выход
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
        #print('post_time')
        #print(time_tisk)
        filter_coment = CreatreTasks.objects.filter(id=request.POST.get('task_id')).values('answear')
        #print('filter_coment')
        #print(filter_coment)
        temp_com = (filter_coment[0]['answear'])
        temp_com = temp_com + ',' + request.POST.get('comment')
        #print(temp_com)
        com_create = CreatreTasks.objects.filter(id=request.POST.get('task_id'))\
                                    .update(answear=temp_com, time_task=time_tisk)
        #print('com_create')
        #print(com_create)
        filter_coment_new = Comments.objects.filter(id_task=request.POST.get('task_id')).values('comment')
        temp_com_new = (filter_coment_new[0]['comment'])
        temp_com_new = temp_com_new + ',' + request.POST.get('comment')
        new_comment = Comments.objects.filter(id_task=request.POST.get('task_id')).update(comment=temp_com_new)
        #print('new_comment')
        #print(new_comment)



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
                    #print('all_task7')
                    #print(all_task7)
                    tmp_list = [all_task_s[0], all_task_s[1], all_task_s[2], all_task_s[3],
                                all_task_s[4], all_task_s[5], all_task_s[6], all_task7, username_lk, all_task_s[8]]
                    final_array.append(tmp_list)
                #print('final_array')
                #print(final_array)
        return render(request, 'main/taskcard.html', {'id_task': id_task, 'final_array': final_array})

    def post(self, request):
        #print(request.POST.get('id_state_task'), request.POST.get('stat_task'))
        #print('id_state_task')
        CreatreTasks.objects.filter(id=request.POST.get('id_state_task')).update(status_task=request.POST.get('stat_task'))
        referer = self.request.META.get('HTTP_REFERER')
        return redirect(referer)



class AnswerCommentView(View):
    #answer_comment ответ на комментарий
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

        filter_coment_new = Comments.objects.filter(id_task=id_task).values('answear_comment')
        temp_com_new = (filter_coment_new[0]['answear_comment'])
        temp_com_new = temp_com_new + ',' + post_comment
        new_comment = Comments.objects.filter(id_task=id_task).update(answear_comment=temp_com_new)
        print('new_comment')
        print(new_comment)

        referer = self.request.META.get('HTTP_REFERER')# вернуться на предыдущую страницу на тот же урл
        return redirect(referer)

class AjaxCalView(View):
    # задачи в календаре
    def get(self, request):
        ajax_data = request.GET.get('date')
        split_ajax_data = ajax_data.split('-')
        ajax_data_data = split_ajax_data[2]
        print('ajax_data')
        print(ajax_data_data)
        ajax_user = request.session['my_list']
        #print(ajax_data, ajax_user, request.session)
        # 26.05.20 # убрал фильтрацию  filter(user_email_calc=ajax_user).
        calc_task_user = DayTask.objects.filter(user_email_calc=ajax_user).filter(day_task__contains=ajax_data_data).values_list('day_task', 'tascs')
        print('calc_task_user')
        print(calc_task_user)
        arr_name_tasks = ''
        for calc_task_user_s in calc_task_user:
            get_task_name = CreatreTasks.objects.filter(id=calc_task_user_s[1]).values('inputtitle')
            print('get_task_name')
            print(get_task_name[0]['inputtitle'])
            if(arr_name_tasks==''):
                arr_name_tasks = get_task_name[0]['inputtitle']
            else:
                arr_name_tasks = arr_name_tasks + ';' + get_task_name[0]['inputtitle']
        print('arr_name_tasks')
        print(arr_name_tasks)

        all_task_day = DayTask.objects.filter(day_task=ajax_data_data).values_list('tascs', 'iduser', 'user_email_calc')
        print('all_task_day')
        print(all_task_day)
        main_arr = []
        for all_task_day_s in all_task_day:
            #print('all_task_day_s[0]')
            #print(all_task_day_s[0])
            all_task_users_day = CreatreTasks.objects.filter(id=all_task_day_s[0]).values_list('inputtitle')
            print('all_task_users_day')
            print(all_task_users_day)
            main_arr.append([all_task_day_s[2], all_task_users_day[0][0]])
        print('main_arr')
        print(main_arr)

        return render(request, 'main/lk_ajax.html', context={'arr_name_tasks': arr_name_tasks, 'main_arr': main_arr})