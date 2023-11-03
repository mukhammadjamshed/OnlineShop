from django.urls import path

from pages.models import ContactModel
from pages.views import ContactCreateView, AboutTemplateView, HomeTemplateView

app_name = 'pages'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
]
