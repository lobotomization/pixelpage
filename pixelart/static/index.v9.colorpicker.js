var picker = document.getElementById('colorpicker');
var pickerctx = picker.getContext('2d');
var pickerscale = 40;
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
xmlhttppicker.open("GET", "/v9/colors", true);
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
		}
		else{
			lcolor = pickedcolor.data
		}
		//var array = new Uint8ClampedArray(jsonimg.data);
		//var sqr = new ImageData(array, jsonimg.width, jsonimg.height);
		//console.log(jsonimg);
		//ctx.putImageData(sqr, clickx, clicky);  // Draw single pixel
		//pixelboard.src = picker.toDataURL("image/png") ;
		//Use this to show which color is picked
	  }
};


var rightclick = false;
picker.addEventListener('mouseup',function(evt){
	dragStart = null;
	if(!rightclick){
		clickx = Math.floor((evt.clientX - pickeroffsetX)/pickerscale);
		clicky = Math.floor((evt.clientY - pickeroffsetY)/pickerscale);
		xmlhttpclick.open("GET", "/v9/colors?clickx=" + clickx + "&clicky=" + clicky, true);
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
		xmlhttpclick.open("GET", "/v9/colors?clickx=" + clickx + "&clicky=" + clicky + "&rclick=1", true);
		xmlhttpclick.send();
	    }
	    return false; //Prevent right click menu
}, false);
		
