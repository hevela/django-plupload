from django import template
from django.conf import settings

register = template.Library()


class PluploadScript(template.Node):
    def __init__(self, csrf_token, upload_url):
        """generates the necessary script for file upload
        :param csrf_token: token de proteccion
        """
        self.csrf_token = template.Variable(csrf_token)
        self.upload_url = upload_url

    def render(self, context):
        return """
            <style type="text/css">@import url(%sjs/jquery.plupload.queue/css/jquery.plupload.queue.css);</style>
            <script type="text/javascript" src="%sjs/plupload.full.js"></script>
            <script type="text/javascript" src="%sjs/jquery.plupload.queue/jquery.plupload.queue.js"></script>
            <script type="text/javascript">
            $(function() {
                $("#uploader").pluploadQueue({
                    // General settings
                    runtimes : 'gears,silverlight,html5,flash',
                    //url where you are going to proccess the upload
                    url : %s,
                    max_file_size : '10mb',
                    chunk_size : '1mb',
                    unique_names : true,
                    multipart_params: {"csrfmiddlewaretoken" : "%s"},

                    // Resize images on clientside if we can
                    //uncomment if you are going to upload images
                    //resize : {width : 640, height : 480, quality : 90},

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

            """ % (settings.STATIC_URL, settings.STATIC_URL,
                   settings.STATIC_URL, self.upload_url,
                   self.csrf_token.resolve(context),
                   settings.STATIC_URL, settings.STATIC_URL)


def plupload_script(parser, token):
    parameters = token.split_contents()
    csrf_token_form = parameters[1]
    upload_url = parameters[2]
    return PluploadScript(csrf_token_form, upload_url)

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


class CustomPluploadScript(template.Node):
    def __init__(self, csrf_token, upload_url, url_get_last,
                 delete_file_url, media_folder, all_files_url):
        """generates the necessary script for file upload
        :param csrf_token: token de proteccion
        """
        self.csrf_token = template.Variable(csrf_token)
        self.upload_url = upload_url
        self.url_get_last = template.Variable(url_get_last)
        self.delete_file_url = template.Variable(delete_file_url)
        self.media_folder = template.Variable(media_folder)
        self.all_files_url = template.Variable(all_files_url)

    def render(self, context):
        return """
    <script type="text/javascript" src="%sjs/plupload.full.js">
    </script>
    <style type="text/css">@import url(%scss/custom_queue.css);
    </style>
    <script type="text/javascript">
        $(document).on("ready", function() {
        get_existent_files();
        // -------------Setup----------------
        var uploader = new plupload.Uploader({
            // General settings
            runtimes : 'gears,silverlight,html5,flash',
            url : %s,
            max_file_size : '10mb',
            chunk_size : '1mb',
            container: 'uploader_cont',
            browse_button : 'pickfiles',
            unique_names : true,
            multipart_params: {"csrfmiddlewaretoken" : "%s"},
            // Resize images on clientside if we can
            // uncomment if you are going to upload images
            // resize : {width : 640, height : 480, quality : 90},
            // Specify what files to browse for
            filters : [
                {title : "CSV files", extensions : "csv"}
                //{title : "Image files", extensions : "jpg,gif,png"},
                //{title : "Zip files", extensions : "zip"}
            ],
            // Flash settings
            flash_swf_url : '%sjs/plupload.flash.swf',
            silverlight_xap_url : '%sjs/plupload.silverlight.xap'
        });
        // -------------This function executes at plUpload init----------------
        var thumbs_cont = $("#thumbs_cont");
        var filelist = $('#filelist');
        $('#uploadfiles_table').click(function(e) {
            //links the "uploadfiles" button with the image load event
            uploader.start();
            thumbs_cont.append("<div id='loader'>"+
            "<img src='%simages/loader.gif'/>"+
            "<span>Cargando im&aacute;genes...</span></div>");
            e.preventDefault();
        });
        uploader.init();
        // -------------Generates a table of added files----------------
        uploader.bind('FilesAdded', function(up, files) {
            filelist.removeClass("hidden");
            $("#pickfiles").html("Seleccionar Archivos");
            $("#upload_buttons").addClass("table");
            $.each(files, function(i, file) {
                var nombre_archivo;
                if (file.name.length>14){
                    nombre_archivo = file.name.substr(0, 14) +
                            "&tilde;" +
                            file.name.substr(file.name.length-4, file.name.length)
                }else{
                    nombre_archivo=file.name;
                }
                filelist.append(
                    '<div id="' + file.id + '" class="file_row">' +
                    '<span class="archivo">' +
                    nombre_archivo + '</span><span class="tamanio">' +
                    plupload.formatSize(file.size) + '</span>'+
                    '<span class="progreso"><span></span>'+
                    '<div id="progress-bar">'+
                    '<div id="progress-level"></div>'+
                    '</div>'+
                    '</span>' +
                    '</div>');
                thumbs_cont.append('<div id="thumb_' + file.id +
                '" class="thumb_container hidden"></div>');
            });
            $("#uploadfiles_table").removeClass("hidden");

            if(thumbs_cont.is(":hidden")){
                thumbs_cont.removeClass("hidden");
            }
            if(thumbs_cont.height()<filelist.height()){
                thumbs_cont.css("min-height", filelist.height()+38);
            }
            up.refresh(); // Reposition Flash/Silverlight
        });
        // -------------on file upload progress
        uploader.bind('UploadProgress', function(up, file) {
            $('#' + file.id + " .progreso span").html(file.percent + "%%");
            $("#progress-level").css("width",file.percent + "%%");
        });
        // ----Detects and delete bad format files from the upload queue------
        uploader.bind('Error', function(up, err) {
            $('#uploader_cont').append("<div id='err_"+err.file.id+"'>Error: " +
                err.code + ", Message: " + err.message +
                (err.file ? ", File: " +
                err.file.name : "") + "</div>" );
            $("#err_"+err.file.id).remove();
            setTimeout("remove_rows('"+err.file.id+"')",1000);
            uploader.removeFile(err.file);
            up.refresh(); // Reposition Flash/Silverlight
        });
        // -------------Retrieve uploaded files----------------
        uploader.bind('FileUploaded', function(up, file) {
            var thumb = $("#thumb_"+file.id);
            //Get last uploaded file
            var url = "%s";
            $.ajax({
                url: url,
                type: "get",
                success: function(latest_file){
                    thumb.html("<div class='upfile'>" +
                    "<img src='%simages/file_icon.png'/>" +
                    "<a href='#' class='del_file' rel='" +
                    latest_file +
                    "'>delete file</a></div>").removeClass('hidden');
                    //creates a link to the file,
                    //replace 'media folder' with the dir where you
                    //are going to upload the files
                    //you can use this url to show an image, if you uploaded one
                    thumb.prepend('<span class="file_name">'+
                    '<a href="%s'+latest_file+'">'+
                    file.name+'</a></span>');
                }
            });

            $("#"+file.id).remove(); //remove the file from the upload list
            thumbs_cont.find("#loader").remove();
            $("#pickfiles").show();
            $("#legend_upload_img").hide();
            $("#uploadfiles").hide();
            $("#uploadfiles_table").show();
        });
        $(".del_file").live("click", function(e){
            e.preventDefault();
            var latest_file = $(this).attr("rel");
            delete_file(latest_file, $(this).parent().parent());
        });
    });
    function remove_rows(id){
        $("div#"+id).remove();
    }
    //-------------------------------------------------------------------------
    //  deletes the selected image from the form AND from the server
    //-------------------------------------------------------------------------
    function delete_file(file, thumb_container){
        //then again, change the url to meet your needs
        var url="%s?file="+file;
        $.ajax({
            url: url,
            type: "get",
            success: function(data){
                if(data == 1){
                    thumb_container.remove();
                }else{
                    thumb_container.append("<span class='notice'>"+
                    "Cannot Delete File</span>")
                }
            }
        });

    }
    //-------------------------------------------------------------------------
    //  Retrieve the files currently in the media folder
    //-------------------------------------------------------------------------
    function get_existent_files(){
        var url="%s";
        $.ajax({
            url: url,
            type: "get",
            success: function(data){
                if(data.length > 0){
                    data.forEach(function(file){
                        var thumb = '<div id="thumb_'+file.name+
                        '" class="thumb_container">'+
                        '<span class="file_name">'+
                        '<a href="%s' + file.filename + '">' +
                        file.filename +
                        '</a></span>'+
                        '<div class="upfile">'+
                        '<img src="/static/images/file_icon.png">'+
                        '<a href="#" class="del_file" rel="'+file.filename +
                        '">delete file</a></div></div>';
                        $("#thumbs_cont").show().append(thumb);
                    });
                }
            }
        });
    }

    </script>""" % (settings.STATIC_URL, settings.STATIC_URL,
                    self.upload_url,
                    self.csrf_token.resolve(context),
                    settings.STATIC_URL, settings.STATIC_URL,
                    settings.STATIC_URL, self.url_get_last.resolve(context),
                    settings.STATIC_URL, self.media_folder.resolve(context),
                    self.delete_file_url.resolve(context),
                    self.all_files_url.resolve(context),
                    self.media_folder.resolve(context))


def plupload_script_custom(parser, token):
    parameters = token.split_contents()
    csrf_token_form = parameters[1]
    upload_url = parameters[2]
    url_get_last = parameters[3]
    delete_file_url = parameters[4]
    media_folder = parameters[5]
    all_files_url = parameters[6]
    return CustomPluploadScript(csrf_token_form, upload_url, url_get_last,
                                delete_file_url, media_folder, all_files_url)

register.tag("plupload_script_custom", plupload_script_custom)


class PluploadFormCustomQueue(template.Node):

    def render(self, context):
        return """
        <div id="uploader_cont">
            <div id="table_cont">
            <div id="filelist" class="hidden">
                <div id="table_header">
                <span id="head_archivo">File</span>
                <span id="head_size">File Size</span>
                <span id="head_progress">Progress</span>
                </div>

            </div>
            <div id="upload_buttons">
                <button id="uploadfiles_table" class="default_button_upload hidden">Upload Files</button>
                <button id="pickfiles" class="default_button_upload">Select Files</button>
            </div>
            </div>
            <div id="thumbs_cont"  class="thumbs hidden">
            </div>
        </div>
        """


def pl_upload_form_custom_queue(parser, token):
    return PluploadFormCustomQueue()

register.tag("pl_upload_form_custom_queue", pl_upload_form_custom_queue)