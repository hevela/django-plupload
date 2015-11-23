[![Build Status](https://secure.travis-ci.org/vellonce/django-plupload.svg?branch=master)](https://secure.travis-ci.org/vellonce/django-plupload?branch=master)
[![Coverage](https://codecov.io/github/vellonce/django-plupload/coverage.svg?branch=master)](https://codecov.io/github/vellonce/django-plupload?branch=master)

# django-plupload

django-plupload is a barebones multi file upload app for django. Uses plupload [http://www.plupload.com/], and jQuery.
You can use it in your applications with simple inclusion tag.

## Requirements
- Django 1.4+
- Pillow if you need to upload images

## Usage

In the html template just load the 'plupload_script' tag passing the csrf token to generate the javascript needed,
along with the url where you are going to process the file uploads.
and include the 'pl_upload_form' to generate the 'div' where the upload queue will appear:

    <!DOCTYPE html>
    <html>
    <head>
        <title></title>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        {% load plupload %}
        {% plupload_script csrf_token "/plupload/" %}
    </head>
    <body>
        <form method="post" action=".">
        {% csrf_token %}
        {% pl_upload_form %}
            <p>
                <button type="submit">Save</button>
            </p>
        </form>
    </body>
    </html>

## Using the PlUploadFormField

If you have a model that defines a `FileField`, for example:

    class MyUpload(models.Model):

        uploads = models.FileField(
            blank=True, null=True
        )


The `PlUploadFormField` can be used on a form like this:

    class UploadForm(forms.ModelForm):

        class Meta:
            model = MyUpload

        uploads = PlUploadFormField(
            path='uploads',
            options={
                "max_file_size": '5000mb'
            }
        )

All the values in the `options` dictionary will be passed to the PlUpload constructor.

For a full list of options that can be passed to PlUpload, please refer to:

http://www.plupload.com/docs/Options

### TODO

* Make PlUploadFormField fully customizable

## Installation

1.Add 'plupload' to your INSTALLED_APPS

2.Register urls in your root urlconf urls.py adding string to your urlpatterns like so :

    #The url where the upload form is located:
    url(r'^$', 'plupload.views.upload'),

3.Specify the directory in which you would like to save the uploaded files:

    UPLOAD_ROOT = '/tmp/upload/


4.Edit templates and styles to meet your needs. (Optional)
    (for e.g. changing the form design and/or behavior)

## Models

It's barebones, so it doesn't need any model, so you can easily modify the plupload.py views functions to meet your needs :)

That's all, I'm open for sugestions, or bug corrections if you find one.
