from django.utils.encoding import smart_unicode
from django.contrib.localflavor.us.forms import USPhoneNumberField
from django.forms.util import ErrorList
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django import forms
from django.forms import ModelForm, Form, ModelChoiceField
from django.utils.translation import ugettext_lazy as _

from user_profile import *
from portal.l10n.models import *

class UserAccountForm(Form):
    first_name = forms.CharField(label=_("First Name"), max_length=30, required=True)
    last_name = forms.CharField(label=_("Last Name"), max_length=30, required=True)
    email = forms.EmailField(label=_('Email'), required=True, max_length=75)
    address1 = forms.CharField(label=_('Address 1'), max_length=50, required=False)
    address2 = forms.CharField(label=_('Address 2'), max_length=50, required=False)
    city = forms.CharField(label=_('City'), max_length=50, required=False)
    state = forms.CharField(label=_('State'), max_length=30, required=False)
    postal_code = forms.CharField(label=_('Postal Code'), max_length=30, required=False)
    country = forms.ModelChoiceField(label=_("Country"), required=False, queryset=Country.objects.all())
    phone = forms.CharField(label=_('Phone'), max_length=30, required=False)

    def __init__(self, data=None, email_changed=False, **kwargs):
        self.email_changed = email_changed
        super(UserAccountForm, self).__init__(data,**kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data
        address1 = cleaned_data.get('address1', None)
        address2 = cleaned_data.get('address2', None)
    	city = cleaned_data.get('city', None)
    	state = cleaned_data.get('state', None)
    	country = cleaned_data.get('country', None)
    	phone = cleaned_data.get('phone', None)
        #if phone_number and not country_code:
        #    if 'country_code' not in self._errors:
        #        self._errors['country_code'] = ErrorList([_("This field is required if you enter an international phone number.")])
        #    if 'country_code' in cleaned_data:
        #        del cleaned_data['country_code']

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if not email:
            raise forms.ValidationError(_("This field is required."))
            
        if not self.email_changed:
            return email
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        except Exception as e:
            pass
        
        raise forms.ValidationError(_("This email has already been registered, please enter a different one."))
        
class OrderBillToForm(Form):
    billto_name = forms.CharField(label=_("Name"), max_length=100, required=True)
    billto_address1 = forms.CharField(label=_("Address 1"),max_length=50, required=True)
    billto_address2 = forms.CharField(label=_("Address 2"), max_length=50, required=False)
    billto_city = forms.CharField(label=_("City"), max_length=50, required=True)
    billto_state = forms.CharField(label=_("State"), max_length=30, required=True)
    billto_postal_code = forms.CharField(label=_("Postal Code"), max_length=9, required=True)
    billto_country = forms.CharField(label=_("Country"), max_length=50, required=True)
    billto_phone = forms.CharField(label=_("Phone"), max_length=30, required=False)
    billto_email = forms.CharField(label=_("Email"), max_length=100, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        billto_name = cleaned_data.get('billto_name', None)
        billto_address1 = cleaned_data.get('billto_address1', None)
        billto_address2 = cleaned_data.get('billto_address2', None)
    	billto_city = cleaned_data.get('billto_city', None)
    	billto_state = cleaned_data.get('billto_state', None)
    	billto_postal_code = cleaned_data.get('billto_postal_code', None)
    	billto_country = cleaned_data.get('billto_country', None)
    	billto_phone = cleaned_data.get('billto_phone', None)
    	billto_email = cleaned_data.get('billto_email', None)

        return cleaned_data
                
class OrderShipToForm(Form):
    shipto_name = forms.CharField(label=_("Name"), max_length=100, required=True)
    shipto_address1 = forms.CharField(label=_("Address 1"),max_length=50, required=True)
    shipto_address2 = forms.CharField(label=_("Address 2"), max_length=50, required=False)
    shipto_city = forms.CharField(label=_("City"), max_length=50, required=True)
    shipto_state = forms.CharField(label=_("State"), max_length=30, required=True)
    shipto_postal_code = forms.CharField(label=_("Postal Code"), max_length=9, required=True)
    shipto_country = forms.CharField(label=_("Country"), max_length=50, required=True)
    shipto_phone = forms.CharField(label=_("Phone"), max_length=30, required=False)
    shipto_email = forms.CharField(label=_("Email"), max_length=100, required=False)

    def clean(self):
        cleaned_data = self.cleaned_data
        shipto_name = cleaned_data.get('shipto_name', None)
        shipto_address1 = cleaned_data.get('shipto_address1', None)
        shipto_address2 = cleaned_data.get('shipto_address2', None)
    	shipto_city = cleaned_data.get('shipto_city', None)
    	shipto_state = cleaned_data.get('shipto_state', None)
    	shipto_postal_code = cleaned_data.get('shipto_postal_code', None)
    	shipto_country = cleaned_data.get('shipto_country', None)
    	shipto_phone = cleaned_data.get('shipto_phone', None)
    	shipto_email = cleaned_data.get('shipto_email', None)

        return cleaned_data
                
class PasswordReset(Form):
    email = forms.EmailField(label=_("Email"))
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError(_("This email does not exist."))
        return email
                
class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=PasswordInput(attrs={"class":"form-control"}))
    
class CustomAuthenticationForm(forms.Form):
    username = forms.CharField(max_length=75, widget=forms.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))

    def __init__(self, request=None, *args, **kwargs):
        """
        If request is passed in, the form will validate that cookies are
        enabled. Note that the request (a HttpRequest object) must have set a
        cookie with the key TEST_COOKIE_NAME and value TEST_COOKIE_VALUE before
        running this validation.
        """
        self.request = request
        self.user_cache = None
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower()
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))

        return self.cleaned_data

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
