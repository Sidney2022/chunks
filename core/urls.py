from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='home'),
    path('saved_chunks', views.saved_chunks, name='saved_chunks'),
    path('new_chunk', views.new_chunk, name='new_chunk'),
    path('signin', views.signin, name='login'),
    path('logout', views.logout, name = 'logout'),
    path('signup', views.signup, name = 'signup'),


    # path('signup', views.signup, name='register'),
    # path('/file_upload', views.file_upload, name='file_upload')
]