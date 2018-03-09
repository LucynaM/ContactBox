from django.shortcuts import render, redirect
from django.views import View
from .models import Person, Address, Email, Phone, Group
from .forms import PersonForm, AddressForm, PhoneForm, EmailForm, DeletePersonForm, GroupForm, SearchForm

# Create your views here.

class ShowPeople(View):
    """Show all people in contact box"""
    def get(self, request):
        people = Person.objects.all()
        context = {'people': people}
        return render(request, 'contacts_box/index.html', context)


class PersonDetails(View):
    """Show person details"""
    def get(self, request, id):
        person = Person.objects.get(id=id)
        context = {
            'person': person,
        }
        return render(request, 'contacts_box/person_details.html', context)


class AddPerson(View):
    """Add new person"""
    def get(self, request):
        form_person = PersonForm()
        form_address = AddressForm()
        form_phone = PhoneForm()
        form_email = EmailForm()
        ctx = {
            'form_person': form_person,
            'form_address': form_address,
            'form_phone': form_phone,
            'form_email': form_email,
        }
        return render(request, 'contacts_box/add_person.html', ctx)

    def post(self, request):
        form_person = PersonForm(request.POST)
        form_address = AddressForm(request.POST)
        form_phone = PhoneForm(request.POST)
        form_email = EmailForm(request.POST)
        form_person_valid = form_person.is_valid()
        form_address_valid = form_address.is_valid()
        form_phone_valid = form_phone.is_valid()
        form_email_valid = form_email.is_valid()

        if form_person_valid and form_address_valid and form_phone_valid and form_email_valid:

            # save new address object
            if Address.objects.filter(**form_address.cleaned_data):
                address = Address.objects.get(**form_address.cleaned_data)
            else:
                address = Address.objects.create(**form_address.cleaned_data)

            # save new person object
            person = Person.objects.create(address=address, **form_person.cleaned_data)

            # save new phone object
            if form_phone.cleaned_data['home_phone'] is not None:
                home_phone = form_phone.cleaned_data['home_phone']
                Phone.objects.create(number=home_phone, type=1, owner=person)
            if form_phone.cleaned_data['business_phone'] is not None:
                business_phone = form_phone.cleaned_data['business_phone']
                Phone.objects.create(number=business_phone, type=2, owner=person)

            # save new email object
            if form_email.cleaned_data['home_email'] != '':
                home_email = form_email.cleaned_data['home_email']
                Email.objects.create(email=home_email, type=1, owner=person)
            if form_email.cleaned_data['business_email'] != '':
                business_email = form_email.cleaned_data['business_email']
                Email.objects.create(email=business_email, type=2, owner=person)

            return redirect('contacts_box:person_details', id=person.id)

        ctx = {
            'form_person': form_person,
            'form_address': form_address,
            'form_phone': form_phone,
            'form_email': form_email,
        }
        return render(request, 'contacts_box/add_person.html', ctx)


class EditPerson(View):
    """Edit person details"""
    def get(self, request, id):
        person = Person.objects.get(id=id)
        phones = {}
        emails = {}

        for phone in person.phones.all():
            if phone.type == 1:
                phones['home_phone'] = phone.number
            else:
                phones['business_phone'] = phone.number

        for email in person.emails.all():
            if email.type == 1:
                emails['home_email'] = email.email
            else:
                emails['business_email'] = email.email

        form_person = PersonForm(instance=person)
        form_address = AddressForm(instance=person.address)
        form_phone = PhoneForm(initial=phones)
        form_email = EmailForm(initial=emails)


        ctx = {
            'form_person': form_person,
            'form_address': form_address,
            'form_phone': form_phone,
            'form_email': form_email,
        }
        return render(request, 'contacts_box/edit_person.html', ctx)

    def post(self, request, id):

        person = Person.objects.get(id=id)
        current_address = person.address

        form_person = PersonForm(request.POST)
        form_address = AddressForm(request.POST)
        form_phone = PhoneForm(request.POST)
        form_email = EmailForm(request.POST)
        form_person_valid = form_person.is_valid()
        form_address_valid = form_address.is_valid()
        form_phone_valid = form_phone.is_valid()
        form_email_valid = form_email.is_valid()

        if form_person_valid and form_address_valid and form_phone_valid and form_email_valid:
            # update person object
            Person.objects.filter(pk=id).update(**form_person.cleaned_data)
            # update address object
            if Address.objects.filter(**form_address.cleaned_data):
                new_address = Address.objects.get(**form_address.cleaned_data)
            else:
                new_address = Address.objects.create(**form_address.cleaned_data)
            person.address = new_address
            person.save()

            # delete address object if not assigned to any person
            if not Person.objects.filter(address=current_address.id).count():
                current_address.delete()

            # update phone object
            if form_phone.cleaned_data['home_phone'] is not None:
                home_phone = form_phone.cleaned_data['home_phone']
                Phone.objects.filter(type=1, owner=person).update(number=home_phone)
            if form_phone.cleaned_data['business_phone'] is not None:
                business_phone = form_phone.cleaned_data['business_phone']
                Phone.objects.filter(type=2, owner=person).update(number=business_phone)

            # update email object
            if form_email.cleaned_data['home_email'] != '':
                home_email = form_email.cleaned_data['home_email']
                Email.objects.filter(type=1, owner=person).update(email=home_email)
            if form_email.cleaned_data['business_email'] != '':
                business_email = form_email.cleaned_data['business_email']
                Email.objects.filter(type=2, owner=person).update(email=business_email)

            return redirect('contacts_box:person_details', id=person.id)

        ctx = {
            'form_person': form_person,
            'form_address': form_address,
            'form_phone': form_phone,
            'form_email': form_email,
        }
        return render(request, 'contacts_box/edit_person.html', ctx)

class DeletePerson(View):
    """Delete single person"""
    def get(self, request, id):
        person = Person.objects.get(id=id)
        initial = {
            'firstname': person.firstname,
            'lastname': person.lastname,
        }
        if person.description:
            initial['description'] = person.description
        form = DeletePersonForm(initial=initial)
        ctx = {
            'form': form,
            'person': person,
        }
        return render(request, 'contacts_box/delete_person.html', ctx)
    def post(self, request, id):
        person = Person.objects.get(id=id)
        person.delete()
        return redirect('contacts_box:people')

class ShowGroups(View):
    """Show all groups"""
    def get(self, request):
        groups = Group.objects.all()
        ctx = {
            'groups': groups
        }
        return render(request, 'contacts_box/groups.html', ctx)

class GroupDetails(View):
    """Show group details"""
    def get(self, request, id):
        group = Group.objects.get(pk=id)
        members = group.member.all()
        ctx = {
            'group': group,
            'members': members,
        }
        return render(request, 'contacts_box/group_details.html', ctx)

class AddGroup(View):
    """Add new group"""
    def get(self, request):
        form = GroupForm()
        ctx = {
            'form': form,
        }
        return render(request, 'contacts_box/add_group.html', ctx)

    def post(self, request):
        form = GroupForm(request.POST)
        if form.is_valid():
            members = form.cleaned_data.pop('member')
            group = form.save()
            group.member.set(member for member in members)
            return redirect('contacts_box:groups')
        ctx = {
            'form': form,
        }
        return render(request, 'contacts_box/add_group.html', ctx)

class EditGroup(View):
    """Edit group"""
    def get(self, request, id):
        group = Group.objects.get(pk=id)
        form = GroupForm(instance=group)
        ctx = {
            'form': form,
        }
        return render(request, 'contacts_box/edit_group.html', ctx)
    def post(self, request, id):
        group = Group.objects.get(pk=id)
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            members = form.cleaned_data.pop('member')
            group = form.save()
            group.member.set(member for member in members)
            return redirect('contacts_box:group_details', id=group.id)
        ctx = {
            'form': form,
        }
        return render(request, 'contacts_box/edit_group.html', ctx)

class DeleteGroup(View):
    """Delete group"""
    def get(self, request, id):
        group = Group.objects.get(pk=id)
        ctx = {
            'group': group,
        }
        return render(request, 'contacts_box/delete_group.html', ctx)
    def post(self, request, id):
        group = Group.objects.get(pk=id)
        group.delete()
        return redirect('contacts_box:groups')

class SearchPerson(View):
    def get(self, request):
        form = SearchForm()
        ctx = {
            'form': form,
        }
        return render(request, 'contacts_box/search.html', ctx)
    def post(self, request):
        form = SearchForm(request.POST)
        people = None
        msg = ""
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            if firstname != "" and lastname != "":
                people = Person.objects.filter(firstname__icontains=firstname, lastname__icontains=lastname)
            elif firstname != "":
                people = Person.objects.filter(firstname__icontains=firstname)
            elif lastname != "":
                people = Person.objects.filter(lastname__icontains=lastname)
            else:
                msg = "At least one field must be filled to perform search"
        ctx = {
            'form': form,
            'people': people,
            'msg': msg,
        }
        return render(request, 'contacts_box/search.html', ctx)
