---
layout: post
title: Building a living photo frame with a Raspberry Pi and a motion detector
date: '2014-01-02T06:00:00+00:00'
redirect_from:
  - /photoframe

---
<style>
.rpi-lcd {
    margin: 12px 0;
}
.rpi-lcd img {
    width: 202px;
    height: 156px;
    margin-right: 16px;
    border: none;
}
.rpi-image-float {
    float: right; 
    margin: 0 0 0 24px;
}
</style>

Every hardware hacker has a start, and this one is mine. [My girlfriend](http://twitter.com/brittanymorgan) bought me a [Raspberry Pi](http://raspberrypi.org) for my birthday, and so I became determined to build something with it for her birthday two months later.

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%20Photo%20Frame%20corrected.jpg" style="border: 1px solid #303030; margin: 0 0 24px;">

As you can see above, I built a photo frame that has a few interesting parts. For one, the software which runs the photo frame, which I explore below, keeps the photos fresh from Instagram and Flickr. It then displays a random photo for a configurable six seconds. Secondly, there is a motion detector, built using a PIR sensor, which only turns the monitor on when somebody walks by.

This photo frame is easy to build, but it does take a bit of know-how. Mainly, you should feel comfortable soldering wires and mounting the screen and Raspberry Pi to a board or other object. The hard part for me was figuring out how to turn the monitor on and off through the command line. 

Everything else is gravy, from configuring wifi and autoboot/auto-login on the device to attaching and setting up the motion detecting PIR sensor. You can also use the [eLinux guide](http://elinux.org/R-Pi_Hub) to Raspberry Pi and its handy [RPi Hardware Basic Setup wiki](http://elinux.org/RPi_Hardware_Basic_Setup).

## Parts

### Raspberry Pi

I chose to use a Raspberry Pi for its simple wifi integration so that photos could be automatically updated. I didn't want to have to load photos on to an SD card which could then be read by an Arduino. 

Connecting the monitor was also trivial on a Raspberry Pi, where an Arduino, Maple, or Beagle Bone would require sourcing a connection between the monitor's composite input and an output from the device.

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%20Raspberry%20Pi.jpg">

###### [Raspberry Pi](http://www.adafruit.com/products/1344), $29 on Adafruit.

Make note of the fact that you actually don't see any of my connections on the top of the board (pictured below). In the below photo, where the Raspberry Pi is flipped vertically to show off the electrical connections, the monitor's composite cable and the motion detecting PIR sensor's red wires are soldered underneath. 

<img src="https://s3.amazonaws.com/static.newsblur.com/blog/Raspberry%20Pi%20Backside.jpg">

This way the photo frame looks cleaner. If I had connected the monitor using the yellow composite cable, it would have to be with a male-to-male composite adapter, since both the Raspberry Pi and the monitor have a male RCA connection. This would jut out about 2 inches below the device, resulting in a messy look for the frame.

### 3.5" LCD Monitor

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%203.5%20lcd.jpg">

###### [3.5" LCD Monitor](http://www.adafruit.com/products/913), $45 on Adafruit

Note that if you do not plan to solder the composite cable's two wires, you will need the ugly male-to-male adapter, <a href="http://www.adafruit.com/products/951">sold for $1.50 on Adafruit</a>.

There are a number of different sized LCD monitors:

<table class="rpi-lcd">
    <tr>
        <td><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%201.5%20lcd.jpg"></td>
        <td><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%202%20lcd.jpg"></td>
        <td><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%202.5%20lcd.jpg"></td>
    </tr>
    <tr>
        <td><h6><a href="http://www.adafruit.com/products/910">1.5" LCD</a>, $40</h6></td>
        <td><h6><a href="http://www.adafruit.com/products/911">2" LCD</a>, $40</h6></td>
        <td><h6><a href="http://www.adafruit.com/products/912">2.5" LCD</a>, $45</h6></td>
    </tr>
</table>
<table class="rpi-lcd">
    <tr>
        <td><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%204.3%20lcd.jpg"></td>
        <td><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%207%20lcd.jpg"></td>
        <td><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%2010%20lcd.jpg"></td>
    </tr>
    <tr>
        <td><h6><a href="http://www.adafruit.com/products/946">4.3" LCD</a>, $50</h6></td>
        <td><h6><a href="http://www.adafruit.com/products/947">7" LCD</a>, $75</h6></td>
        <td><h6><a href="http://www.adafruit.com/products/1287">10" LCD</a>, $150</h6></td>
    </tr>
</table>

<!--more-->

### 4GB SD Card with Raspbian (Raspberry Pi + Debian)

<div class="rpi-image-float">
    <img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%20SD%20Card.jpg" width="200">
    <h6><a href="http://www.adafruit.com/products/1121">4GB SD Card</a>, $10 on Adafruit</h6>
</div>

This tiny SD card comes pre-loaded with Raspbian. If you prefer to use your own SD card and want to bootload it, just follow [eLinux's Easy SD Card Setup wiki](http://elinux.org/RPi_Easy_SD_Card_Setup).

<div style="clear: both;"></div>

### Miniature Wifi on USB

<div class="rpi-image-float">
    <img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%20Wifi.jpg" width="200">
    <h6><a href="http://www.adafruit.com/products/814">USB Wifi</a>, $11 on Adafruit</h6>
</div>

Unless you're planning to use an ugly ethernet cable, this tiny wifi USB device works perfectly. It's easy to setup as well. I followed [Adafruit's tutorial for setting up wifi on a Raspberry Pi](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/overview). 

<div style="clear: both;"></div>

### Passive Infrared Motion Sensor

<div class="rpi-image-float">
    <img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%20PIR.jpg" width="200">
    <h6><a href="http://www.adafruit.com/products/189">PIR sensor</a>, $10 on Adafruit</h6>
</div>

This is a simple and inexpensive component that is responsible for turning the monitor on and off. The accuracy is great, as it never misses a beat, yet I haven't found it to accidentally trigger in the night unless we walk by. It also has two adjustable dials on the back that allow you to control its sensitivity and delay before firing. [Ladyada covers how it works](http://www.ladyada.net/learn/sensors/pir.html).

<div style="clear: both;"></div>

### Soldering Iron

<div class="rpi-image-float">
    <img src="http://ecx.images-amazon.com/images/I/31NVnBvhZdL._SL500_AA300_.jpg" width="200">
    <h6><a href="http://www.amazon.com/Aoyue-937-Digital-Soldering-Station/dp/B000I30QBW">Aoyue 937+</a>, $60 on Amazon</h6>
</div>

In order to connect the PIR motion detector and the composite cables, without resorting to the ugly male-to-male adapter, you will need to use a soldering iron. I chose the Aoyue 937+ Digital Soldering Station. Works great and I'm quite happy with it. I should have bought more tips, though.

<div style="clear: both;"></div>

### Frame

This is where you get creative. You effectively just need an enclosure, but I found that picture frames offer the greatest aesthetics-to-enclosure ratio. You just need something that can hold a Raspberry Pi and monitor taped to it. I used double-sided mounting tape as an adhesive, although the wires are being held up by the frame itself.

## Software

### Raspberry Pi setup

You'll want to make sure you're setup with the following:

 * [Auto-login](http://elinux.org/RPi_Debian_Auto_Login), so your Raspberry Pi doesn't sit at a login prompt.
 * [Auto-wifi](http://learn.adafruit.com/adafruits-raspberry-pi-lesson-3-network-setup/setting-up-wifi-with-occidentalis), so you can download images automatically whenever your Raspberry Pi is turned on.
 * [Disabled sleep](http://www.cyberciti.biz/tips/linux-disable-screen-blanking-screen-going-blank.html), so your photo frame doesn't shut off when you don't want it to.

### Downloading personal photos from Flickr

You'll need to [register your Flickr API app](http://www.flickr.com/services/apps/create/apply/), which is a quick process. That way you can get a Flickr API key that you can then use to walk the photos from your account. You will also need your [Flickr user id](http://idgettr.com).

There are two Python library dependencies for this code:

{% highlight shell %}
pip install flickrapi
pip install requests
{% endhighlight %}

Once those are installed, save this script as `download_flickr.py`
    
{% highlight python %}
#!/usr/bin/env python

import flickrapi
import requests

FLICKR_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
USER_ID = "25704617@N04"

def make_url(photo):
    # url_template = "http://farm{farm-id}.staticflickr.com/
    #                 {server-id}/{id}_{secret}_[mstzb].jpg"
    photo['filename'] = "%(id)s_%(secret)s_z.jpg" % photo
    url = ("http://farm%(farm)s.staticflickr.com/%(server)s/%(filename)s" 
           % photo)
    return url, photo['filename']

def main():
    print " ---> Requesting photos..."
    flickr = flickrapi.FlickrAPI(FLICKR_KEY)
    photos = flickr.walk(user_id=USER_ID)
    for photo in photos:
        url, filename = make_url(photo.__dict__['attrib'])
        path = '/home/pi/photoframe/flickr/%s' % filename
        try:
            image_file = open(path)
            print " ---> Already have %s" % url
        except IOError:
            print " ---> Downloading %s" % url
            r = requests.get(url)      
            image_file = open(path, 'w')
            image_file.write(r.content)
            image_file.close()

if __name__ == '__main__':
    main()
{% endhighlight %}

### Downloading extra photos from Flickr by tag name

Part of the fun of this photo frame is that not only do all of my photos get shown randomly, but I introduced a hodgepodge of random photos by downloading photos from a specific Flickr tag. In this case, I added koala photos, which makes for a pleasant randomness.

Save the following command as `download_koalas.sh` or whatever you like as a tag.

{% highlight shell %}
FLICKR_TAG=koala && \
wget 'http://api.flickr.com/services/feeds/photos_public.gne?tags=$FLICKR_TAG' -O- \
| grep -Po 'http://[^.]+\.staticflickr[^"]+(_b.jpg|_z.jpg)' \
| wget -P /home/pi/photoframe/$FLICKR_TAG -nc -i- 
{% endhighlight %}

### Automatic downloading of new photos

In order to have the photos refreshed, you'll need to have them download in the background. Add these two lines to your crontab with `crontab -e` if you're using both the Flickr photo downloader and the Flickr tag downloader.

{% highlight shell %}
0 * * * * python /home/pi/photoframe/download_flickr.py
30 * * * * /home/pi/photoframe/download_koalas.sh
{% endhighlight %}

### Slideshow

Now that we have the photos downloaded and refreshed at a regular interval, we need to get the slideshow running. We'll use a simple app called the Linux framebuffer imageviewer. Stick this command into a `slideshow.sh`.

{% highlight shell %}
fbi -noverbose -m 640x480 -a -u -t 6 /home/pi/art/**/*
{% endhighlight %}

The option for time is set to 6 seconds, and it uses autozoom to automagically pick a reasonable zoom factor when loading images. The `-u` option randomizes the order. 

### Detecting movement

The slideshow is now running at fullscreen with a randomized assortment of Flickr photos, both your own and from favorite tags. But it's running even when you're not there! let's use the PIR (motion) sensor to turn off the monitor after no movement has been detected for 60 seconds.

Save this file as `pir.py`.

{% highlight python %}
#!/usr/bin/env python

import sys
import time
import RPi.GPIO as io
import subprocess

io.setmode(io.BCM)
SHUTOFF_DELAY = 60 # seconds
PIR_PIN = 25       # 22 on the board
LED_PIN = 16

def main():
    io.setup(PIR_PIN, io.IN)
    io.setup(LED_PIN, io.OUT)
    turned_off = False
    last_motion_time = time.time()

    while True:
        if io.input(PIR_PIN):
            last_motion_time = time.time()
            io.output(LED_PIN, io.LOW)
            print ".",
            sys.stdout.flush()
            if turned_off:
                turned_off = False
                turn_on()
        else:
            if not turned_off and time.time() > (last_motion_time + 
                                                 SHUTOFF_DELAY):
                turned_off = True
                turn_off()
            if not turned_off and time.time() > (last_motion_time + 1):
                io.output(LED_PIN, io.HIGH)
        time.sleep(.1)

def turn_on():
    subprocess.call("sh /home/pi/photoframe/monitor_on.sh", shell=True)

def turn_off():
    subprocess.call("sh /home/pi/photoframe/monitor_off.sh", shell=True)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        io.cleanup()
{% endhighlight %}

### Turning the monitor on and off

There are two ways to turn the monitor on and off. Use the `tvservice` command to turn off the monitor port.

{% highlight shell %}
pi@raspberrypi ~/photoframe $ chmod 0744 monitor_off.sh 
pi@raspberrypi ~/photoframe $ cat monitor_off.sh 
tvservice -o

pi@raspberrypi ~/photoframe $ chmod 0744 monitor_on.sh 
pi@raspberrypi ~/photoframe $ cat monitor_on.sh 
tvservice -c "PAL 4:3" && fbset -depth 8 && fbset -depth 16
{% endhighlight %}

This method actually turns off the port, which works great except when you're connected to an HDMI monitor and it shuts off when the port is turned off. When you walk into the room, the port is turned back on but the monitor is off, so it doesn't come right back up. In this case, simply switch virtual terminals to blank out the screen using the `chvt` command.

{% highlight shell %}
pi@raspberrypi ~/photoframe $ chmod 0744 monitor_off.sh 
pi@raspberrypi ~/photoframe $ cat monitor_off.sh 
chvt 2

pi@raspberrypi ~/photoframe $ chmod 0744 monitor_on.sh 
pi@raspberrypi ~/photoframe $ cat monitor_on.sh 
chvt 7
{% endhighlight %}

### Fixing the monitor edges

By default, the image won't stretch to the edges of your monitor without cajoling. 

Here's the before photo:

<img src="https://s3.amazonaws.com/static.newsblur.com/blog/Raspberry%20Pi%20Photo%20Frame.jpg" style="border: 1px solid #303030; margin: 0 0 24px;">

And here's with margin correction on the monitor: 

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/RPi%20-%20Photo%20Frame%20corrected.jpg" style="border: 1px solid #303030; margin: 0 0 24px;">

To fix this, take a look at using <a href="http://elinux.org/RPiconfig">RPiconfig</a>. All you need to do is edit `/boot/config.txt` directly on the Raspberry Pi. The values you need to set are:

{% highlight python %}
overscan_left=-6    # number of pixels to skip on left
overscan_right=-6   # number of pixels to skip on right
overscan_top=24     # number of pixels to skip on top
overscan_bottom=24  # number of pixels to skip on bottom
{% endhighlight %}

These are my values, but every monitor is different. In order to figure out the values, I would set the values using a binary search (set high then low then halfway between the two and repeat with the new halfway point being the high/low on the correct side), and then rebooting. Eventually I found optimal values. 

Note that the values will be different from the boot screen to the photo viewer. Obviously, I optimized for the photo viewer, but that means the top and bottom of the boot screen is cut off. Not much better you can expect from a tiny $50 LCD monitor.

Also, if you need to rotate or flip the display, it's easy.

{% highlight python %}
display_rotate=0        Normal
display_rotate=1        90 degrees
display_rotate=2        180 degrees
display_rotate=3        270 degrees
display_rotate=0x10000  horizontal flip
display_rotate=0x20000  vertical flip
{% endhighlight %}

### Automatic start of the photo frame software

You'll want the software to start automatically on boot, so create a new init.d file at `/etc/init.d/flickrd`, and add the motion sensor and slideshow scripts to that new file:

{% highlight shell %}
sudo python /home/pi/photoframe/pir.py
/home/pi/photoframe/slideshow.sh
{% endhighlight %}

Then set the permissions with:

{% highlight shell %}
sudo chmod 755 /etc/init.d/flickrd
{% endhighlight %}

and finally register the script to be run at startup:

{% highlight shell %}
sudo update-rc.d flickrd defaults
{% endhighlight %}

Don't forget to run the `pir.py` script as root, since you'll need permissions to turn the monitor on and off.

## Troubleshooting

Everything above should leave you with a photo slideshow that automatically updates your photos, displays them zoomed in and fullscreen in random order, shutting off the monitor when nobody is around.

If you used the code above with no issues, congratulations! You're in a minority that can work with hardware and get everything right on the first try. For everybody else, we have to troubleshoot. Here are the issues that I ran into.

### Test your LED

Just getting the Raspberry Pi to respond to my commands was tricky enough, so I wrote this basic program to just blink the onboard LED. This is the Hello, World of the Raspberry Pi.

{% highlight python %}
import RPi.GPIO as GPIO
import time

LED_PIN = 18
def blink(pin):
    GPIO.output(pin,GPIO.HIGH)
    print " ---> On"
    time.sleep(.5)
    GPIO.output(pin,GPIO.LOW)
    print " ---> Off"
    time.sleep(.5)
    return

# to use Raspberry Pi board pin numbers
GPIO.setmode(GPIO.BOARD)
# set up GPIO output channel
GPIO.setup(LED_PIN, GPIO.OUT)
for _ in range(0,3):
    blink(LED_PIN)
GPIO.cleanup() 
{% endhighlight %}
    
### SSH'ing into your Raspberry Pi

You shouldn't have to rely on an external keyboard and a tiny screen to debug your Raspberry Pi. I suggest using [Pi Finder](http://ivanx.com/raspberrypi/) to locate the IP address, if it's on your local network. 

You can also use `arp -a` to find it. 

### Getting additional help

Turn to [Stack Exchange's new Raspberry Pi section](http://raspberrypi.stackexchange.com). It's still in beta as of early 2014, but there's a whole lot of great questions.
