# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test

import os,logging,time,json,sys
import xmlrpc.client
from creditfeeder.models import *

FORMAT = 'VIEW: %(message)s'

RLOG_FULL_PATH='/var/www/feeder/creditfeeder/feeder.log'
logging.basicConfig(filename=RLOG_FULL_PATH,level=logging.DEBUG, format=FORMAT)
mylogger=logging

def nrt_config(request):
	context={
		'title':'NRT CONFIG',
	}
	return render(request,'nrt_editor.html',context)


def nrt_test(request):
	context={
		'title':'NRT TEST',
	}
	return render(request,'nrt_assignment.html',context)
