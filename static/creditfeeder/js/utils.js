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
	print(a.id);
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
var testCB=function(id){
	print('testCB');
	var activity_name=id.split("_")[0];
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
var configureCB=function(){print('configureCB');}

var createAssignmentObj=function(att){
	var a=document.createElement("a");
	a.className="attachment";
	a.id=att['activity_name']+"_"+att['id'];
	print("a.id="+a.id);

	var bgname,att_color,att_class;
	var sherbert_colors=["#aaf2aa","#f48da8","#fcb96a",];

	var att_class1='fa fa-external-link';
	var att_class2='fa fa-gear';
	var att_class3='fa fa-edit';
	var att_class4='fa fa-times-rectangle';

	if(att['activity_name']=='ColorMyWorld'){bgname='/static/creditfeeder/images/colormyworld_tile.png';att_color='#8bc98b';}
	else if(att['activity_name']=='NowReadThis'){bgname='/static/creditfeeder/images/jcdesign.jpg';att_color='#f48da8';}
	else if(att['activity_name']=='TuxMathScrabble'){bgname='/static/creditfeeder/images/tuxmathscrabble_tile.png';att_color='#d49b57';}

	var attrs=['activity_name','title'];
	var scidx=parseInt(Math.random()*sherbert_colors.length);

	var header_html="";
	if(att['mode']==0){
		header_html+="<div class='header' style='color:"+att_color+"'>";
		header_html+="<i onclick='assignCB(\""+a.id+"\")' class='tooltip "+att_class1+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Assign</span></i>";
		header_html+="<i onclick='testCB(\""+a.id+"\")' class='tooltip "+att_class2+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Test</span></i>";
		header_html+="<i onclick='configureCB(\""+a.id+"\")' class='tooltip "+att_class3+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Configure</span></i>";
		header_html+="<i onclick='deleteCB(\""+a.id+"\")' class='tooltip "+att_class4+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Delete</span></i>";
		header_html+="<br>";
		header_html+=att['title'].slice(-15)+"</div>";
	}
	else if(att['mode']==1){
		header_html+="<div class='header' style='color:"+att_color+"'>";
//		header_html+="<i onclick='assignCB(\""+a.id+"\")' class='tooltip "+att_class1+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Assign</span></i>";
		header_html+="<i onclick='testCB(\""+a.id+"\")' class='tooltip "+att_class2+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Test</span></i>";
//		header_html+="<i onclick='configureCB(\""+a.id+"\")' class='tooltip "+att_class3+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Configure</span></i>";
		header_html+="<i onclick='removeCB(\""+a.id+"\")' class='tooltip "+att_class4+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Remove</span></i>";
		header_html+="<br>";
		header_html+=att['title'].slice(-15)+"</div>";
	}
	else{
		header_html+="<div class='header' style='color:"+att_color+"'>";
//		header_html+="<i onclick='assignCB(\""+a.id+"\")' class='tooltip "+att_class1+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Assign</span></i>";
		header_html+="<i onclick='testCB(\""+a.id+"\")' class='tooltip "+att_class2+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Test</span></i>";
//		header_html+="<i onclick='configureCB(\""+a.id+"\")' class='tooltip "+att_class3+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Configure</span></i>";
//		header_html+="<i onclick='removeCB(\""+a.id+"\")' class='tooltip "+att_class4+"' style='font-size:40px;padding:0px 5px'><span class='tooltiptext'>Remove</span></i>";
		header_html+="<br>";
		header_html+=att['title'].slice(-15)+"</div>";
	}

	var body_html="<img src='"+bgname+"' style='width:200px;height:200px;'/>"
	var footer_html="<div class='footer' style='color:"+att_color+"'>"+att['activity_name'].slice(-15)+"</div>";

	var tableHTML="<table class='attachment_table' align='center'><tr><td>";
	tableHTML+=header_html;
	tableHTML+="</td></tr><tr><td>";
	tableHTML+=body_html;
	tableHTML+="</td></tr><tr><td>";
	tableHTML+=footer_html;
	tableHTML+="</td></tr></table>";

	a.innerHTML=tableHTML;
	return a;
}
