---
layout: post
title: 'Code snippet: Stopping a jQuery AJAX Request'
date: '2010-03-02T23:27:31+00:00'

---
I want JavaScript to feel as smooth as a native application. I think scrolling is one of the largest issues, but this code snippet is more about aborting the jQuery AJAX event before it has a chance to complete.

There's no good documentation in the jQuery docs about how to do this. other than to just use this command on an existing AJAX request:

<code class="javascript">
var request = $.ajax('/url', data, callback);
request.abort();
</code>

That doesn't work. Well, it does work, but if you try to run it again or synchronously with other requests, you'll run into issues.

The issues are non-trivial, but avoidable. I'll cut to the chase; I came up with a solution, then found that somebody did it better and more correct. 

Rather than spreading incorrect (rather, incomplete) code, I'll just show the proper way to do it and then link to the source.

<code class="javascript">
_isAbort: function(xhr, o){
	var ret = !!( o.abortIsNoSuccess 
	              && ( !xhr 
	                   || xhr.readyState === 0
	                   || this.lastAbort === o.xhrID ) );
	xhr = null;
	return ret;
},
</code>

That's a lot of work. Don't bother, just use jquery.ajaxManager v.3.0: <http://www.protofunc.com/scripts/jquery/ajaxManager3/>

Note, however, that if you just google "jquery ajax manager" or some variant, you will end up at the old version, which is at: <http://www.protofunc.com/scripts/jquery/ajaxManager/>. They could do some work on their google juice pointing to the latest version.

Hope this helps somebody else, even if part of a google search for "[jquery ajax stop request](http://www.google.com/search?client=safari&rls=en&q=jquery+ajax+stop+request&ie=UTF-8&oe=UTF-8)" someday.
