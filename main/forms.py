# -*- coding: utf-8 -*-
from django import forms
#from datetimepicker.helpers import js_loader_url
#from datetimepicker.widgets import DateTimePicker

class DateForm(forms.Form):
    date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

"""
class SampleForm(forms.Form):
    datetimepicker_without_script_tag = forms.DateTimeField(
        widget=DateTimePicker(script_tag=False),
    )

@property
def media(self):
   form_media = forms.Media(js=[
       js_loader_url(
           fields=self.fields,
           input_ids=['id_datetimepicker_without_script_tag'],
       ),
   ])
   return super(SampleForm, self).media + form_media

class SampleForm(forms.Form):

    datetimepicker_without_script_tag = forms.DateTimeField(
    	widget=DateTimePicker(script_tag=False),
    )"""