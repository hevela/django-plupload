import os
import datetime
import random
import string

from django.http import HttpResponse, Http404
from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response

#Dirertory where you want to save your files
FILE_FOLDER = "templates/static/media/csv_files/"


def upload(request):
    if request.method == "POST":
        # Do any other process once you have upoloaded you files
        print "post"
    template_vars_template = RequestContext(request)
    return render_to_response('upload_form.html',
                              template_vars_template)


def upload_file(request):
    if request.method == 'POST' and request.FILES:
        dir_name = str(datetime.date.today())
        dir_fd = os.open(os.path.join(settings.PROJECT_PATH,
                                      FILE_FOLDER),
                         os.O_RDONLY)
        os.fchdir(dir_fd)
        #creates a directory named to today's date
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        os.chdir(dir_name)

        for _file in request.FILES:
            handle_uploaded_file(request.FILES[_file], "csv")
        os.close(dir_fd)
        #response only to notify plUpload that the upload was successful
        return HttpResponse()
    else:
        raise Http404


def handle_uploaded_file(f, ext):
    """
    Here you can do whatever you like with your files, like resize them if they
    are images
    :param f: the file
    :param ext: extention to append in the file name
    """
    file_name = random_string_generator()
    file_name += "." + ext
    with open(file_name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def random_string_generator(size=6,
                            chars=string.ascii_uppercase + string.digits):
    """Random String Generator

    :param size: longitud de la cadena (default 6)
    :param chars: caracteres de entre los que generara la cadena
                  (default [A-Z0-9])
    :return: generated random string
    >>> id_generator()
    'G5G74W'
    >>> id_generator(3, "6793YUIO")
    'Y3U'

    """
    return ''.join(random.choice(chars) for x in range(size))