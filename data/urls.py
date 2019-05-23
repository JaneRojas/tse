from django.urls import path
from . import views

app_name = 'data'

urlpatterns = [
    path('', views.listViewData.as_view(), name='getAllData'),
    path('statistics/', views.getQuantityVoters, name='statistics'),
    path('filter/', views.searchListView.as_view(), name='search_person'),
    path('distelec/', views.distelecListView.as_view(), name='distelec'),
    path('<str:cedula>/', views.info_by_person.as_view(), name='info_by_person'),
    path('distelec/<str:codele>/', views.info_by_distelec.as_view(), name='info_by_distelec'),
    path('create_person/', views.personCreateView.as_view(), name='create-person')
]
from django.conf.urls import url
