from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from catalog.models import BookInstance


class RenewBookForm(forms.Form):
 renewal_date = forms.DateField(help_text="Enter a data between now and 4 weeks( default 3)")

 def clean_renewal_date(self):
  date = self.cleaned_data['renewal_date']
  if date < datetime.date.today():
   raise ValidationError(_('invalid date - renewal in past'))

  if date > datetime.date.today() + datetime.timedelta(weeks=4):
   raise ValidationError(_('invalid date - renewal more then 4 weeks ahead.'))

  return date


class RenewBookModelForm(ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('renewal date')}
        help_texts = {'due_back': _('Enter a date between now and 4 weeks (default 3).')} 

    def clean_renewal_date(self):
     date = self.cleaned_data['due_back']
     if date < datetime.date.today():
      raise ValidationError(_('invalid date - renewal in past'))
     if date > datetime.date.today() + datetime.timedelta(weeks=4):
      raise ValidationError(_('invalid date - renewal more then 4 weeks ahead.'))
     return date

