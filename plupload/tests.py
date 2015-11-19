from django.test import TestCase

from plupload.forms import PlUploadFormField
from plupload.widgets import PlUploadWidget

class TestPluploadWidgetOptions(TestCase):
    """ Make sure Plupload options are handled correctly

    PlUpload options are defined here:

      http://www.plupload.com/docs/Options
    """

    def test_all_params_are_passed_to_js_widget(self):
        """ Make sure that all the options given to the
        FormField are passed to the resulting javascript widget

        This does not test that the javascript widget is rendered
        correctly.
        """

        widget_options = {
            'browse_button': 'test_button',
            'url': 'upload_url',
            'filters': {
                'mime_types': [
                    {
                        'title': "Image files",
                        'extensions': "jpg,gif,png"},
                    {
                        'title': "Zip files",
                        'extensions': "zip"
                    }
                ],
                'max_file_size': 0,
                'prevent_duplicates': 'true',
            },
            'headers': {
                'my_header': 'my_value'
            },
            'multipart_params': {
                'one': 'two',
            },
            'max_retries': 0,
            'chunk_size': '1mb',
            'resize': {'width': '100px'},
            'drop_element': 'false',
            'multi_selection': 'false',
            'required_features': 'html5',
            'unique_names': 'false',
            'runtimes': 'html5',
            'file_data_name': "file",
            'container': 'container',
            'flash_swf_url': "js/Movie.swf",
            'silverlight_xap_url': 'js/Movie.xap',
        }

        form_field = PlUploadFormField(
            path='dummy_path',
            options=widget_options,
        )

        # Assert that all keys are passed to the widget
        for key in widget_options.keys():
            self.assertTrue(
                key in form_field.widget.widget_options.keys()
            )
