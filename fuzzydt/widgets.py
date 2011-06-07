import datetime

from django.forms.widgets import Input, MultiWidget
from django.utils.safestring import mark_safe
from django.utils.dateformat import format, time_format

fuzzy_dtinput_template = u'''<div id="parsed_%(name)s" class="fuzzy_dtinput_parsed">%(tip)s</div><br clear="all">
<script type="text/javascript">
    var oldval_%(name)s = '';
    var origval_%(name)s = $("#id_%(name)s").val();
    function remote_validate_%(name)s() {
        // performs the actual remote validation call
        var raw = $("#id_%(name)s").val();
        if (raw == '') {
            $('#id_%(name)s').removeClass('annotated')
            $('#parsed_%(name)s').html('%(tip)s').attr('class', 'fuzzy_dtinput_parsed');
        } else if (oldval_%(name)s != raw) {
            oldval_%(name)s = raw;
            $.ajax({
                'url': '%(url)s',
                'data': {
                    'dtstring': raw,
                    'timeformat': '%(previewformat)s',
                    'require': '%(require)s',
                 },
                'dataType': 'json',
                'timeout': 2000,
                'error': function(XMLHttpRequest, textStatus, errorThrown) {
                    $('#id_%(name)s').addClass('annotated')
                    $('#parsed_%(name)s').html('%(tip)s').attr('class', 'fuzzy_dtinput_error');
                },
                'success': function(json) {
                    $('#id_%(name)s').addClass('annotated')
                    $("#parsed_%(name)s").text(json.parsed).attr('class', 'fuzzy_dtinput_ok');
                }
            });
        }
    }
    // validate the initial contents of the field before labelify
    if (origval_%(name)s != '') {
        $('#id_%(name)s').removeClass('annotated');
        $('#parsed_%(name)s').html('').attr('class', 'fuzzy_dtinput_working');
        remote_validate_%(name)s();
    }
    $('#id_%(name)s').labelify({labelledClass: 'fuzzy_dtinput_label'});
    $("#id_%(name)s").keyup(function(e) {
        if (oldval_%(name)s != $("#id_%(name)s").val()) {
            $('#id_%(name)s').removeClass('annotated')
            $('#parsed_%(name)s').html('').attr('class', 'fuzzy_dtinput_working');
        }
    });
    $("#id_%(name)s").keyup($.debounce(function(e) {
        remote_validate_%(name)s();
    }, 500));
</script>
'''


class FuzzyDateInput(Input):
    input_type = 'text'
    format = 'M jS Y' # 'Oct 31st 2009'
    previewformat = 'l, F jS Y' # 'Tuesday, October 31st 2009'
    tip = 'A date, like "Jan 1st 2010" or "next friday".'

    class Media:
        css = {
            'all': ('css/fuzzydt.css',),
        }
        js = ('js/jquery.debounce.js', 'js/jquery.labelify.js')

    def __init__(self, url, attrs=None, format=None, previewformat=None, tip=None):
        if not attrs:
            attrs = {'class': 'natural_dtinput'}
        else:
            if 'class' in attrs:
                attrs['class'] += ' natural_dtinput'
            else:
                attrs['class'] = 'natural_dtinput'
        super(FuzzyDateInput, self).__init__(attrs)
        self.url = url
        if format:
            self.format = format
        if previewformat:
            self.previewformat = previewformat
        if tip:
            self.tip = tip

        self.attrs['title'] = 'Date'

    def _format_value(self, value):
        if value is None:
            return ''
        elif not isinstance(value, datetime.date):
            return value
        else:
            return format(value, self.format)

    def render(self, name, value, attrs=None):
        value = self._format_value(value)
        rendered = super(FuzzyDateInput, self).render(name, value, attrs)
        return rendered + mark_safe(fuzzy_dtinput_template % {
            'name': name,
            'url': self.url,
            'previewformat': self.previewformat,
            'require': 'date',
            'tip': self.tip })

    def _has_changed(self, initial, data):
        return super(FuzzyDateInput, self)._has_changed(self._format_value(initial), data)

class FuzzyTimeInput(Input):
    input_type = 'text'
    format = 'g:i A' # '11:59 PM'
    previewformat = 'g:i A' # '11:59 PM'
    tip = 'a time, like "noon", "10a", or "6:23pm".'

    class Media:
        css = {
            'all': ('css/fuzzydt.css',),
        }
        js = ('js/jquery.debounce.js', 'js/jquery.labelify.js')

    def __init__(self, url, attrs=None, format=None, previewformat=None, tip=None):
        if not attrs:
            attrs = {'class': 'natural_dtinput'}
        else:
            if 'class' in attrs:
                attrs['class'] += ' natural_dtinput'
            else:
                attrs['class'] = 'natural_dtinput'

        super(FuzzyTimeInput, self).__init__(attrs)
        self.url = url
        if format:
            self.format = format
        if previewformat:
            self.previewformat = previewformat
        if tip:
            self.tip = tip

        self.attrs['title'] = 'Time'


    def _format_value(self, value):
        if value is None:
            return ''
        elif not isinstance(value, datetime.time):
            return value
        else:
            return time_format(value, self.format)

    def render(self, name, value, attrs=None):
        value = self._format_value(value)
        rendered = super(FuzzyTimeInput, self).render(name, value, attrs)
        return rendered + mark_safe(fuzzy_dtinput_template % {
            'name': name,
            'url': self.url,
            'previewformat': self.previewformat,
            'require': 'time',
            'tip': self.tip })

    def _has_changed(self, initial, data):
        return super(FuzzyTimeInput, self)._has_changed(self._format_value(initial), data)

class FuzzyDateTimeInput(Input):
    input_type = 'text'
    format = 'M jS Y, g:i A' # 'Oct 31st 2009, 11:59 PM'
    previewformat = 'l, F jS Y, g:i A' # 'Tuesday, October 31st 2009, 11:59 PM'
    tip = 'A date and time like "4 Oct 2009, 11:23p".'
    class Media:
        css = {
            'all': ('css/fuzzydt.css',),
        }
        js = ('js/jquery.debounce.js', 'js/jquery.labelify.js')

    def __init__(self, url, attrs=None, format=None, previewformat=None, tip=None):
        if not attrs:
            attrs = {'class': 'natural_dtinput'}
        else:
            if 'class' in attrs:
                attrs['class'] += ' natural_dtinput'
            else:
                attrs['class'] = 'natural_dtinput'
        super(FuzzyDateTimeInput, self).__init__(attrs)
        self.url = url
        if format:
            self.format = format
        if previewformat:
            self.previewformat = previewformat
        if tip:
            self.tip = tip

        self.attrs['title'] = 'Date and Time'

    def _format_value(self, value):
        if value is None:
            return ''
        else:
            return format(value, self.format)

    def render(self, name, value, attrs=None):
        value = self._format_value(value)
        rendered = super(FuzzyDateTimeInput, self).render(name, value, attrs)
        return rendered + mark_safe(fuzzy_dtinput_template % {
            'name': name,
            'url': self.url,
            'previewformat': self.previewformat,
            'require': 'datetime',
            'tip': self.tip })

    def _has_changed(self, initial, data):
        return super(FuzzyDateTimeInput, self)._has_changed(self._format_value(initial), data)

class SplitFuzzyDateTimeWidget(MultiWidget):
    """
    A Widget that splits datetime input into two <input type="text"> boxes.
    """
    date_format = FuzzyDateInput.format
    date_previewformat = FuzzyDateInput.previewformat
    time_format = FuzzyTimeInput.format
    time_previewformat = FuzzyTimeInput.previewformat

    def __init__(self, url, attrs=None, date_format=None, date_previewformat=None,
                 time_format=None, time_previewformat=None):
        self.url = url
        if date_format:
            self.date_format = date_format
        if date_previewformat:
            self.date_previewformat = date_previewformat
        if time_format:
            self.time_format = time_format
        if time_previewformat:
            self.time_previewformat = time_previewformat

        widgets = (
            FuzzyDateInput(url,
                             attrs=attrs,
                             format=self.date_format,
                             previewformat=self.date_previewformat),
            FuzzyTimeInput(url,
                             attrs=attrs,
                             format=self.time_format,
                             previewformat=self.time_previewformat))
        super(SplitFuzzyDateTimeWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]
