
from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^api_doc$', views.api_doc, name="api_doc"),
    url(r'^get_file$', views.get_file, name="get_file"),
    url(r'^run_rename$', views.run_rename_request, name="run_rename_request"),
    url(r'^run_wordfrequency$', views.run_wordfrequency_request, name="run_wordfrequency_request"),
    url(r'^run_sentistrength$', views.run_sentistrength_request, name="run_sentistrength_request"),
    url(r'^delete_all$', views.delete_all_uploads, name="delete_all_uploads"),
    url(r'^run_posit$', views.run_posit, name="run_posit"),
    url(r'^api_posit$', views.api_posit_zipped, name="api_posit_zipped"),
    url(r'^api_posit_single$', views.api_posit, name="api_posit"),
    url(r'^result/(?P<filename>[a-zA-Z0-9-]+)$', views.api_result, name='api_result'),
    url(r'^download/(?P<filename>[a-zA-Z0-9-]+)$', views.download_result, name='download_result'),
    url(r'^intermiediatepage/(?P<filename>[a-zA-Z0-9-]+)$', views.run_posit_intermiediatepage, name='run_posit_intermiediatepage'),

]
