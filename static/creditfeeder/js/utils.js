var logout=function(){window.location="/logout"}
var print=function(msg){console.log(msg)}
function get_selected(select_id, whichfield){
	target_select=document.getElementById(select_id);
	for(var oidx=0;oidx<target_select.options.length;oidx++){
		if(target_select.options[oidx].selected==1) {
			if(whichfield==0)return target_select.options[oidx].text;
			return target_select.options[oidx].value;
		}
	}
	return '';
}
function set_selected(select_id,select_text){
	target_select=document.getElementById(select_id);
	for(var oidx=0;oidx<target_select.options.length;oidx++){
		if(target_select.options[oidx].text==select_text)
			target_select.selectedIndex=oidx;
	}
}
var decode=function(str){
	var div = document.createElement('div');
	div.innerHTML = str;
	var decoded=str;
	try{
		decoded = div.firstChild.nodeValue;
	}
	catch(e){;}
	return decoded;
}
var mkHtmlDiv=function(html){
	var rval=document.createElement("div");
	rval.innerHTML=html;
	return rval;
}
var mkStudentSelect=function(a_id,opts){
	var rval=document.createElement("select");
	rval.id="select_student_"+a_id;
	for(var oidx=0;oidx<opts.length;oidx++){
		console.log(oidx);
		console.log("adding: "+opts[oidx].value);
		var opt=document.createElement('option');
		opt.value=opts[oidx].value;
		opt.text=opts[oidx].text;
		rval.append(opt);
	}
	return rval;
}
var mkAssignB=function(a_id){
	var b=document.createElement("button");
	b.id="assign_"+a_id;
	b.innerHTML="Assign";
	b.addEventListener("click",assignCB,false)
	return b;
}
var mkRemoveB=function(a_id){
	var b=document.createElement("button");
	b.id="remove_"+a_id;
	b.innerHTML="Remove";
	b.addEventListener("click",removeCB,false)
	return b;
}
var mkDeleteB=function(a_id){
	var b=document.createElement("button");
	b.id="delete_"+a_id;
	b.innerHTML="Delete";
	b.addEventListener("click",deleteCB,false)
	return b;
}
var mkTestB=function(a_id){
	var b=document.createElement("button");
	b.id="test_"+a_id;
	b.innerHTML="Test";
	b.addEventListener("click",testCB,false)
	return b;
}
var mkEditB=function(a_id){
	var b=document.createElement("button");
	b.id="edit_"+a_id;
	b.innerHTML="Edit";
	b.addEventListener("click",editCB,false)
	return b;
}
var mkEarnB=function(a_id){
	var b=document.createElement("button");
	b.id="earn_"+a_id;
	b.innerHTML="Earn";
	b.addEventListener("click",testCB,false)
	return b;
}

var add_assignment=function(a){
	var t=document.getElementById("assignment_table");
	var r=t.insertRow(-1);
	r.id="assignment_table_row_"+a.id;

	var c=r.insertCell(-1);
	c.appendChild(mkHtmlDiv(a['title']))

	var c=r.insertCell(-1);
	c.appendChild(mkHtmlDiv(a['activity_name']))

	var c=r.insertCell(-1);
	c.appendChild(mkEditB(a.id))

	var c=r.insertCell(-1);
	c.appendChild(mkTestB(a['activity_name']))

	var c=r.insertCell(-1);
	c.appendChild(mkAssignB(a.id))

	var c=r.insertCell(-1);
	var opts=document.getElementById("student_select").childNodes;
	c.appendChild(mkStudentSelect(a.id,opts))

	var c=r.insertCell(-1);
	c.appendChild(mkDeleteB(a.id))

}
var add_assignment_to_student=function(a){//the student_username is included in a (assignment summary)
	console.log("add_assignment_to_student")
	student_username=a['student_username']
	selected_student_username=get_selected("student_select",1)
	if(student_username==selected_student_username){
		var t=document.getElementById("student_assignments");
		var r=t.insertRow(-1);
		r.id="student_assignment_row_"+a.id;

		var c=r.insertCell(-1);
		c.appendChild(mkHtmlDiv(a['title']))

		var c=r.insertCell(-1);
		c.appendChild(mkHtmlDiv(a['activity_name']))

		var c=r.insertCell(-1);
		c.appendChild(mkHtmlDiv(a['complete']))

		var c=r.insertCell(-1);
		c.appendChild(mkRemoveB(a.id))
	}
	else{print('that student not currently loaded')}
}
var testCB=function(e){
	var activity_name=e.target.id.split("_")[1];
	print("testCB: "+activity_name);
	if(activity_name=="ColorMyWorld"){
		print("launching CMW");
		var url = "https://ccosse.github.io/colormyworld/";
		window.open(url);
	}
	else if(activity_name=="NowReadThis"){
		print("launching NRT");
		var url = "http://www.asymptopia.org/NowReadThis/";
		window.open(url);
	}
	else if(activity_name=="TuxMathScrabble"){
		print("launching TMS");
		var url = "http://www.asymptopia.org/TuxMathScrabble-2015/";
		window.open(url);
	}
}
var createAssignmentObj=function(att){
	var a=document.createElement("a");
	a.id=att['activity_name']+"_attachments-bar";
	print("a.id="+a.id);

	var ext=att['activity_name'].slice(-3);
	var att_color;
	var att_class;
	if(ext=='pdf'||ext=='PDF')
		{att_color="#FC0";att_class="fa fa-file-pdf-o";}
	else if(ext=='png'||ext=='jpg'||ext=='gif'||ext=='jpeg'||ext=='svg'||ext=='xcf')
		{att_color="#F66";att_class="fa fa-file-image-o";}
	else if(ext=='.py'||ext=='.js'||ext=='css'||ext=='tml')
		{att_color="#AAF";att_class="fa fa-file-code-o";}
	else if(ext=='mov'||ext=='mp4'||ext=='avi')
		{att_color="#CF5";att_class="fa fa-file-video-o";}
	else if(ext=='doc'||ext=='ocx')
		{att_color="#55F";att_class="fa fa-file-word-o";}
	else if(ext=='zip'||ext=='tgz'||ext=='tar'||ext=='.gz')
		{att_color="#F55";att_class="fa fa-file-zip-o";}
	else if(ext=='mp3'||ext=='snd'||ext=='m4a'||ext=='wav'||ext=='WAV')
		{att_color="#0B0";att_class="fa fa-file-audio-o";}
	else if(ext=='txt'||ext=='cii')
		{att_color="#0FF";att_class="fa fa-file-text-o";}
	else
		{att_color="#CF5";att_class="fa fa-file-o";}

	var attrs=['activity_name','title'];
	var sherbert_colors=["#aaf2aa","#f48da8","#fcb96a",];
	var scidx=parseInt(Math.random()*sherbert_colors.length);
	var table_html='<div><center><table class="attachment-card" style="padding:2px 2px;background-color:'+sherbert_colors[scidx]+';border-radius:2px;color:#555;">';
/*
	table_html+='<tr><td><table style="background-color:'+att_color+'">'
	table_html+='<tr><td><div class="renameB" id="'+att['name']+'">RE</div></td></tr>';
	table_html+='<tr><td><div class="deleteB" id="'+att['name']+'">DE</div></td></tr>';
	table_html+='</table></td>';
*/
//&#xf013;
	table_html+='<tr>';
	table_html+='<td><div class="renameB" id="'+att['title']+'"><i id="'+att['title']+'" class="fa fa-gear" style="z-index:100;font-size:40px;color:'+att_color+'"></i></div></td>';
	table_html+='<td><a href="'+'serve?file='+att['title']+'" target="_blank"><i class="'+att_class+'" style="z-index:100;font-size:40px;color:'+att_color+'"></i></a></td>';
	table_html+='<td><a href="'+'serve?file='+att['title']+'" target="_blank"><i class="fa fa-edit" style="z-index:100;font-size:40px;color:'+att_color+'"></i></a></td>';


	table_html+='</tr>';
	for(var idx=0;idx<attrs.length;idx++){
		table_html+='<tr><td colSpan="3"><div style="text-align:center;">';
		var att_string=String(att[attrs[idx]])//.slice(-14);
		if(att_string.length==0)att_string="Unknown";
		table_html+=att_string;
		table_html+='</div></td></tr>';
	}
	table_html+='</table></center></div>';

	a.className="attachment";
	a.id=att['activity_name']+"_attachments-bar";
	a.innerHTML=table_html;
	print(table_html);
	return a;
}
