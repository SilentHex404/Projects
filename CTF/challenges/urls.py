from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('challenges/',views.challenges,name='challenges'),
    path('chall/<str:id>/',views.Chall,name='chall'),
    path('DownloadFile/<str:id>/',views.DownloadFile,name='DownloadFile'),
    path('SubmitFlag/',views.SubmitFlag,name='SubmitFlag'),
    path('CreateChall/',views.CreateChall,name='CreateChall'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)