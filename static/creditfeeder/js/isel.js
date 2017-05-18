/**********************************************************

    Organization    :Asymptopia Software | Software@theLimit

    Website         :www.asymptopia.org

    Author          :Charles B. Cosse

    Email           :ccosse@asymptopia.org

    Copyright       :(C) 2006-2014 Asymptopia Software

    License         :All Rights Reserved

***********************************************************/
var IconSelect=function(iconset,opts,id,idx_selected,title){


	var me={};

	me.iconset=iconset;
	me.opts=opts;
	me.idx_selected=idx_selected;
	me.selected=me.opts[me.idx_selected];
	me.title=title;
	me.cidlist=[];

	me.selectCB=function(e){

		var cid=e.target.id.split("_")[1];
		var lb=document.getElementById("lb_"+cid);

		me.idx_selected=me.opts.indexOf(lb.innerHTML);
		//should also equal cidlist.indexOf(cid)


		me.selected=me.opts[me.idx_selected];
		me.button.title=me.title+" = "+me.selected;
		document.getElementById("iopts_"+me.title).style.visibility="hidden";

		for(var cidx=0;cidx<me.cidlist.length;cidx++){
			rb_id="rb_"+me.cidlist[cidx];
			rb=document.getElementById(rb_id);
			lb_id="lb_"+me.cidlist[cidx];
			lb=document.getElementById(lb_id);
			if(cidx==me.idx_selected){
				lb.className="isel_selected";
				rb.checked=true;
			}
			else{
				lb.className="isel_choice";
				rb.checked=false;
			}
		}

	}

	me.button=document.createElement("div");
	me.button.className="iselB";
	me.button.style.width="32px";
	me.button.style.height="32px";
	me.button.id=common_id();
	me.button.style.zIndex="0";
	me.button.title=me.title+" = "+me.selected;
	me.button.id=id;
	me.button.value=me.opts[me.idx_selected];

	icon_url="/static/creditfeeder/icons/"+iconset[0];
	me.button.style.backgroundImage="url("+icon_url+")";

	me.iopts=document.createElement("div");
	me.iopts.className="isel_menu";
	me.iopts.id="iopts_"+title;
	me.button.appendChild(me.iopts);

	var t=document.createElement("table");

	for(var oidx=0;oidx<me.opts.length;oidx++){

		var r=t.insertRow(-1);
		var c0=r.insertCell(-1);
		var c1=r.insertCell(-1);
		cid=common_id();
		me.cidlist.push(cid);

		rb=document.createElement("input");
		rb.type="radio";
		rb.id="rb_"+cid;

		lb=document.createElement("div");
		lb.className="isel_choice";
		lb.innerHTML=me.opts[oidx];
		lb.id="lb_"+cid;

		if(oidx==me.idx_selected){
			rb.checked=true;
			lb.className="isel_selected";
		}
		if(navigator.appName=="Microsoft Internet Explorer"){
			rb.attachEvent("onmousedown",me.selectCB);
			lb.attachEvent("onmousedown",me.selectCB);
		}
		else{
			rb.addEventListener("mousedown",me.selectCB,false);//Q:click for ffox, mousedown for chrome?? apparently need 2 test!
			lb.addEventListener("mousedown",me.selectCB,false);//Q:click for ffox, mousedown for chrome?? apparently need 2 test!
		}
		c0.appendChild(rb);
		c1.appendChild(lb);
	}


	me.hover_iconCB=function(e){
		icon_url="/static/creditfeeder/icons/"+me.iconset[1];
		me.button.style.backgroundImage="url("+icon_url+")";
	}
	me.unhover_iconCB=function(e){
		icon_url="/static/creditfeeder/icons/"+me.iconset[0];
		me.button.style.backgroundImage="url("+icon_url+")";
	}
	me.down_iconCB=function(e){
		icon_url="/static/creditfeeder/icons/"+me.iconset[1];
		me.button.style.backgroundImage="url("+icon_url+")";
		if(me.iopts.style.visibility=="visible"){me.hideCB();}
		else{me.iopts.style.visibility="visible";}
	}
	me.up_iconCB=function(e){
		icon_url="/static/creditfeeder/icons/"+me.iconset[0];
		me.button.style.backgroundImage="url("+icon_url+")";
	}
	me.hideCB=function(e){
		me.iopts.style.visibility="hidden";
	}
	me.get_selected=function(){
		return me.selected;
	}
	me.get_idx_selected=function(){
		return me.idx_selected;
	}
	me.get=function(){
		return me.button;
	}
	if(navigator.appName=="Microsoft Internet Explorer"){
		me.button.attachEvent("onmouseover",me.hover_iconCB);
		me.button.attachEvent("onmouseout",me.unhover_iconCB);
		me.button.attachEvent("onmousedown",me.down_iconCB);
		me.button.attachEvent("onmouseup",me.up_iconCB);
		me.iopts.attachEvent("onmouseout",me.hideCB);
	}
	else{
		me.button.addEventListener("mouseover",me.hover_iconCB,false);
		me.button.addEventListener("mouseout",me.unhover_iconCB,false);
		me.button.addEventListener("mousedown",me.down_iconCB,false);
		me.button.addEventListener("mouseup",me.up_iconCB,false);
		me.iopts.addEventListener("click",me.hideCB,false);
	}

	me.iopts.appendChild(t);
	return me;
}
