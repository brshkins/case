from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test1/', views.test1, name='test1'),
    path('test1_result/<int:result_id>/', views.test1_result, name='test1_result'),
    path('test2/', views.test2, name='test2'),
    path('test2_result/<int:result_id>/', views.test2_result, name='test2_result'),
    path('test3/', views.test3, name='test3'),
    path('test3_result/<int:result_id>/', views.test3_result, name='test3_result'),
]
