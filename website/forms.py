from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from website.models import Booking,Profile
import phonenumbers


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=False, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    class Meta:
        model = User
        fields = ('username',  'name', 'birth_date', 'email', 'password1', 'password2' )
    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        return cleaned_data


class BookingForm(forms.ModelForm):
  
  class Meta:
    model = Booking

    fields = ('name', 'phone_number')

  def clean(self):
    
    cleaned_data = super(BookingForm, self).clean()

    gotten_phone_number = cleaned_data.get('phone_number')

    '''if len(gotten_phone_number) != 10:
        print("ADFS")
        raise forms.ValidationError('The phone number is not a valid')'''

    return cleaned_data

class ProfileUpdate(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ('bio','location','phone')

  '''def save(self, User = None):
    user_profile = super(ProfileUpdate,self).save(commit =False)
    print("www")
    print(type(user_profile))
    if User:
      user_profile.Profile = User
      print('222')
    user_profile.save()
    return user_profile'''
  