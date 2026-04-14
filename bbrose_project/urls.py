from django.contrib import admin
from django.urls import path, include
from questionnaire import views as questionnaire_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('questionnaire.urls')),
    path('media/<path:path>', questionnaire_views.media_file, name='media_file'),
]
