# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 19:18:39 2014

@author: Reed
"""
from django import forms
from django.forms.widgets import Select, HiddenInput

class CurrCapacityForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())

class CurrAffForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())

class CurrAttForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())
    
class CurrContForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())

class CurrDelForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())
    dropdown = forms.TextField(label='Default Continuity Rule:',widget=Select(choices=('Share','Do Not Share')))

class CurrUtForm(forms.Form):
    pass    
    
class CurrResForm(forms.Form):    
    pass
    
class ScenCapacityForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())

class ScenAffForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())

class ScenAttForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())
    
class ScenContForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())

class ScenDelForm(forms.Form):
    table = forms.TextField(widget=HiddenInput())
    dropdown = forms.TextField(label='Default Continuity Rule:',widget=Select(choices=('Share','Do Not Share')))
    
class ScenUtForm(forms.Form):
    pass
    
class ScenResForm(forms.Form):
    pass