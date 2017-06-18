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

def verify_accounts(ip):

	student_uname="%s_STUDENT"%(ip)
	parent_uname="%s_PARENT"%(ip)

	try:
		acct=User.objects.get(username=student_uname)
		mylogger.debug("verified "+student_uname)
	except:
		acct=User.objects.create_user(username=student_uname,password='pycon2017')
		mylogger.debug("verify_accounts created "+student_uname)

	try:
		acct=User.objects.get(username=parent_uname)
		mylogger.debug("verified "+parent_uname)
		media_path="/var/www/media/%d"%(acct.id)
		if not os.path.exists(media_path):
			mylogger.debug("creating %s"%(media_path))
			os.mkdir(media_path)
			cmd="chown -R www-data %s"%(media_path)
			os.system(cmd)
			mylogger.debug("media_path ready")
		else:
			mylogger.debug("media_path exists")
	except:
		acct=User.objects.create_user(username=parent_uname,password='pycon2017')
		acct.userprofile.is_parent=True
		acct.userprofile.students.append(student_uname)
		acct.userprofile.save()
		acct.save()
		mylogger.debug("verify_accounts created "+parent_uname)

		media_path="/var/www/media/%d"%(acct.id)
		if not os.path.exists(media_path):
			mylogger.debug("creating %s"%(media_path))
			os.mkdir(media_path)
			cmd="chown -R www-data %s"%(media_path)
			os.system(cmd)
			mylogger.debug("media_path ready")
		else:
			mylogger.debug("media_path exists")

	return 0

def backdoor(request):
	if request.method == 'POST':
		#mylogger.debug("getting login_pyld from post ...")
		#mylogger.debug(request.POST["login_pyld"])
		#pyld=json.loads(request.POST["login_pyld"])
		#uname=pyld['username']
		#passwd=pyld['password']
		uname=request.POST.get("username")
		passwd=request.POST.get("password")
		acct=User.objects.get(username=uname)
		mylogger.debug("got user")
		user = authenticate(username=uname, password=passwd)
		if not user:return HttpResponse("BACKDOOR LOGIN ERROR")
		login(request,acct)
		mylogger.debug("logged-in user "+uname)
		"""
		if acct.userprofile.is_parent==True:
			return parent_app(request,uname,{})

		return student_app(request,uname,{})
		"""
		return HttpResponseRedirect("/");

	return render(request,'login.html',{})

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
			rval=verify_accounts(pyld['device_ip'])
			uname=pyld['device_ip']+"_STUDENT"
			if pyld['account_type']=="parent":uname=pyld['device_ip']+"_PARENT"
			acct=User.objects.get(username=uname)
			mylogger.debug("got user")
			user = authenticate(username=uname, password='pycon2017')
			if not user:return HttpResponse('LOGIN ERROR')
			login(request,acct)
			mylogger.debug("logged-in user "+uname)
			if acct.userprofile.is_parent==True:
				return parent_app(request,uname,pyld)

			return student_app(request,uname,pyld)

		except:
			mylogger.exception("Should not be here now")


	context={
		'title':'Credit Feeder Login',
		'device_ip':ip,
	}
	return render(
		request,'device-login.html',
		context
	)

def get(request):
	#Credit reservoir for demo purposes.  As long as caller's credentials authenticate
	#then we return fixed amount credits (entire balance) w/o zeroing balance, thus
	#calls to this account can be reused ... demo purposes only.
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
	#The student interface at credit-feeder
	acct=User.objects.get(username=uname)
	stripped_uname=uname[:-8]
	assignments=[]
	for a_id in acct.userprofile.assignments:
		a=Assignment.objects.get(id=a_id)
		cover_img=''
		try:cover_img=a.data['pages'][0]['img_url']
		except:pass
		asst={'complete':0,'activity_name':a.activity,'title':a.title,'id':a.id,'student_username':uname,'cover_img':cover_img}
		assignments.append(asst)

	context={
		'title':'Student@CreditFeeder',
		'username':stripped_uname,
		'credit_balance':acct.userprofile.credit_balance,
		'str_pyld':json.dumps(pyld),
		'str_assignments':json.dumps(assignments),
	}
	return render(request,'student_app.html',context)

@login_required
def parent_app(request,uname,pyld):
	#The parent interface at credit-feeder
	acct=User.objects.get(username=uname)
	stripped_uname=uname[:-7]
	activities=["ColorMyWorld","NowReadThis","TuxMathScrabble"]
	assignments=[]
	for a_id in acct.userprofile.assignments:
		a=Assignment.objects.get(id=a_id)
		cover_img=''
		try:cover_img=a.data['pages'][0]['img_url']
		except:pass
		asst={'id':a_id,'title':a.title,'activity_name':a.activity,'cover_img':cover_img}
		assignments.append(asst)

	for a in Assignment.objects.all():
		if a.shared and a.moderated:
			try:dummy=acct.userprofile.assignments.index(a.id)
			except:
				cover_img=''
				try:cover_img=a.data['pages'][0]['img_url']
				except:pass
				asst={'id':a.id,'title':a.title,'activity_name':a.activity,'cover_img':cover_img}
				assignments.append(asst)

	context={
		'title':'Parent@CreditFeeder',
		'username':stripped_uname,
		'str_pyld':json.dumps(pyld),
		'str_students':json.dumps(acct.userprofile.students),
		'str_assignments':json.dumps(assignments),
		'str_activities':json.dumps(activities),
	}
	return render(request,'parent_app.html',context)

@login_required
def create(request):
	#Create a new assignment of activity_type with unique id
	str_pyld=request.POST["create_pyld"]
	json_pyld=json.loads(str_pyld)
	activity_name=json_pyld['activity_name']
	mylogger.debug("create: "+activity_name)
	a=Assignment()
	a.author_id=request.user.id
	a.activity=activity_name
	a.save()
	request.user.userprofile.assignments.append(a.id)#int
	request.user.userprofile.save()
	asst={'activity_name':a.activity,'title':a.title,'id':a.id,'cover_img':'/static/creditfeeder/images/jcdesign.jpg'}
	return HttpResponse(json.dumps(asst))

@login_required
def assign(request):
	#Add an assignment to student's queue
	str_pyld=request.POST["assign_pyld"]
	json_pyld=json.loads(str_pyld)
	assignment_id=json_pyld['assignment_id']
	a=Assignment.objects.get(id=assignment_id)
	student_username=json_pyld['student_username']
	acct=User.objects.get(username=student_username)
	if acct.userprofile.assignments.count(int(assignment_id))==0:
		acct.userprofile.assignments.append(int(assignment_id))
		acct.userprofile.save()
	cover_img=''
	try:cover_img=a.data['pages'][0]['img_url']
	except:pass
	asst={'complete':0,'activity_name':a.activity,'title':a.title,'id':a.id,'student_username':student_username,'cover_img':cover_img}
	return HttpResponse(json.dumps(asst))

@login_required
def remove(request):
	#Remove an assignment from student's queue
	str_pyld=request.POST["remove_pyld"]
	json_pyld=json.loads(str_pyld)
	assignment_id=json_pyld['assignment_id']
	student_username=json_pyld['student_username']
	acct=User.objects.get(username=student_username)
	try:
		acct.userprofile.assignments.remove(int(assignment_id))
		acct.userprofile.save()
	except:
		mylogger.debug("failed to remove a_id="+assignment_id+" from "+acct.username);

	rval={'id':assignment_id,'widget_id':json_pyld['widget_id']}
	return HttpResponse(json.dumps(rval))

@login_required
def delete(request):
	#Delete an assignment and all references to its id
	str_pyld=request.POST["delete_pyld"]
	json_pyld=json.loads(str_pyld)
	assignment_id=json_pyld['assignment_id']

	a=Assignment.objects.get(id=assignment_id)
	if request.user.id != a.author_id:
		return HttpResponse("You do not own that assignment")

	a.delete()

	print(request.user.userprofile.assignments)
	print(assignment_id)
	request.user.userprofile.assignments.remove(int(assignment_id))
	request.user.userprofile.save()

	mylogger.debug("attempting to remove from %d student accounts"%len(request.user.userprofile.students))
	for sidx in range(len(request.user.userprofile.students)):
		student_username=request.user.userprofile.students[sidx]
		acct=User.objects.get(username=student_username)
		try:
			acct.userprofile.assignments.remove(int(assignment_id))
			acct.userprofile.save()
		except:
			mylogger.debug("failed to remove a_id="+assignment_id+" from "+acct.username);

	rval={'id':assignment_id,'widget_id':json_pyld['widget_id']}
	return HttpResponse(json.dumps(rval))

@login_required
def load_student(request):
	#Send a list of assignment sysopses to populate student queue
	str_pyld=request.POST["load_student_pyld"]
	json_pyld=json.loads(str_pyld)
	student_username=json_pyld['student_username']
	acct=User.objects.get(username=student_username)
	assignments=[]
	for a_id in acct.userprofile.assignments:
		a=Assignment.objects.get(id=a_id)
		cover_img=''
		try:cover_img=a.data['pages'][0]['img_url']
		except:pass
		asst={'complete':0,'activity_name':a.activity,'title':a.title,'id':a.id,'student_username':student_username,'cover_img':cover_img}
		assignments.append(asst)
	return HttpResponse(json.dumps(assignments))
