/**********************************************************

    Organization    :Asymptopia Software | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2014 Asymptopia Software

    License         :All Rights Reserved

***********************************************************/
var IconButton=function(iconset,iCB,title,iID){


	var me={};

	me.iconset=iconset;
	me.iCB=iCB;
	
	me.selectCB=function(e){
		me.idx_selected=me.opts.indexOf(e.target.innerHTML);
		me.selected=me.opts[me.idx_selected];
		me.div.title="selected: "+me.selected+" "+me.idx_selected.toString();
		me.iopts.style.visibility="hidden";
	}
	
	me.div=document.createElement("div");
	me.div.className="ibutton";
	me.div.style.width="32px";
	me.div.style.height="32px";
	if(iID!=null)me.div.id=iID;
	else me.div.id=common_id();
	me.div.style.zIndex="100";
	me.div.title=title;
	
	icon_url="http://www.autoteach.net/static/icons/"+me.iconset[0];
	me.div.style.backgroundImage="url("+icon_url+")";
	
	me.hover_iconCB=function(e){
		icon_url="http://www.autoteach.net/static/icons/"+me.iconset[1];
		me.div.style.backgroundImage="url("+icon_url+")";
	}
	me.unhover_iconCB=function(e){
		icon_url="http://www.autoteach.net/static/icons/"+me.iconset[0];
		me.div.style.backgroundImage="url("+icon_url+")";
	}
	me.down_iconCB=function(e){
		icon_url="http://www.autoteach.net/static/icons/"+me.iconset[2];
		me.div.style.backgroundImage="url("+icon_url+")";
	}
	me.up_iconCB=function(e){
		icon_url="http://www.autoteach.net/static/icons/"+me.iconset[0];
		me.div.style.backgroundImage="url("+icon_url+")";
	}
	me.get=function(){
		return me.div;
	}
	if(navigator.appName=="Microsoft Internet Explorer"){
		me.div.attachEvent("onmouseover",me.hover_iconCB);
		me.div.attachEvent("onmouseout",me.unhover_iconCB);
		me.div.attachEvent("onmousedown",me.down_iconCB);
		me.div.attachEvent("onmouseup",me.up_iconCB);
		me.div.attachEvent("onclick",me.iCB);
	}
	else{
		me.div.addEventListener("mouseover",me.hover_iconCB,false);
		me.div.addEventListener("mouseout",me.unhover_iconCB,false);
		me.div.addEventListener("mousedown",me.down_iconCB,false);
		me.div.addEventListener("mouseup",me.up_iconCB,false);
		me.div.addEventListener("click",me.iCB,false);
	}	

	return me;
}

