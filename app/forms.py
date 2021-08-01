from django import forms
from django.db.models import fields
from django.forms.models import ModelForm
from .models import Contact, Profile, Report, ServiceRequest


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('Full_Name', 'gender', 'mobile', 'pic', 'address')

class ServiceRequestForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ('durations', 'gender', 'age', 'request_for')
        
class ContactForm(forms.ModelForm):
    """Form definition for Contact."""

    class Meta:
        """Meta definition for Contactform."""

        model = Contact
        fields = ('name','email','subject','messages')

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ('feedbackfor','message','rating')

