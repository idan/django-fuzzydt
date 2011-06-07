import datetime
from parsedatetime.parsedatetime import Calendar

from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson as json
from django.utils.dateformat import format

def fuzzydtparse(request):
    """
    Attempts to parse a natural-language date/time string and return a
    formatted representation of the parsed date/time.

    The returned representations are formatted using django's php-style
    datetime formatting facilities. See
    http://docs.djangoproject.com/en/dev/ref/templates/builtins/#now for a
    full specification

    GET/POST arguments:
    dtstring *(required)*
        The natural-language date and/or time string to parse.

    dateformat (optional)
        A format specifier string used to format the returned representation
        if it is determined to be a date instance. The default format is
        'l, F jS Y', which produces values like 'Thursday, October 1st 2009'.

    timeformat (optional)
        A format specifier string used to format the returned representation
        if it is determined to be a time instance. The default format is
        'P', which produces values like '6:26 p.m.'.

    dtformat (optional)
        A format specifier string used to format the returned representation
        if it is determined to be a datetime instance. The default format is
        'l, F jS Y, P', which produces values like
        'Thursday, October 1st 2009, 6:26 p.m.'.

    require (optional)
        One of 'date', 'time', 'datetime'. If the parsed value is not of the
        specified type, the view will return 400/Bad Request

    callback (optional)
        JSONP callback.

    Returns a json dictionary containing two values:
    type
        An string indicating the kind of representation returned.
        One of 'date', 'time', or 'datetime'

    parsed
        A string representation of the parsed datetime.

    Invalid / unparsable datetimes will return 400/Bad Request.

    """
    try:
        dtstring = request.REQUEST['dtstring']
    except KeyError:
        return HttpResponseBadRequest()


    kind = {
        'date': 1,
        'time': 2,
        'datetime': 3
    }

    dateformat = request.REQUEST.get('dateformat', 'l, F jS Y' )
    timeformat = request.REQUEST.get('timeformat', 'P')
    dtformat = request.REQUEST.get('dtformat', 'l, F jS Y, P')
    require = request.REQUEST.get('require', None)
    callback = request.REQUEST.get('callback', None)

    if require and require not in kind:
        return HttpResponseBadRequest()

    c = Calendar()

    # TODO: possible security hole?
    parsed = c.parse(dtstring)
    if parsed[1] == 0:
        return HttpResponseBadRequest()
    parsed_dt = datetime.datetime(*parsed[0][:6])
    response_dict = {}
    if require and parsed[1] != kind[require]:
        return HttpResponseBadRequest()
    try:
        if parsed[1] == 1:
            response_dict['type'] = 'date'
            response_dict['parsed'] = format(parsed_dt, dateformat)
        elif parsed[1] == 2:
            response_dict['type'] = 'time'
            response_dict['parsed'] = format(parsed_dt, timeformat)
        elif parsed[1] == 3:
            response_dict['type'] = 'datetime'
            response_dict['parsed'] = format(parsed_dt, dtformat)
        else:
            #should never be here
            return HttpResponseBadRequest()
    except:
        return HttpResponseBadRequest()

    if callback:
        resp = "%s(%s)" % (callback, json.dumps(response_dict))
    else:
        resp = json.dumps(response_dict)
    return HttpResponse(resp, mimetype='application/javascript')
