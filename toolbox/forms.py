# -*- coding: utf-8 -*-
from pagedown.widgets import AdminPagedownWidget
from django import forms
from toolbox.models import CommonFields, License

class LicenseForm(forms.ModelForm):
    license_md = forms.CharField(widget=AdminPagedownWidget())
    
    class Meta:
        model = License

class CommonFieldsForm(forms.ModelForm):
    content_md = forms.CharField(widget=AdminPagedownWidget(),label="Beschrijving")
    intro_md   = forms.CharField(widget=AdminPagedownWidget(),label="Intro")            
    
    class Meta:
        model = CommonFields

