from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    # The url where the upload form is located:
    url(r'^$', 'plupload.views.upload'),
    # the url where the upload petition is processed
    url(r'^plupload/', 'plupload.views.upload_file'),
    # The folowing are the urls for a custom upload queue
    url(r'^custom_queue$', 'plupload.views.upload_custom'),
    url(r'^del_file/(\d{4})/(\d{2})/(\d+)/$',
        'plupload.views.del_file'),
    # retrieves a list of all files in a dir, change as convenient
    url(r'^get_all_files/(\d{4})/(\d{2})/(\d+)/$',
        'plupload.views.get_all_files'),
)
