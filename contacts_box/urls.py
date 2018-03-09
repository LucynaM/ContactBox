
from django.conf.urls import url, include
from .views import ShowPeople, AddPerson, EditPerson, DeletePerson, PersonDetails, \
    ShowGroups, AddGroup, EditGroup, DeleteGroup, GroupDetails, SearchPerson

urlpatterns = [
    url(r'^$', ShowPeople.as_view(), name="people"),
    url(r'^person/(?P<id>(\d)+)/$', PersonDetails.as_view(), name="person_details"),
    url(r'^person/add/$', AddPerson.as_view(), name="add_person"),
    url(r'^person/edit/(?P<id>(\d)+)/$', EditPerson.as_view(), name="edit_person"),
    url(r'^person/delete/person/(?P<id>(\d)+)/$', DeletePerson.as_view(), name="delete_person"),
    url(r'^groups/$', ShowGroups.as_view(), name="groups"),
    url(r'^group/(?P<id>(\d)+)/$', GroupDetails.as_view(), name="group_details"),
    url(r'^group/add/$', AddGroup.as_view(), name="add_group"),
    url(r'^group/edit/(?P<id>(\d)+)/$', EditGroup.as_view(), name="edit_group"),
    url(r'^group/delete/group/(?P<id>(\d)+)/$', DeleteGroup.as_view(), name="delete_group"),
    url(r'^search/$', SearchPerson.as_view(), name="search"),
]
