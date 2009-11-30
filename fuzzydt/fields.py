from django import forms
from django.utils.translation import ugettext_lazy as _
from fuzzydt.widgets import *
from parsedatetime.parsedatetime import Calendar
import datetime

# These values, if given to to_python(), will trigger the self.required check.
EMPTY_VALUES = (None, '')

class FuzzyDateField(forms.Field):
    #widget = FuzzyDateInput
    default_error_messages = {
        'invalid': _(u'Enter a valid date.'),
    }

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.widget = FuzzyDateInput(url=url)
        super(FuzzyDateField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        """
        Validates that the input can be converted to a date. Returns a Python
        datetime.date object.
        """
        super(FuzzyDateField, self).clean(value)
        if value in EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        c = Calendar()
        parsed = c.parse(value)
        if parsed[1] == 1:
            return datetime.date(*parsed[0][:3])
        raise ValidationError(self.error_messages['invalid'])

class FuzzyTimeField(forms.Field):
    #widget = FuzzyTimeInput
    default_error_messages = {
        'invalid': _(u'Enter a valid time.')
    }

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.widget = FuzzyTimeInput(url=url)
        super(FuzzyTimeField, self).__init__(*args, **kwargs)


    def clean(self, value):
        """
        Validates that the input can be converted to a time. Returns a Python
        datetime.time object.
        """
        super(FuzzyTimeField, self).clean(value)
        if value in EMPTY_VALUES:
            return None
        if isinstance(value, datetime.time):
            return value
        
        c = Calendar()
        parsed = c.parse(value)
        if parsed[1] == 2:
            return datetime.time(*parsed[0][3:6])
        raise ValidationError(self.error_messages['invalid'])

class FuzzyDateTimeField(forms.Field):
    #widget = FuzzyDateTimeInput
    default_error_messages = {
        'invalid': _(u'Enter a valid date/time.'),
    }

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.widget = FuzzyDateTimeInput(url=url)
        super(FuzzyDateTimeField, self).__init__(*args, **kwargs)
    
    def clean(self, value):
        """
        Validates that the input can be converted to a datetime. Returns a
        Python datetime.datetime object.
        """
        super(DateTimeField, self).clean(value)
        if value in EMPTY_VALUES:
            return None
        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            return datetime.datetime(value.year, value.month, value.day)
        if isinstance(value, list):
            # Input comes from a SplitDateTimeWidget, for example. So, it's two
            # components: date and time.
            if len(value) != 2:
                raise ValidationError(self.error_messages['invalid'])
            value = '%s %s' % tuple(value)
        
        c = Calendar()
        parsed = c.parse(value)
        if parsed[1] == 3:
            return datetime.date(*parsed[0][:6])
        raise ValidationError(self.error_messages['invalid'])

class SplitFuzzyDateTimeField(forms.MultiValueField):
    #widget = SplitFuzzyDateTimeWidget
    hidden_widget = forms.widgets.SplitHiddenDateTimeWidget
    default_error_messages = {
        'invalid_date': _(u'Enter a valid date.'),
        'invalid_time': _(u'Enter a valid time.'),
    }

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.widget = SplitFuzzyDateTimeWidget(url=url)
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        fields = (
            FuzzyDateField(url=url, error_messages={'invalid': errors['invalid_date']}),
            FuzzyTimeField(url=url, error_messages={'invalid': errors['invalid_time']}),
        )

        super(SplitFuzzyDateTimeField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            # Raise a validation error if time or date is empty
            # (possible if SplitDateTimeField has required=False).
            if data_list[0] in EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_date'])
            if data_list[1] in EMPTY_VALUES:
                raise ValidationError(self.error_messages['invalid_time'])
            return datetime.datetime.combine(*data_list)
        return None
