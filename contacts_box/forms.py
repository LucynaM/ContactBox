from django import forms
from django.core.validators import validate_email
from .models import Person, Address, Group, Phone, Email, TYPES


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = '__all__'

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        exclude = ('address',)

class PhoneForm(forms.Form):
    home_phone = forms.IntegerField(required=False, )
    business_phone = forms.IntegerField(required=False, )

class EmailForm(forms.Form):
    home_email = forms.CharField(max_length=64, required=False, validators=[validate_email], )
    business_email = forms.CharField(max_length=64, required=False, validators=[validate_email], )

class DeletePersonForm(forms.Form):
    # person
    firstname = forms.CharField(max_length=64,)
    lastname = forms.CharField(max_length=64,)
    description = forms.CharField(widget=forms.Textarea, required=False,)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = '__all__'

class SearchForm(forms.Form):
    firstname = forms.CharField(max_length=64, required=False)
    lastname = forms.CharField(max_length=64, required=False)
