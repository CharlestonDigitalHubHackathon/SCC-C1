from django.shortcuts import render

# Create your views here.


from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth import logout
# default user table

# for forgot password feature
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail

from django.contrib.auth.models import User

# import the models
from .models import AirPollutionRecords
# use this function for returning json data on ajax requests
import json

# for ajax requests, returning JSON to JS
def render_to_json_response(context, **response_kwargs):
    data = json.dumps(context)
    response_kwargs['content_type'] = 'application/json'
    return HttpResponse(data, **response_kwargs)


# home page function
@csrf_exempt
def index(request):

    # qslist = Table.objects.all()
    # context = {'qs':qslist}

    template = loader.get_template('main/home_admin.html')

    allyears = {}
    for year in range(1990, 2018):
        allyears[year] = AirPollutionRecords.ordered_by_year(year)

    if request.is_ajax():
        year = int(request.POST.get('year'))
        mylist = AirPollutionRecords.ordered_by_year(year)
        retmylist = [MyObj(_cbsa_name=el.cbsa_name,_arith_mean=el.arithmetic_mean,_units_of_measure=el.units_of_measure, _param_name=el.parameter_name).toJSON() for el in mylist]
        data = {'mylist': retmylist}
        return render_to_json_response(data)

    #context = {'allyears': allyears}
    #allyears = [i for i in range(1990, 2018)]
    context= { 'allyears':allyears}

    return HttpResponse(template.render(context, request))

# 404 page
@csrf_exempt
def err404(request):
    template = loader.get_template('main/404.html')
    context = {
        '': '',
    }
    return HttpResponse(template.render(context, request))




# use this json serialization function particularly for objects with dates as fields
def json_default(value):
    if isinstance(value, datetime.datetime):
        return dict(year=value.year, month=value.month, day=value.day, hour=value.hour,min=value.minute,sec=value.second)

    elif isinstance(value, datetime.date):
        return dict(year=value.year,month=value.month,day=value.day)

    elif isinstance(value,datetime.time):
        value = value.strftime("%I:%M")
        print("value 1: ",value)
        value = datetime.datetime.strptime(value, "%H:%M")
        print("value2:",value)
        return dict(hour=value.hour,min=value.minute)

    else:
        return value.__dict__


class MyObj:
    def __init__(self,_cbsa_name,_param_name,_units_of_measure,_arith_mean):
        self.cbsa_name = _cbsa_name
        self.parameter_name = _param_name
        self.units_of_measure = _units_of_measure
        self.arithmetic_mean = _arith_mean
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)