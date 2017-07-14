from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ApplicationDetailView
from . import views


app_name = 'sua'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^apply_sua$', views.apply_sua, name='apply_sua'),
    url(
        r'^application/(?P<pk>[0-9]+)/$',
        login_required(ApplicationDetailView.as_view()),
        name='application_detail',
    ),
]
