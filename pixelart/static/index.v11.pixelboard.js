Number.prototype.mod = function(n) {
	    return ((this%n)+n)%n;
};

var canvas = document.getElementById('myCanvas');
var pixelboard = new Image;
canvas.width = width;
canvas.height = height;
var ox = 0; // Need to keep track of origin
var oy = 0; // Using ctx to track origin led to graphical glitches
var margin = 5; // Size of margin around canvas in pixels
var offsetX = canvas.offsetLeft + margin; // Top right pixel of canvas
var offsetY = canvas.offsetTop + margin;
var lcolor = [0, 0, 0, 255]
var rcolor = [255, 255, 255, 255] //Used by colorpicker and this script too
//console.log("Board is " + board); //Loaded from outside of script, in html file
window.onload = function(){		    
	var ctx = canvas.getContext('2d');
	trackTransforms(ctx);	 
	function redraw(){
		// Clear the entire canvas
		var p1 = ctx.transformedPoint(0,0);
	        var p2 = ctx.transformedPoint(canvas.width,canvas.height);
	        ctx.clearRect(p1.x,p1.y,p2.x-p1.x,p2.y-p1.y);
	      	ctx.save();
	      	ctx.setTransform(1,0,0,1,0,0);
	      	ctx.clearRect(0,0,canvas.width,canvas.height);
	      	ctx.restore();
	      	ctx.drawImage(pixelboard,0,0);	              
	}
	redraw();
	// Use API to draw some stuff from the DB to get captured as an Image object
	var xmlhttpapi = new XMLHttpRequest();
	var jsonimg = [];
	xmlhttpapi.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			jsonimg = JSON.parse(this.responseText);
			var array = new Uint8ClampedArray(jsonimg.data);
			var sqr = new ImageData(array, jsonimg.width, jsonimg.height);
	      		ctx.setTransform(1,0,0,1,0,0); // Move draw ctx to origin
			ctx.putImageData(sqr, 0, 0);  // draw Image on canvas
			pixelboard.src = canvas.toDataURL("image/png") ;
		  }
	};
	xmlhttpapi.open("GET", "/v11/api?ox=" + ox + "&oy=" + oy + "&board=" + board + "&width=" + width + "&height=" + height, true);
	xmlhttpapi.send();	
      

	var lastX=canvas.width/2, lastY=canvas.height/2;
	var dragStart,dragged;
	canvas.addEventListener('mousedown',function(evt){
		document.body.style.mozUserSelect = document.body.style.webkitUserSelect = document.body.style.userSelect = 'none';
		lastX = evt.offsetX/scale || (evt.pageX - canvas.offsetLeft)/scale;
		lastY = evt.offsetY/scale || (evt.pageY - canvas.offsetTop)/scale;
		dragStart = ctx.transformedPoint(lastX,lastY);
		dragged = false;
	},false);
	
	canvas.addEventListener('mousemove',function(evt){
		lastX = evt.offsetX/scale || (evt.pageX - canvas.offsetLeft)/scale;
		lastY = evt.offsetY/scale || (evt.pageY - canvas.offsetTop)/scale;
		var deadzone = .75	
		if (dragStart){
			var pt = ctx.transformedPoint(lastX,lastY);
			if((Math.abs(pt.x - dragStart.x) > deadzone || Math.abs(pt.y - dragStart.y) > deadzone) && !rightclick){
				dragged = true;
				ctx.translate(pt.x-dragStart.x,pt.y-dragStart.y);
				redraw();
			}
		}
	},false);

	var clickx;
	var clicky;
	var xmlhttpclick = new XMLHttpRequest();
	xmlhttpclick.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			jsonimg = JSON.parse(this.responseText);
			var array = new Uint8ClampedArray(jsonimg.data);
			var sqr = new ImageData(array, jsonimg.width, jsonimg.height);
	      		//ctx.setTransform(1,0,0,1,0,0); // Might not need this
			ctx.putImageData(sqr, clickx, clicky);  // Draw single pixel
			pixelboard.src = canvas.toDataURL("image/png") ;
		  }
	};

	var rightclick = false;
	document.addEventListener('mouseup',function(evt){
		dragStart = null;
		if(dragged && !rightclick){
			var p1 = ctx.transformedPoint(0,0);
			ox = ox + Math.round(p1.x);
			oy = oy + Math.round(p1.y);
			xmlhttpapi.open("GET", "/v11/api?ox=" + ox + "&oy=" + oy + "&board=" + board + "&width=" + width + "&height=" + height, true);
			xmlhttpapi.send();
		}
		else if(!rightclick){
			var p1 = ctx.transformedPoint(0,0);
			ox = ox + Math.round(p1.x);
			oy = oy + Math.round(p1.y);
			clickx = Math.floor((evt.clientX - offsetX)/scale);
			clicky = Math.floor((evt.clientY - offsetY)/scale);
			xmlhttpclick.open("GET", "/v11/click?ox=" + ox + "&oy=" + oy + "&clickx=" + clickx + "&clicky=" + clicky + "&board=" + board + "&r=" + lcolor[0] + "&g=" + lcolor[1] + "&b=" + lcolor[2], true);
			xmlhttpclick.send();
		}	
		rightclick = false;
	},false);


	canvas.addEventListener('contextmenu', function(evt) {
		    rightclick = true;
		    evt.preventDefault(); //Prevent right click menu
		    if(!dragged){
			var p1 = ctx.transformedPoint(0,0);
			ox = ox + Math.round(p1.x);
			oy = oy + Math.round(p1.y);
			clickx = Math.floor((evt.clientX - offsetX)/scale);
			clicky = Math.floor((evt.clientY - offsetY)/scale);
			xmlhttpclick.open("GET", "/v11/click?ox=" + ox + "&oy=" + oy + "&clickx=" + clickx + "&clicky=" + clicky + "&board=" + board + "&r=" + rcolor[0] + "&g=" + rcolor[1] + "&b=" + rcolor[2] , true);
			xmlhttpclick.send();
		    }
		    return false; //Prevent right click menu
	}, false);
			};

	
	// Adds ctx.getTransform() - returns an SVGMatrix
	// Adds ctx.transformedPoint(x,y) - returns an SVGPoint
	function trackTransforms(ctx){
	      	var svg = document.createElementNS("http://www.w3.org/2000/svg",'svg');
	      	var xform = svg.createSVGMatrix();
	     	ctx.getTransform = function(){ return xform; };

		var savedTransforms = [];
	      	var save = ctx.save;
	      	ctx.save = function(){
			savedTransforms.push(xform.translate(0,0));
			return save.call(ctx);
		};   
	var restore = ctx.restore;
	ctx.restore = function(){
		xform = savedTransforms.pop();
		return restore.call(ctx);
       	};
	var translate = ctx.translate;
	ctx.translate = function(dx,dy){
		xform = xform.translate(dx,dy);
		return translate.call(ctx,dx,dy);
	};    
	var transform = ctx.transform;
	ctx.transform = function(a,b,c,d,e,f){
		var m2 = svg.createSVGMatrix();
		m2.a=a; m2.b=b; m2.c=c; m2.d=d; m2.e=e; m2.f=f;
		xform = xform.multiply(m2);
		return transform.call(ctx,a,b,c,d,e,f);
	};    
	var setTransform = ctx.setTransform;
	ctx.setTransform = function(a,b,c,d,e,f){
			                xform.a = a;
			                xform.b = b;
			                xform.c = c;
			                xform.d = d;
			                xform.e = e;
			                xform.f = f;
			                return setTransform.call(ctx,a,b,c,d,e,f);
			            };
		    
	var pt  = svg.createSVGPoint();
	ctx.transformedPoint = function(x,y){
		pt.x=x; pt.y=y;
		return pt.matrixTransform(xform.inverse());
	}
}	
