---
layout: post
title: Old-style Mac OS X Leopard Exposé in Snow Leopard
date: '2011-01-09T10:37:33+00:00'

---
Progress is progress, except when it gets in the way of your workflow. Let's compare these two screenshots:

### Old-style Leopard Exposé
<img src="http://www.ofbrooklyn.com/media/photos/Screen_shot_2011-01-09_at_10.39.46_AM.png" width="640" style="border: 1px solid #909090;" />

### New-style Snow Leopard Exposé
<img src="http://www.ofbrooklyn.com/media/photos/Screen_shot_2011-01-09_at_10.59.03_AM.png" width="640" style="border: 1px solid #909090; margin-bottom: 24px;" />

Notice how much more pleasant the old-style Exposé is? Introduced in Mac OS X 10.3 Panther, and virtually unchanged until OS X 10.6 Snow Leopard, it featured proportional windows. By just looking at the size of the window relative to the other windows, you can get a fair idea of what the application is.

The proportional windows went out the window with the new Exposé. Now it features an inexplicable grid, with windows resized to all different dimensions relative to their original size. 

### Old-style Exposé in Snow Leopard

The great news is that you can get the old-school Exposé back. The beta builds of Snow Leopard included a new Dock.app that used the old-style exposé. By installing the old Dock.app, you get the new Dock features of Snow Leopard, while preserving the legendary Exposé.

#### Installation

1. [Download the Snow Leopard beta-build of Dock.app](http://www.ofbrooklyn.com/media/photos/Dock.app.zip)
1. Save to your Desktop and unzip.

#### Run the following commands in Terminal.app:

    #!sh
    sudo chown -R root ~/Desktop/Dock.app;
    sudo chgrp -R wheel ~/Desktop/Dock.app;
    sudo killall Dock && \
    sudo mv /System/Library/CoreServices/Dock.app ~/Desktop/OldDock.app && \
    sudo mv ~/Desktop/Dock.app /System/Library/CoreServices/

Easy to do and indispensible now that you have it back. Hat-tip to [miknos at MacRumors](http://forums.macrumors.com/showthread.php?t=869611) for the original find.

Note that you will have to repeat this process every time you upgrade your Mac OS to a new patch release (10.6.6 -> 10.6.7).

[@samuelclay](http://twitter.com/samuelclay) is on Twitter.

<i>Use Google Reader? I built [NewsBlur](http://www.newsblur.com), a new feed reader with intelligence.</i>
