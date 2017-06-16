---
layout: post
title: 'A jQuery Plugin: Default Values for Input Fields'
date: '2010-02-16T18:37:08+00:00'

---
<script>
(function($) {
    
    $.fn.extend({
        
        input_default: function(default_text, opts) {
            if (typeof default_text !== 'string') {
                opts = default_text;
            } else if (!opts) {
                opts = {
                    'default_text': default_text
                };
            } else {
                $.extend(opts, {'default_text': default_text});
            }
            
            var defaults = {
                'default_text': 'Type here...',
                'class_name': 'empty-input'
            };
            var options = $.extend({}, defaults, opts);

            return this.each(function () {
                var $this = $(this);

                if ($this.val() == '' 
                    || $this.val() == options['default_text']) {    
                    $this.addClass(options['class_name'])
                         .val(options['default_text']);
                }
                
                $this.bind('focus', function() {
                    if ($this.val() == options['default_text']) {
                        $this.val('')
                             .removeClass(options['class_name']);
                    } else {
                        $this.select();
                    }
                }).bind('blur', function() {
                    if ($.trim($this.val()) == '') {
                        $this.val(options['default_text'])
                             .addClass(options['class_name']);
                    } else {
                        $this.removeClass(options['class_name']);
                    }
                });
            });
        }
        
    });
    
})(jQuery);
</script>

<p>One of the best ways to write code that you tend to have to re-use is to put it in the public domain. That way when you need it again, it's a Google search away from your own blog.</p>

<p>This is a rather simple working example of default text on an input field. Click on the field, the text disappears, only to reappear if the user clicks somewhere else on the page without typing. The input also has a special class signifying that it is empty, so you can style the empty input.</p>

<h3>Demo</h3>
<style>
.default-text {
border: 1px solid #C0C0C0;
padding: 2px;
font-weight: bold;
font-size: 14px;
}

.empty-input {
color: #A0A0A0;
}

.default-text-label {
font-size: 16px;
font-weight: bold;
color: #303030;
}
</style>
<label for="default-text" class="default-text-label">Here is a text box: <input type="text" id="default-text" class="default-text" /></label>

<script>
$('.default-text').input_default('Enter anything in...');
</script>

<!--more-->

### JavaScript Code

{% highlight javascript %}
(function($) {

    $.fn.extend({
    
        input_default: function(default_text, opts) {
            if (typeof default_text !== 'string') {
                opts = default_text;
            } else if (!opts) {
                opts = {
                    'default_text': default_text
                };
            } else {
                $.extend(opts, {'default_text': default_text});
            }
        
            var defaults = {
                'default_text': 'Type here...',
                'class_name': 'empty-input'
            };
            var options = $.extend({}, defaults, opts);

            return this.each(function () {
                var $this = $(this);

                if ($this.val() == '' 
                    || $this.val() == options['default_text']) {    
                    $this.addClass(options['class_name'])
                         .val(options['default_text']);
                }
            
                $this.bind('focus', function() {
                    if ($this.val() == options['default_text']) {
                        $this.val('')
                             .removeClass(options['class_name']);
                    } else {
                        $this.select();
                    }
                }).bind('blur', function() {
                    if ($.trim($this.val()) == '') {
                        $this.val(options['default_text'])
                             .addClass(options['class_name']);
                    } else {
                        $this.removeClass(options['class_name']);
                    }
                });
            });
        }
    
    });

})(jQuery);
{% endhighlight %}

### Usage

First, the HTML you can use:

{% highlight html %}
<label for="default-text" class="default-text-label">
    Here is a text box: 
    <input type="text" id="default-text" class="default-text" />
</label>
{% endhighlight %}

You can call `input_default` with no arguments and get the defaults:

{% highlight javascript %}
$('.text').input_default();
{% endhighlight %}

Specify an optional string or class:

{% highlight javascript %}
$('.text').input_default('Enter text here...', {'class_name': 'empty'});
{% endhighlight %}

Here is some sample CSS to use:

{% highlight css %}
.default-text {
    border: 1px solid #C0C0C0;
    padding: 2px;
    font-weight: bold;
    font-size: 14px;
}

.empty-input {
    color: #A0A0A0;
}

.default-text-label {
    font-size: 16px;
    font-weight: bold;
    color: #303030;
}
{% endhighlight %}
