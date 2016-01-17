from django import forms
from django.forms import Form
from db.models.user_profile import User, UserProfile


class UserAccountForm(Form):
    first_name = forms.CharField(label="First Name", max_length=30, required=True)
    last_name = forms.CharField(label="Last Name", max_length=30, required=True)
    email = forms.EmailField(label="Email", required=True, max_length=75)

    def __init__(self, data=None, email_changed=False, **kwargs):
        self.email_changed = email_changed
        super(UserAccountForm, self).__init__(data,**kwargs)

    def clean(self):
        cleaned_data = self.cleaned_data

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if not email:
            raise forms.ValidationError("This field is required.")

        if not self.email_changed:
            return email
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        except Exception as e:
            pass

        raise forms.ValidationError("This email has already been registered, please enter a different one.")


class PasswordReset(Form):
    email = forms.EmailField(label="Email")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("This email does not exist.")
        return email
