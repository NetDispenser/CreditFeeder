# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test

import os,logging,time,json,sys,string,random
import xmlrpc.client
from creditfeeder.models import *

FORMAT = 'VIEW: %(message)s'

RLOG_FULL_PATH='/var/www/feeder/creditfeeder/feeder.log'
logging.basicConfig(filename=RLOG_FULL_PATH,level=logging.DEBUG, format=FORMAT)
mylogger=logging

def generate_random_string(n):
	mychars=list(string.digits)+list(string.ascii_letters)
	rval=''
	for i in range(n):
		pidx=int(len(mychars)*random.random())
		rval+=mychars[pidx]
	return rval

def nrt_save(request):
	pyld=eval( request.POST.get("pyld") )
	assignment_id=int(pyld['assignment_id'])
	num_pgs=int(pyld['num_pgs'])

	a=Assignment.objects.get(id=assignment_id)
	a.title=request.POST.get("title")
	a.credits=pyld["credits"]
	a.repeatable=pyld["repeatable"]
	a.shared=pyld["shared"]
	if a.shared:a.moderated=1;
	a.save()

	mylogger.debug("save before data")
	pct_replace=pyld['pctreplace']

	data={
		'num_pages':num_pgs,
		'pages':[],
		'pct_replace':pct_replace,
	}
	for pidx in range(num_pgs):

		mylogger.debug("retrieving img_url from POST")
		w="%d_url"%(pidx)
		img_url=request.POST.get(w)

		if img_url=='':
			mylogger.debug("blank img_url ... skipping")
		else:
			mylogger.debug(img_url)

			###########START: IMG DOWNLOAD
			need2download=False
			if img_url.count("http://") > 0:
				mylogger.debug("got on http")
				need2download=True
			elif img_url.split("/")[0].count(".")>0:
				mylogger.debug("got on zeroeth")
				need2download=True
			elif img_url.split("/")[1].count(".")>0:
				mylogger.debug("got on 1st")
				need2download=True
			elif img_url.split("/")[2].count(".")>0:
				mylogger.debug("got on 2nd")
				need2download=True
			else:
				mylogger.debug("need2download remains False")

			if need2download==True:

				mylogger.debug("downloading image ...")

				media_dir="/var/www/media/%d"%request.user.id

				fname=os.path.basename(img_url)

				ext=fname[-3:]
				oufname="%s.%s"%(generate_random_string(10),ext)
				oufpathname=os.path.join(media_dir,oufname)#b/c many img_urls have percent and other chars ...

				cmd="wget -O %s %s"%(oufpathname,img_url)
				mylogger.debug(cmd)
				os.system(cmd)

				img_url="/media/%d/%s"%(request.user.id,oufname)
				mylogger.debug(img_url)

			###########END: IMG DOWNLOAD

		u="%d_paragraph"%(pidx)
		paragraph=request.POST.get(u)
		u="%d_caption"%(pidx)
		caption=request.POST.get(u)
		pg={
			'page_num':str(pidx),
			'img_url':img_url,
			'caption':caption,
			'paragraph':paragraph,
		}

		data['pages'].append(pg)


	if int(pyld['page2delete'])>-1:
		data['pages'].pop(int(pyld['page2delete']))

	a.data=data
	a.save()

	msg="assignment saved"
	mylogger.debug(msg)
	#messages.add_message(request, messages.INFO, msg)

	mylogger.debug(a)
	pctreplace=''
	try:pctreplace=a.data['pct_replace']
	except:pass
	context={
		'title':'Now Read This',
		'user':request.user,
		'author':a.author_id,
		'assignment':a,
		'pctreplace':pctreplace,
		'credits':a.credits,
		'repeatable':a.repeatable,
		'shared':a.shared,
	}
	return render(request,'nrt_editor.html',context)

def nrt_config(request):
	if request.method == 'POST':
		mylogger.debug("POST: nrt_config")
		mylogger.debug(request.POST)
		mylogger.debug(json.dumps(request.POST))
		return nrt_save(request)

	elif request.META['QUERY_STRING']:
		qs=request.META['QUERY_STRING']
		mylogger.debug(qs)
		assignment_id=qs.split("&")[1].split("=")[1].split("_")[1]
		mylogger.debug(assignment_id)
		a=Assignment.objects.get(id=int(assignment_id))
		mylogger.debug(a)
		pctreplace=''
		try:pctreplace=a.data['pct_replace']
		except:pass
		context={
			'title':'Now Read This',
			'user':request.user,
			'author':a.author_id,
			'assignment':a,
			'pctreplace':pctreplace,
			'credits':a.credits,
			'repeatable':a.repeatable,
			'shared':a.shared,
		}
		return render(request,'nrt_editor.html',context)

	context={
		'title':'NRT CONFIG',
	}
	return render(request,'nrt_editor.html',context)


def nrt_test(request):
	qs=request.META['QUERY_STRING']
	mylogger.debug(qs)
	qs_request=qs.split("&")[0].split("=")[1]
	assignment_id=qs.split("&")[1].split("=")[1].split("_")[1]
	mylogger.debug(assignment_id)
	a=Assignment.objects.get(id=int(assignment_id))

	cover_img='/static/creditfeeder/images/jcdesign.jpg'
	try:cover_img=a.data['pages'][0]['img_url']
	except:pass

	context={
		'title':'Assignment In Progress',
		'user':request.user,
		'assignment':a,
		'am_teacher':request.user.userprofile.is_parent,
		'cover_img_url':cover_img,
		#'menu':menu,
		#'base_template':base_template,
	}
	return render(request,'nrt_assignment.html',context)
