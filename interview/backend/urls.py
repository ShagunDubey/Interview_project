from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.create, name='create'),
    path('update_request/<int:pk>',views.update_request,name='update_request'),
    path('update/',views.update,name='update'),
    path('delete/', views.delete,name='delete')
]