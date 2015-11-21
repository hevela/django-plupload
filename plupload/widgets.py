from os import path

from django.forms.widgets import Input
from django.utils.safestring import mark_safe
from django.template.loader import get_template
from django.conf import settings
from django.template.context_processors import csrf
from django.forms.util import flatatt
from django.core.urlresolvers import reverse

import json


class PlUploadWidget(Input):

    needs_multipart_form = True
    input_type = 'text'

    def __init__(self, attrs=None, widget_options=None):
        self.widget_options = widget_options

        if widget_options is None:
            self.widget_options = {}

        return super().__init__(
            attrs=attrs
        )

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        template = get_template(
            "plupload_widget.html"
        )

        upload_rel_path = path.relpath(
            settings.UPLOAD_ROOT,
            settings.MEDIA_ROOT
        )

        self.widget_options.update({
            'STATIC_URL': settings.STATIC_URL,
            'id': final_attrs['id'],
            'url': reverse('plupload:upload_file'),
            'path': upload_rel_path
        })

        options = {
            'STATIC_URL': settings.STATIC_URL,
            'id': final_attrs['id'],
            'csrf_token': csrf(name),
            'final_attrs': flatatt(final_attrs),
            'json_params': mark_safe(json.dumps(self.widget_options))
        }

        return mark_safe(
            template.render(
                options,
            )
        )
