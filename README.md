django-plupload
===============

django-plupload is a barebones multi file upload app for django. Uses plupload [http://www.plupload.com/], and jQuery.
You can use it in your applications with simple inclusion tag.

**Requirements:**
- Nothing really, if you plan to upload images, then you'll need PIL, but just for files, you don't need anything
- Well, you'll need django (at least 1.4v) installed and running

**Usage:**
In the html template just load the 'plupload_script' tag passing the csrf token to generate the javascript needed, 
and include the 'pl_upload_form' to generate the 'div' where the upload queue will show:

    <!DOCTYPE html>
    <html>
    <head>
        <title></title>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"></script>
        {% load plupload %}
        {% plupload_script csrf_token  %}
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
    
**Installation**

1.Install an app. Do it by adding:

    'plupload', 

string to your settings.py -> INSTALLED_APPS = () dictionary.

2.Register urls in your root urlconf urls.py adding string to your urlpatterns like so :

    #The url where the upload form is located:
    url(r'^$', 'plupload.views.upload'),
    
3.In plupload/views.py, change the FILE_FOLDER var to whatever dir you want to use:    

    FILE_FOLDER = "templates/static/media/csv_files/"
    
Note that 'FILE_FOLDER' is relative to your 'PROJECT_PATH', wich is added in settings.py

4.Edit templates and styles to meet your needs. (Optional)
    (for e.g. changing the form design and/or behavior)

**Models**

It's barebones, so it doesn't need any model, so you can easily modify the plupload.py views functions to meet your needs :)

That's all, I'm open for sugestions, or bug corrections if you find one.
