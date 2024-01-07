from django.urls import path
from .views import AppointmentView

app_name = 'appointment'

urlpatterns = (
    path('appoint/', AppointmentView.as_view(), name='appointment'),
)
