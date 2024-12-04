from django import forms
from .models import Code
#this is the modelform for allowing users to input verification code in verify 
class VerificationCodeForm(forms.ModelForm):
    number = forms.CharField(
        label='code',
        help_text= 'enter SMS Verification Code') # feild to enter code

    class Meta: #defines configuration options
        model = Code
        fields = ('number', )