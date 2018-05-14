from django.conf.urls import url
from . import views
  
urlpatterns = [
    url(r'^$', views.index, name="home"),
    url(r'^signup/$', views.signup, name="signup"),
    url(r'^signup/process$', views.signup_process),
    url(r'^signup/success$', views.signup_success, name="signup_success"),
    url(r'^signin/$', views.signin, name="signin"),
    url(r'^signin/process$', views.signin_process),
    url(r'^signout$', views.signout_process, name="signout_process"),
    url(r'^dashboard$', views.dashboard, name="dashboard")
]