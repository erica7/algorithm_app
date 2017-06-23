from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^random$', views.random),

    url(r'^algorithms/(?P<id>\d+)$', views.show, name='algorithm'),
    url(r'^algorithms/search$', views.search), # POST method to search; redirect to /algorithm/<id>
    url(r'^algorithms/random$', views.random), # POST method to get random; redirect to /algorithms/<id>

    url(r'^calculate$', views.calculate),
]
