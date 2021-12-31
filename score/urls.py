from django.urls import path
from . import views

urlpatterns = [
	path('', views.ScoreListView.as_view(), name='score-home'),
]