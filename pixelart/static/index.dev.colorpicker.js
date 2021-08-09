var picker = document.getElementById('colorpicker');
var pickerctx = picker.getContext('2d');
var lcolorcanvas = document.getElementById('leftcolor');
var rcolorcanvas = document.getElementById('rightcolor');
var lcolorctx = lcolorcanvas.getContext('2d');
var rcolorctx = rcolorcanvas.getContext('2d');
var pickerscale = 3;
var margin = 5; // Size of margin around canvas in pixels
var pickeroffsetX = picker.offsetLeft + margin; // Top right pixel of canvas
var pickeroffsetY = picker.offsetTop + margin;
var xmlhttppicker = new XMLHttpRequest();
var jsonimg = [];
xmlhttppicker.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		jsonimg = JSON.parse(this.responseText);
		var array = new Uint8ClampedArray(jsonimg.data);
		var sqr = new ImageData(array, jsonimg.width, jsonimg.height);
		pickerctx.putImageData(sqr, 0, 0);  // draw Image on picker
	  }
};
xmlhttppicker.open("GET", "/v11/colors", true);
xmlhttppicker.send();	


picker.addEventListener('mousedown',function(evt){
	document.body.style.mozUserSelect = document.body.style.webkitUserSelect = document.body.style.userSelect = 'none';
	lastX = evt.pickeroffsetX/pickerscale || (evt.pageX - picker.offsetLeft)/pickerscale;
	lastY = evt.pickeroffsetY/pickerscale || (evt.pageY - picker.offsetTop)/pickerscale;
	dragged = false;
},false);


var clickx;
var clicky;
var xmlhttpclick = new XMLHttpRequest();
xmlhttpclick.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		pickedcolor = JSON.parse(this.responseText);
		if(pickedcolor.rclick){
			rcolor = pickedcolor.data
			var array = new Uint8ClampedArray(rcolor);
			var sqr = new ImageData(array, 1, 1);
			rcolorctx.putImageData(sqr, 0, 0)
		}
		else{
			lcolor = pickedcolor.data
			var array = new Uint8ClampedArray(lcolor);
			var sqr = new ImageData(array, 1, 1);
			lcolorctx.putImageData(sqr, 0, 0)
		}
		//Use this to show which color is picked
	  }
};
xmlhttpclick.open("GET", "/v11/colors?clickx=0&clicky=0", true);
xmlhttpclick.send();

var rightclick = false;
picker.addEventListener('mouseup',function(evt){
	dragStart = null;
	if(!rightclick){
		clickx = Math.floor((evt.clientX - pickeroffsetX)/pickerscale);
		clicky = Math.floor((evt.clientY - pickeroffsetY)/pickerscale);
		xmlhttpclick.open("GET", "/v11/colors?clickx=" + clickx + "&clicky=" + clicky, true);
		xmlhttpclick.send();
	}	
	rightclick = false;
},false);

picker.addEventListener('contextmenu', function(evt) {
	    rightclick = true;
	    evt.preventDefault(); //Prevent right click menu
	    if(!dragged){
		clickx = Math.floor((evt.clientX - pickeroffsetX)/pickerscale);
		clicky = Math.floor((evt.clientY - pickeroffsetY)/pickerscale);
		xmlhttpclick.open("GET", "/v11/colors?clickx=" + clickx + "&clicky=" + clicky + "&rclick=1", true);
		xmlhttpclick.send();
	    }
	    return false; //Prevent right click menu
}, false);
		
