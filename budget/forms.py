from django.contrib.auth import forms
from django.forms import ModelForm, DateField
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Expense

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model=User #built in model
        fields=["first_name","last_name","username","email","password1","password2"]


class ExpenseCreateForm(ModelForm):
    class Meta:
        model=Expense
        fields="__all__"

    def clean(self):
        cleaned_data=super().clean()
        amount=cleaned_data.get("amount")
        if amount<50:
            msg="invalid amount"
            self.add_error("amount",msg)

# class DateSearchForm(forms.Form):
#     date = forms.DateField()
