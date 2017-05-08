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

def logout_view(request):
    logging.debug("logout_view")
    empty_session_id=logout(request)
    logging.debug("empty_session_id: %s"%empty_session_id)
    request.session.delete()
    return HttpResponseRedirect("/")

def home(request):
	logging.debug("home");
	if request.user.is_authenticated():
		logging.debug("already authenticated:"+request.user.username)
		if request.user.userprofile.is_parent==True:
			return parent_app(request,request.user.username,{})
		return student_app(request,request.user.username,{})

	ip=request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR')
	logging.debug("not authenticated: %s"%(ip))
	if request.method == 'POST':
		mylogger.debug("getting login_pyld from post ...")
		mylogger.debug(request.POST["login_pyld"])
		pyld=json.loads(request.POST["login_pyld"])
		uname=None
		acct=None
		try:
			uname=pyld['device_ip']+"_STUDENT"
			if pyld['account_type']=="parent":uname=pyld['device_ip']+"_PARENT"
			acct=User.objects.get(username=uname)
			mylogger.debug("got user")
			login(request,acct)
			mylogger.debug("logged-in user "+uname)

		except:
			mylogger.debug("creating new account ...")
			uname=pyld['device_ip']+"_STUDENT"
			if pyld["account_type"]=="parent":uname=pyld['device_ip']+"_PARENT"
			acct=User.objects.create_user(username=uname,password='pycon2017')
			acct.userprofile.is_parent=False
			if pyld["account_type"]=="parent":acct.userprofile.is_parent=True
			default_student=pyld['device_ip']+"_STUDENT"
			acct.userprofile.students.append(default_student)
			acct.userprofile.save()
			acct.save()

			mylogger.debug("logging-in "+uname)
			login(request,acct)

		if acct.userprofile.is_parent==True:
			return parent_app(request,uname,pyld)

		return student_app(request,uname,pyld)

	context={
		'title':'Credit Feeder Login',
		'device_ip':ip,
	}
	return render(
		request,'device-login.html',
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
def student_app(request,uname,pyld):
	acct=User.objects.get(username=uname)
	context={
		'title':'Student@CreditFeeder',
		'username':uname,
		'credit_balance':acct.userprofile.credit_balance,
		'json_pyld':json.dumps(pyld),
		'json_assignments':json.dumps(acct.userprofile.assignments),
	}
	return render(request,'student_app.html',context)

@login_required
def parent_app(request,uname,pyld):
	acct=User.objects.get(username=uname)
	activities=["ColorMyWorld","NowReadThis","TuxMathScrabble"]
	assignments=[]
	for a_id in acct.userprofile.assignments:
		a=Assignment.objects.get(id=a_id)
		asst={'id':a_id,'title':a.title,'activity_name':a.activity}
		assignments.append(asst)

	context={
		'title':'Parent@CreditFeeder',
		'username':uname,
		'str_pyld':json.dumps(pyld),
		'str_students':json.dumps(acct.userprofile.students),
		'str_assignments':json.dumps(assignments),
		'str_activities':json.dumps(activities),
	}
	return render(request,'parent_app.html',context)

@login_required
def create(request):
	str_pyld=request.POST["create_pyld"]
	json_pyld=json.loads(str_pyld)
	activity_name=json_pyld['activity_name']
	mylogger.debug("create: "+activity_name)
	a=Assignment()
	a.author_id=request.user.id
	a.activity=activity_name
	a.save()
	request.user.userprofile.assignments.append(a.id)
	request.user.userprofile.save()
	asst={'activity_name':activity_name,'title':'NewAssignment','id':a.id,}
	return HttpResponse(json.dumps(asst))

@login_required
def assign(request):
	str_pyld=request.POST["assign_pyld"]
	json_pyld=json.loads(str_pyld)
	assignment_id=json_pyld['assignment_id']
	a=Assignment.objects.get(id=assignment_id)
	student_username=json_pyld['student_username']
	acct=User.objects.get(username=student_username)
	acct.userprofile.assignments.append(assignment_id)
	acct.userprofile.save()
	asst={'complete':0,'activity_name':a.activity,'title':a.title,'id':a.id,'student_username':student_username,}
	return HttpResponse(json.dumps(asst))

@login_required
def remove(request):
	str_pyld=request.POST["remove_pyld"]
	json_pyld=json.loads(str_pyld)
	assignment_id=json_pyld['assignment_id']
	a=Assignment.objects.get(id=assignment_id)
	student_username=json_pyld['student_username']
	acct=User.objects.get(username=student_username)
	acct.userprofile.assignments.remove(assignment_id)
	acct.userprofile.save()
	return HttpResponse("Assignmet Removed")

@login_required
def load_student(request):
	str_pyld=request.POST["load_student_pyld"]
	json_pyld=json.loads(str_pyld)
	student_username=json_pyld['student_username']
	acct=User.objects.get(username=student_username)
	assignments=[]
	for a_id in acct.userprofile.assignments:
		a=Assignment.objects.get(id=a_id)
		asst={'complete':0,'activity_name':a.activity,'title':a.title,'id':a.id,'student_username':student_username,}
		assignments.append(asst)
	return HttpResponse(json.dumps(assignments))
