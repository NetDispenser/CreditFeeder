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
