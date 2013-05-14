from django.conf.urls import patterns, include, url
import plupload.views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    #The url where the upload form is located:
    url(r'^$', 'plupload.views.upload'),
    url(r'^custom_queue$', 'plupload.views.upload_custom'),
    #the url where the upload petition is processed
    url(r'^plupload/', 'plupload.views.upload_file'),
    #I'm using a dir with todays date as name, change urls as convenient
    url(r'^get_files/(\d{4})/(\d{2})/(\d+)/$',
        'plupload.views.get_files'),
    url(r'^del_file/(\d{4})/(\d{2})/(\d+)/$',
        'plupload.views.del_file'),
)
