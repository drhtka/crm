from django.contrib import admin
# -*- coding: utf-8 -*-
# Register your models here.
from main.models import CreatreTasks

class CreateTaskAdmin(admin.ModelAdmin):

    list_display = ('inputtitle', 'created')
    list_filter = ('id', 'created')

admin.site.register(CreatreTasks, CreateTaskAdmin)