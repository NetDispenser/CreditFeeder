# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test

import os,logging,time,json,sys
import xmlrpc.client

FORMAT = 'VIEW: %(message)s'

RLOG_FULL_PATH='/var/www/feeder/creditfeeder/feeder.log'
logging.basicConfig(filename=RLOG_FULL_PATH,level=logging.DEBUG, format=FORMAT)

def home(request):
    logging.debug("home");
    if request.user.is_authenticated():
        logging.debug("already authenticated:"+request.user.username)
        return app(request)
    else:
        ip=request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
        logging.debug("not authenticated: %s"%(ip))
        if request.method == 'POST':
            logging.debug("login POST")
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user!=None:
                logging.debug("logging in user")
                login(request, user)
                return app(request)

        context={'title':'Login','button_text':'Login'}
        return render(
                request,'login.html',
                context
        )

def get(request):
	progress=0
	try:
		logging.debug("get request")
		logging.debug(request)
		qs=request.META['QUERY_STRING']
		logging.debug(qs)
		if len(qs)>1:
			logging.debug(qs)
			split_qs=qs.split("&")
			action=split_qs[0].split('=')[1]
			u=split_qs[1].split('=')[1]
			p=split_qs[2].split('=')[1]
			user = authenticate(username=u, password=p)
			if user!=None:return HttpResponse(user.userprofile.credit_balance)
			else:return HttpResponse('Login Failed')
	except:
		return HttpResponse('Exception')
	return HttpResponse('What Happened?');


@login_required
def app(request):
        context={
                'title':'CreditFeeder',
                'username':request.user.username,
                'is_parent':request.user.userprofile.is_parent,
                'credit_balance':request.user.userprofile.credit_balance,
        }
        return render(request,'creditfeeder.html',context)

