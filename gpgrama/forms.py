from typing import Container
from django import forms
from django.contrib.postgres import fields
from .models import Candidate
from .models import Admin
from .models import HiringManager
from .models import HR
from django.core.validators import RegexValidator


class AdminCreate(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))
    class Meta:
        model = Admin
        fields = ('password','image')

class CandidateCreate(forms.ModelForm):

    STATUS_CHOICES = (
        ("0", "Lead"),
		("1", "Active"),
		("2", "On-hold"),
		("3", "Not interested")
    )

    PIPELINE_STATUS_CHOICES = ( 
        ("0", "For future revision"), 
        ("1", "On-hold"), 
        ("2", "Dropped"), 
        ("3", "In process - phone interview"), 
        ("4", "In process - interviewing"),
        ("5", "In process - proposal sent"),
        ("6", "Contracted"),
        ("7", "Proposal rejected")
    )

    EXP_CHOICES = (
        ("1", "Entry-level"),
        ("2", "Junior"),
        ("3", "Mid"),
        ("4", "Senior"),
    )
    
    name = forms.CharField(widget=forms.TextInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 70%; background: 0 0; margin-bottom:8%;'}))
    type = forms.CharField(widget=forms.TextInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:2%;'}))
    enterprise = forms.CharField(widget=forms.TextInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:2%;'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:2%;'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:2%;'}))
    linkedin = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:2%;'}))
    source = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:5%;'}))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], widget=forms.NumberInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:2%;'}))
    years_exp = forms.IntegerField(widget=forms.Select(choices=EXP_CHOICES, attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-top:1%; margin-bottom:2%;'}))
    status = forms.CharField(widget=forms.Select(choices=STATUS_CHOICES, attrs={'name': 'name-status', 'style': 'width: 50%; background-color: #EEEEEE; color: black; border-style: none;', 'class': 'btn btn-secondary btn-sm dropdown-toggle'}))
    pipeline_status = forms.CharField(required=False, widget=forms.Select(choices=PIPELINE_STATUS_CHOICES, attrs={'name': 'name-pipeline-status', 'style': 'width: 50%; background-color: #EEEEEE; color: black; border-style: none;', 'class': 'btn btn-secondary btn-sm dropdown-toggle'}))
    comments = forms.CharField(required=False, widget=forms.TextInput(attrs={'style': 'font-family: IBM Plex Mono; font-style: normal; font-weight: 500; font-size: 13px; line-height: 17px; margin: 2%; border-style: none; font-size: 100%; color: #000000; line-height: 0;display: block; width: 80%; background: 0 0;'}))
    HiringManager = forms.ModelChoiceField(empty_label=None, queryset=HiringManager.objects.all().order_by('name'), widget=forms.Select(attrs={'style': 'margin-bottom: 5%; width: 50%; background-color: #EEEEEE; color: black; border-style: none;', 'class': 'btn btn-secondary btn-sm dropdown-toggle'}))

    # Campos auxiliares para o dropdown do contact person
    contact_person_type = forms.CharField(widget=forms.TextInput)
    contact_person_id = forms.IntegerField(widget=forms.NumberInput)

    class Meta:
        model = Candidate
        fields = ['name', 'type', 'enterprise', 'email', 'location', 'linkedin', 'source', 'phone_number', 'years_exp', 'status', 'pipeline_status', 'comments', 'HiringManager','image']
        

class HrCreate(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom: 25%;'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:5%;'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:5%;'}))
    type = forms.IntegerField(required = False)
    class Meta:
        model = HR
        fields = ('name', 'password','email','image')

class HiringManagerCreate(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom: 25%;'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:5%;'}))
    password = forms.CharField(widget=forms.PasswordInput(render_value=True, attrs={'style': 'position: relative; border-style: none; border-bottom: 2px solid #adadad; font-size: 100%; color: #555; line-height: 0; display: block; width: 80%; background: 0 0; margin-bottom:5%;'}))
    type = forms.IntegerField(required = False)
    class Meta:
        model = HiringManager
        fields = ('name', 'password','email','image')
