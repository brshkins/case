from django.contrib import admin
from django.urls import path, include
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('test1/', views.test1, name='test1'),
    path('test1_result/<int:result_id>/', views.test1_result, name='test1_result'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
