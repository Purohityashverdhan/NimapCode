from django.urls import path
from . import views

urlpatterns = [
    path('clients/', views.ClientListCreateView.as_view(), name='client-list-create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client-detail'),
    path('clients/<int:client_id>/projects/', views.ProjectListCreateView.as_view(), name='client-projects-create'),
    path('projects/', views.UserProjectsView.as_view(), name='user-projects'),
]
