var create_uploader = function(params) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var path = params['path'];

    var uploader = new plupload.Uploader({
        browse_button: 'pickfiles',
        // TODO: Customize runtimes
        runtimes : 'html5,gears,silverlight',

        url : params['url'],
        max_file_size : params['max_file_size'],
        chunk_size : params['chunk_size'],
        unique_names : false,
        multipart_params: {"csrfmiddlewaretoken" : csrf_token },

        filters : [
            {title : "Image files", extensions : "jpg,gif,png"},
            {title : "Zip files", extensions : "zip"}
        ],

        // Silverlight settings
        silverlight_xap_url : params['STATIC_URL'] + 'js/Moxie.xap',

        init: {
            FileUploaded: function(up, file, info) {
                $('#' + params['id']).val(path + "/" + file.name);
            },
            PostInit: function() {
		document.getElementById('filelist').innerHTML = '';

		document.getElementById('uploadfiles').onclick = function() {
		    uploader.start();
		    return false;
		};
	    },
	    FilesAdded: function(up, files) {
		plupload.each(files, function(file) {
		    document.getElementById('filelist').innerHTML += '<div id="' + file.id + '">' + file.name + ' (' + plupload.formatSize(file.size) + ') <b></b></div>';
		});
	    },

	    UploadProgress: function(up, file) {
		document.getElementById(file.id).getElementsByTagName('b')[0].innerHTML = '<span>' + file.percent + "%</span>";
	    },

	    Error: function(up, err) {
		document.getElementById('console').appendChild(document.createTextNode("\nError #" + err.code + ": " + err.message));
	    }

        }
    });

    uploader.init();
}
