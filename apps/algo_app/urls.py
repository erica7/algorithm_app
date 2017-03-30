from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^random$', views.random),
    url(r'^manage$', views.manage), # manage page for algo, tags, & langs with forms to add new, buttons to edit and delete

    url(r'^admin/login$', views.admin_login),
    url(r'^admin/logout$', views.admin_logout),

    url(r'^tag/create$', views.create_tag), # POST method to create in db
    url(r'^tag/(?P<id>\d+)/edit$', views.edit_tag), # form to edit
    url(r'^tag/(?P<id>\d+)/update$', views.update_tag), # POST method to update db
    url(r'^tag/(?P<id>\d+)/destroy$', views.destroy_tag), # POST method to destroy/remove from db

    url(r'^language/create$', views.create_language), # POST method to create in db
    url(r'^language/(?P<id>\d+)/edit$', views.edit_language), # form to edit
    url(r'^language/(?P<id>\d+)/update$', views.update_language), # POST method to update db
    url(r'^language/(?P<id>\d+)/destroy$', views.destroy_language), # POST method to destroy/remove from db

    url(r'^algorithm/create$', views.create_algorithm), # POST method to create in db
    url(r'^algorithm/(?P<id>\d+)$', views.show, name='algorithm'),
    url(r'^algorithm/(?P<id>\d+)/show$', views.show_solution),
    url(r'^algorithm/(?P<id>\d+)/hide$', views.hide_solution),
    url(r'^algorithm/(?P<id>\d+)/edit$', views.edit), # form to edit
    url(r'^algorithm/(?P<id>\d+)/update$', views.update), # POST method to update db
    url(r'^algorithm/(?P<id>\d+)/delete$', views.delete), # form to confirm delete
    url(r'^algorithm/(?P<id>\d+)/destroy$', views.destroy), # POST method to destroy/remove from db
    url(r'^algorithm/(?P<id>\d+)/add_solution$', views.add_solution), # POST method to destroy/remove from db
    url(r'^algorithm/search$', views.search), # POST method to search; redirect to /algorithm/<id>
    url(r'^algorithm/results$', views.results), # render results.html
    url(r'^algorithm/random$', views.random), # POST method to get random; redirect to /algorithm/<id?

    url(r'^solution/create$', views.add_solution), # POST method to create in db
    url(r'^solution/(?P<id>\d+)$', views.show_solution),
    url(r'^solution/(?P<id>\d+)/edit$', views.edit_solution), # form to edit
    url(r'^solution/(?P<id>\d+)/update$', views.update_solution), # POST method to update db
    url(r'^solution/(?P<id>\d+)/delete$', views.delete_solution), # form to confirm delete
    url(r'^solution/(?P<id>\d+)/destroy$', views.destroy_solution), # POST method to destroy/remove from db
]
