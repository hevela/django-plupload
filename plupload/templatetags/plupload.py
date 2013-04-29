from django import template
from django.conf import settings

register = template.Library()


class PluploadScript(template.Node):
    def __init__(self, csrf_token):
        """generates the necessary script for file upload
        :param csrf_token: token de proteccion
        """
        self.csrf_token = template.Variable(csrf_token)

    def render(self, context):
        return """
            <style type="text/css">@import url(/static/js/jquery.plupload.queue/css/jquery.plupload.queue.css);</style>
            <script type="text/javascript" src="/static/js/plupload.full.js"></script>
            <script type="text/javascript" src="/static/js/jquery.plupload.queue/jquery.plupload.queue.js"></script>
            <script type="text/javascript">
            $(function() {
                $("#uploader").pluploadQueue({
                    // General settings
                    runtimes : 'gears,silverlight,html5,flash',
                    url : '/plupload/',
                    max_file_size : '10mb',
                    chunk_size : '1mb',
                    unique_names : true,
                    multipart_params: {"csrfmiddlewaretoken" : "%s"},

                    // Specify what files to browse for
                    filters : [
                        {title : "CSV files", extensions : "csv"}
                        //{title : "Image files", extensions : "jpg,gif,png"},
                        //{title : "Zip files", extensions : "zip"}
                    ],

                    // Flash settings
                    flash_swf_url : '%sjs/plupload.flash.swf',

                    // Silverlight settings
                    silverlight_xap_url : '%sjs/plupload.silverlight.xap'
                });

                // Client side form validation
                $('form').submit(function(e) {
                    var uploader = $('#uploader').pluploadQueue();

                    // Files in queue upload them first
                    if (uploader.files.length > 0) {
                        // When all files are uploaded submit form
                        uploader.bind('StateChanged', function() {
                            if (uploader.files.length === (uploader.total.uploaded + uploader.total.failed)) {
                                $('form')[0].submit();
                            }
                        });

                        uploader.start();
                    } else {
                        alert('You must queue at least one file.');
                    }

                    return false;
                });
            });
            </script>

            """ % (self.csrf_token.resolve(context), settings.STATIC_URL,
                   settings.STATIC_URL)


def plupload_script(parser, token):
    csrf_token_form = token.split_contents()[1]

    return PluploadScript(csrf_token_form)

register.tag("plupload_script", plupload_script)


class PluploadForm(template.Node):

    def render(self, context):
        return """
				<div id="uploader" style="height: 330px;">
					<p>Loading, if this message does not disappear within
					20 seconds, your browser does not support Flash,
					Silverlight, Gears, BrowserPlus or HTML5</p>
				</div>

				<br style="clear: both" />

        """

def pl_upload_form(parser, token):
    return PluploadForm()

register.tag("pl_upload_form", pl_upload_form)