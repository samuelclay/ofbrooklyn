---
layout: post
title: 'Code Snippet: jQuery Edit In Place'
date: '2010-03-24T11:23:16+00:00'

---
<script>
    $.fn.extend({
        edit_in_place: function(opts, callback) {
            var self = this;
            var defaults = {
                'input_type': 'text'
            }
            var options = $.extend({}, defaults, opts);
            
            return this.each(function() {
                var $this = $(this);
                var $input;
                var original_value = $this.html().replace(/<br.*?>/g, '\n');
                var original_display = $this.css('display');
                
                
                $this.bind('click', function() {
                    var starting_value = $this.html().replace(/<br.*?>/g, '\n');
                    
                    if (options['input_type'] == 'text') {
                        $input = $.make('input', { type: 'text', name: 'eip_input', value: starting_value });
                    } else if (options['input_type'] == 'textarea') {
                        $input = $.make('textarea', { name: 'eip_input' }, starting_value);
                    }
                
                    var $form = $.make('div', { className: 'eip-container' }, [
                        $input,
                        $.make('button', { className: 'eip-submit' }, 'OK'),
                        $.make('button', { className: 'eip-cancel' }, 'Cancel')
                    ]);
                    
                    $this.css({'display': 'none'});
                    $this.after($form);
                    $input.focus();
                    if (original_value == starting_value) {
                        $input.select();
                    }
                    
                    var restore_input = function(input) {
                        return function($this, $form) {
                            $this.css({'display': original_display});
                            $form.empty().remove();
                            if (input) {
                                $this.html(input.replace(/[\n\r]+/g, "<br /><br />"));
                                $.isFunction(callback) && callback.call(self, input);
                            }
                        }($this, $form);
                    };

                    setTimeout(function() {
                        $(document).one('click.edit_in_place', function() {
                            restore_input($input.val());
                        });
                        $form.click(function(e) {
                            if (e.target.className == 'eip-cancel') {
                                restore_input();
                                $(document).unbind('click.edit_in_place');
                            } else if (e.target.className == 'eip-submit') {
                                restore_input($input.val());
                                $(document).unbind('click.edit_in_place');
                            }
                            e.stopPropagation;
                            return false;
                        });
                    }, 10);
                });
                
            });
        }
    });
    
    $.extend({
    
        make: function(){
            var $elem,text,children,type,name,props;
            var args = arguments;
            var tagname = args[0];
            if(args[1]){
                if (typeof args[1]=='string'){
                    text = args[1];
                }else if(typeof args[1]=='object' && args[1].push){
                  children = args[1];
                }else{
                    props = args[1];
                }
            }
            if(args[2]){
                if(typeof args[2]=='string'){
                    text = args[2];
                }else if(typeof args[1]=='object' && args[2].push){
                  children = args[2];
                }
            }
            if(tagname == 'text' && text){
                return document.createTextNode(text);
            }else{
                $elem = $(document.createElement(tagname));
                if(props){
                    for(var propname in props){
                      if (props.hasOwnProperty(propname)) {
                            if($elem.is(':input') && propname == 'value'){
                                $elem.val(props[propname]);
                            } else {
                                $elem.attr(propname, props[propname]);
                            }
                        }
                    }
                }
                if(children){
                    for(var i=0;i<children.length;i++){
                        if(children[i]){
                            $elem.append(children[i]);
                        }
                    }
                }
                if(text){
                    $elem.html(text);
                }
                return $elem;
            }
        }
        
    });

/*
 * jQuery Color Animations
 * Copyright 2007 John Resig
 * Released under the MIT and GPL licenses.
 */

(function(jQuery){

	// We override the animation for all of these color styles
	jQuery.each(['backgroundColor', 'borderBottomColor', 'borderLeftColor', 'borderRightColor', 'borderTopColor', 'color', 'outlineColor'], function(i,attr){
		jQuery.fx.step[attr] = function(fx){
			if ( fx.state == 0 ) {
				fx.start = getColor( fx.elem, attr );
				fx.end = getRGB( fx.end );
			}

			fx.elem.style[attr] = "rgb(" + [
				Math.max(Math.min( parseInt((fx.pos * (fx.end[0] - fx.start[0])) + fx.start[0]), 255), 0),
				Math.max(Math.min( parseInt((fx.pos * (fx.end[1] - fx.start[1])) + fx.start[1]), 255), 0),
				Math.max(Math.min( parseInt((fx.pos * (fx.end[2] - fx.start[2])) + fx.start[2]), 255), 0)
			].join(",") + ")";
		}
	});

	// Color Conversion functions from highlightFade
	// By Blair Mitchelmore
	// http://jquery.offput.ca/highlightFade/

	// Parse strings looking for color tuples [255,255,255]
	function getRGB(color) {
		var result;

		// Check if we're already dealing with an array of colors
		if ( color && color.constructor == Array && color.length == 3 )
			return color;

		// Look for rgb(num,num,num)
		if (result = /rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(color))
			return [parseInt(result[1]), parseInt(result[2]), parseInt(result[3])];

		// Look for rgb(num%,num%,num%)
		if (result = /rgb\(\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*,\s*([0-9]+(?:\.[0-9]+)?)\%\s*\)/.exec(color))
			return [parseFloat(result[1])*2.55, parseFloat(result[2])*2.55, parseFloat(result[3])*2.55];

		// Look for #a0b1c2
		if (result = /#([a-fA-F0-9]{2})([a-fA-F0-9]{2})([a-fA-F0-9]{2})/.exec(color))
			return [parseInt(result[1],16), parseInt(result[2],16), parseInt(result[3],16)];

		// Look for #fff
		if (result = /#([a-fA-F0-9])([a-fA-F0-9])([a-fA-F0-9])/.exec(color))
			return [parseInt(result[1]+result[1],16), parseInt(result[2]+result[2],16), parseInt(result[3]+result[3],16)];

		// Otherwise, we're most likely dealing with a named color
		return colors[jQuery.trim(color).toLowerCase()];
	}
	
	function getColor(elem, attr) {
		var color;

		do {
			color = jQuery.curCSS(elem, attr);

			// Keep going until we find an element that has color, or we hit the body
			if ( color != '' && color != 'transparent' || jQuery.nodeName(elem, "body") )
				break; 

			attr = "backgroundColor";
		} while ( elem = elem.parentNode );

		return getRGB(color);
	};
	
	// Some named colors to work with
	// From Interface by Stefan Petre
	// http://interface.eyecon.ro/

	var colors = {
		aqua:[0,255,255],
		azure:[240,255,255],
		beige:[245,245,220],
		black:[0,0,0],
		blue:[0,0,255],
		brown:[165,42,42],
		cyan:[0,255,255],
		darkblue:[0,0,139],
		darkcyan:[0,139,139],
		darkgrey:[169,169,169],
		darkgreen:[0,100,0],
		darkkhaki:[189,183,107],
		darkmagenta:[139,0,139],
		darkolivegreen:[85,107,47],
		darkorange:[255,140,0],
		darkorchid:[153,50,204],
		darkred:[139,0,0],
		darksalmon:[233,150,122],
		darkviolet:[148,0,211],
		fuchsia:[255,0,255],
		gold:[255,215,0],
		green:[0,128,0],
		indigo:[75,0,130],
		khaki:[240,230,140],
		lightblue:[173,216,230],
		lightcyan:[224,255,255],
		lightgreen:[144,238,144],
		lightgrey:[211,211,211],
		lightpink:[255,182,193],
		lightyellow:[255,255,224],
		lime:[0,255,0],
		magenta:[255,0,255],
		maroon:[128,0,0],
		navy:[0,0,128],
		olive:[128,128,0],
		orange:[255,165,0],
		pink:[255,192,203],
		purple:[128,0,128],
		violet:[128,0,128],
		red:[255,0,0],
		silver:[192,192,192],
		white:[255,255,255],
		yellow:[255,255,0]
	};
	
})(jQuery);

$(document).ready(function() {
    $('.eip .eip-text').edit_in_place({}, function() {
        var $this = $(this);
        $this.animate({'backgroundColor': 'orange'}, {'duration': 300, 'queue': false, 'complete': function() {
            $this.animate({'backgroundColor': 'white'}, {'duration': 300, 'queue': false});
        }});
    });
});
</script>

There are many solutions to the edit-in-place problem, but I wanted to make an easy solution that wasn't as complicated as some of the other edit-in-place JavaScript scripts, like jEditable.

Features:
<ol>
    <li>Detects surroundings and keeps the input container as either a block or inline display.</li>
    <li>Highlights text if it is the original text. If the text has changed, the entire text is not highlighted on edit.</li>
    <li>Easy customizable and styleable.</li>
</ol>

### Demo

<style>
.eip {
    font-family: Helvetica;
    font-size: 16px;
}

.eip .eip-text {
    font-weight: bold;
    padding: 2px 3px;
    border: 1px solid white;
}

.eip .eip-container {
    display: inline;
}

.eip input {
    font-family: Helvetica;
    font-size: 16px;
    font-weight: bold;
    padding: 2px;
    border: 1px solid #A0A0A0;
    display: inline;
    width: 250px;
}
</style>

<div class="eip">
    Test Input: <span class="eip-text">Click here to change this text.</span>
</div>

### JavaScript Code

    #!javascript
    (function($) {
        $.fn.extend({
            edit_in_place: function(opts, callback) {
                var self = this;
                var defaults = {
                    'input_type': 'text'
                }
                var options = $.extend({}, defaults, opts);
            
                return this.each(function() {
                    var $this = $(this);
                    var $input;
                    var original_value = $this.html().replace(/<br.*?>/g, '\n');
                    var original_display = $this.css('display');
                
                
                    $this.bind('click', function() {
                        var starting_value = $this.html().replace(/<br.*?>/g, '\n');
                    
                        if (options['input_type'] == 'text') {
                            $input = $.make('input', { type: 'text', name: 'eip_input', value: starting_value });
                        } else if (options['input_type'] == 'textarea') {
                            $input = $.make('textarea', { name: 'eip_input' }, starting_value);
                        }
                
                        var $form = $.make('div', { className: 'eip-container' }, [
                            $input,
                            $.make('button', { className: 'eip-submit' }, 'OK'),
                            $.make('button', { className: 'eip-cancel' }, 'Cancel')
                        ]);
                    
                        $this.css({'display': 'none'});
                        $this.after($form);
                        $input.focus();
                        if (original_value == starting_value) {
                            $input.select();
                        }
                    
                        var restore_input = function(input) {
                            return function($this, $form) {
                                $this.css({'display': original_display});
                                $form.empty().remove();
                                if (input) {
                                    $this.html(input.replace(/[\n\r]+/g, "<br /><br />"));
                                    $.isFunction(callback) && callback.call(self, input);
                                }
                            }($this, $form);
                        };

                        setTimeout(function() {
                            $(document).one('click.edit_in_place', function() {
                                restore_input($input.val());
                            });
                            $form.click(function(e) {
                                if (e.target.className == 'eip-cancel') {
                                    restore_input();
                                    $(document).unbind('click.edit_in_place');
                                } else if (e.target.className == 'eip-submit') {
                                    restore_input($input.val());
                                    $(document).unbind('click.edit_in_place');
                                }
                                e.stopPropagation;
                                return false;
                            });
                        }, 10);
                    });
                
                });
            }
        });
    
        $.extend({
    
            make: function(){
                var $elem,text,children,type,name,props;
                var args = arguments;
                var tagname = args[0];
                if(args[1]){
                    if (typeof args[1]=='string'){
                        text = args[1];
                    }else if(typeof args[1]=='object' && args[1].push){
                      children = args[1];
                    }else{
                        props = args[1];
                    }
                }
                if(args[2]){
                    if(typeof args[2]=='string'){
                        text = args[2];
                    }else if(typeof args[1]=='object' && args[2].push){
                      children = args[2];
                    }
                }
                if(tagname == 'text' && text){
                    return document.createTextNode(text);
                }else{
                    $elem = $(document.createElement(tagname));
                    if(props){
                        for(var propname in props){
                          if (props.hasOwnProperty(propname)) {
                                if($elem.is(':input') && propname == 'value'){
                                    $elem.val(props[propname]);
                                } else {
                                    $elem.attr(propname, props[propname]);
                                }
                            }
                        }
                    }
                    if(children){
                        for(var i=0;i<children.length;i++){
                            if(children[i]){
                                $elem.append(children[i]);
                            }
                        }
                    }
                    if(text){
                        $elem.html(text);
                    }
                    return $elem;
                }
            }
        
        });
    })(jQuery);

<p>To use this code, simply use this HTML, CSS, and small JavaScript snippet:</p>

    #!xml
    <div class="eip">
        Test Input: <span class="eip-text">Click here to change this text.</span>
    </div>

<p>And this CSS:</p>

    #!css
    .eip {
        font-family: Helvetica;
        font-size: 16px;
    }

    .eip .eip-text {
        font-weight: bold;
        padding: 2px 3px;
        border: 1px solid white;
    }

    .eip .eip-container {
        display: inline;
    }

    .eip input {
        font-family: Helvetica;
        font-size: 16px;
        font-weight: bold;
        padding: 2px;
        border: 1px solid #A0A0A0;
        display: inline;
        width: 250px;
    }

<p>And this simple piece of JavaScript, which includes a callback function that has the same scope as the original selectors:</p>

    #!javascript
    $(document).ready(function() {
        $('.eip .eip-text').edit_in_place({}, function() {
            var $this = $(this);
            $this.animate({'backgroundColor': 'orange'}, {'duration': 300, 'queue': false, 'complete': function() {
                $this.animate({'backgroundColor': 'white'}, {'duration': 300, 'queue': false});
            }});
        });
    });

Note that I am animating background colors in this small JavaScript snippet. To animate colors, you need John Resig's excellent <a href="http://plugins.jquery.com/project/color">jQuery.color.js</a>.
