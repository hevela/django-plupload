from django.conf.urls import patterns, include, url
import plupload.views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    #The url where the upload form is located:
    url(r'^$', 'plupload.views.upload'),
    #the url where the upload petition is processed
    url(r'^plupload/', 'plupload.views.upload_file'),
)
