from django import forms
from django.forms import ModelForm

from center.models import ChiefFunctionary
from main.models import UserProfile
from static_data.models import District


class CenterProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['address1', 'district', 'pincode', 'reg_no', 'reg_date', 'nature', 'website', 'mobile_no']

        def __init__(self, *args, **kwargs):
            district = kwargs.pop('district', '')
            super(CenterProfileForm, self).__init__(*args, **kwargs)
            self.fields['district'] = forms.ModelChoiceField(queryset=District.objects.get(pk=district))


class FunctionaryForm(ModelForm):
    class Meta:
        model = ChiefFunctionary
        exclude = ['center']

