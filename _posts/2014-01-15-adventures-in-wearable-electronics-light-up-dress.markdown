---
layout: post
title: Adventures in Wearable Electronics - Making a Light-up Dress
date: '2014-01-15T11:07:50+00:00'
redirect_from:
  - /dress

---
<table>
    <tr>
        <td>
            <img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Hoolahoop%202.gif" width="130" height="230">
        </td>
        <td>
            <img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Sparkles.gif" width="130" height="230">
        </td>
        <td>
            <img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Raindrops.gif" width="130" height="230">
        </td>
        <td>
            <img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Spiral.gif" width="130" height="230">
        </td>
    </tr>
</table>

For New Year's Eve 2014, my [girlfriend](http://twitter.com/brittanymorgan) and I went to a dance party where wearable electronics were not only encouraged but also on display from a variety of hobbyists. I decided to use this as an opportunity to combine two of my favorite hobbies: sewing and electronics. 

It is my goal to encourage more people to weave wearable electronics into their own clothing. It's the future and we might as well look the part. Plus it's easy to get started and to modify existing code.

The [full source code for this dress](https://gist.github.com/samuelclay/8276775) is available on GitHub.

## Hardware

<table>
    <tr>
        <td>
            <a href="http://www.adafruit.com/products/659"><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/flora.jpg" width="200" height="149" class="OB-hardware"></a>
        </td>
        <td>
            <a href="https://www.sparkfun.com/products/12025"><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/ledstrip.jpg" width="200" height="149" class="OB-hardware"></a>
        </td>
        <td>
            <a href="http://www.adafruit.com/products/727?gclid=CMGI5d3C6LsCFZKGfgod50gASw"><img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/batteries.jpg" width="200" height="149" class="OB-hardware"></a>
        </td>
    </tr>
</table>

I attached six [addressable LED strands from Sparkfun](https://www.sparkfun.com/products/12025) ($20 each) to the lining of Brittany's dress, and then used a [Flora module from Adafruit](http://www.adafruit.com/products/659) ($25) to control them. I then used a [3 x AAA battery holder from Adafruit](http://www.adafruit.com/products/727?gclid=CMGI5d3C6LsCFZKGfgod50gASw) ($2).


## Setup

I used Adafruit's [NeoPixel library](http://learn.adafruit.com/adafruit-neopixel-uberguide) to control the LEDs. There were 60 LEDs per 1 meter-long strand. We only needed 40 of the LEDs, but instead of cutting them off, we simply sewed the unused third underneath the strand and cut the software off at 40 LEDs. This way we can repurpose the LED strands when we decide to move them to a new dress.

In order to make the connections between the LED strands and the Flora module, I used [30 AWG wire](https://www.sparkfun.com/products/8186), which is an extremely thin and light wire. The gauge is 0.01" and is as fine as thread. This allowed me to sew the wire into the fabric. I could have used conductive thread, but this wire wrap has a sheath that prevents it from shorting other wires when they touch. It's also extremely light-weight, so having 18 wires (3 wires per LED strand: power, ground, data) looping around the dress wasn't an issue.

I also want to mention that the code below is hard-coded for six stands. There is a fine line between a hack and a project, and for this, due to my limited time budget, was closer to hack than reusable project. You can easily abstract the code below to account for more or fewer strands, but I was able to ship before midnight on NYE, so I'm considering it a success.

{% highlight C %}
void setup() {
  // To ensure that the first random color in `loop` is never the same
  randomSeed(analogRead(0));

  led_a.begin();
  led_b.begin();
  led_c.begin();
  led_d.begin();
  led_e.begin();
  led_f.begin();

  clearLEDs(true);
}

void loop() {
  for (int i=0; i<2; i++) {
    hulahoop(randomColor(), random(20,60));
  }

  sparkle(randomColor(), random(30,70));

  raindrops(randomColor(), random(20,60));

  spiral(randomColor(), random(15,30));
}
{% endhighlight %}

Above we have the code for `setup` and `loop`, the two main Arduino routines. Notice that I am repeating the hula hoop routine, since it's pretty quick and looks good on repeat.

I also want to note that every single routine gets its own random color and random delay. This bit of randomness is something I weave into all of my wearable electronics, since it goes just a bit further than off-the-shelf components and shows that there was some intelligence behind the routine.

By giving a random delay to each routine I am actually changing the speed of the routine. Sometimes the raindrops would fall quickly, sometimes the hula hoop would have a slow fall and rise. It's all part of making mesmerizing patterns.

<!--more-->

## Hula hoop

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Hoolahoop%202.gif" width="228" height="405" class="OB-full">

For the hula hoop routine, I chose to use cylons at equal positions that move up and down the strand. To make the transition from one LED to the next, I use a cylon, which is a fancy way of saying that the LEDs immediately above and below the active LED are also on, but at a reduced brightness. 

In this case the cylon is 5 LEDs wide. 100% brightness for the middle/active LED, 1/18th brightness for the two adjacent LEDs, and 1/36th brightness for the two LEDs further out from there.

So what you see to the left are actually 5 LEDs turned on per-strand, although they get quite dim as you get further from the active LED. You can adjust the dimness of the adjacent LEDs by adjusting the `weight` parameter.

{% highlight C %}
void hulahoop(unsigned long color, byte wait) {
  // weight determines how much lighter the outer "eye" colors are
  const byte weight = 18;  
  // It'll be easier to decrement each of these colors individually
  // so we'll split them out of the 24-bit color value
  byte red   = (color & 0xFF0000) >> 16;
  byte green = (color & 0x00FF00) >> 8;
  byte blue  = (color & 0x0000FF);

  // Start at closest LED, and move to the outside
  for (int i=0; i<=LED_COUNT-1; i++) {
    clearLEDs(false);
    led_a.setPixelColor(i, red, green, blue);
    led_b.setPixelColor(i, red, green, blue);
    led_c.setPixelColor(i, red, green, blue);
    led_d.setPixelColor(i, red, green, blue);
    led_e.setPixelColor(i, red, green, blue);
    led_f.setPixelColor(i, red, green, blue);
    // Now set two eyes to each side to get progressively dimmer
    for (int j=1; j<3; j++) {
      byte redWJ = red/(weight*j);
      byte greenWJ = green/(weight*j);
      byte blueWJ = blue/(weight*j);
      if (i-j >= 0) {
        led_a.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_b.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_c.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_d.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_e.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_f.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
      }
      if (i-j <= LED_COUNT) {
        led_a.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_b.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_c.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_d.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_e.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_f.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
      }
    }
    led_a.show();
    led_b.show();
    led_c.show();
    led_d.show();
    led_e.show();
    led_f.show();
    delay(wait);
  }

  // Now we go back to where we came. Do the same thing.
  for (int i=LED_COUNT-2; i>=1; i--) {
    clearLEDs(false);
    led_a.setPixelColor(i, red, green, blue);
    led_b.setPixelColor(i, red, green, blue);
    led_c.setPixelColor(i, red, green, blue);
    led_d.setPixelColor(i, red, green, blue);
    led_e.setPixelColor(i, red, green, blue);
    led_f.setPixelColor(i, red, green, blue);
    // Now set two eyes to each side to get progressively dimmer
    for (int j=1; j<3; j++)
    {
      byte redWJ = red/(weight*j);
      byte greenWJ = green/(weight*j);
      byte blueWJ = blue/(weight*j);

      if (i-j >= 0) {
        led_a.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_b.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_c.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_d.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_e.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
        led_f.setPixelColor(i-j, redWJ, greenWJ, blueWJ);
      }
      if (i-j <= LED_COUNT) {
        led_a.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_b.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_c.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_d.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_e.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
        led_f.setPixelColor(i+j, redWJ, greenWJ, blueWJ);
      }
    }
    led_a.show();
    led_b.show();
    led_c.show();
    led_d.show();
    led_e.show();
    led_f.show();
    delay(wait);
  }
}
{% endhighlight %}

## Sparkles

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Sparkles.gif" width="228" height="405" class="OB-full">

This is by far the easiest routine to program yet the one that brought the most attention. It simply flashes a random LED across all of the LED strips.

{% highlight C %}
void sparkle(unsigned long color, uint8_t wait) {
  for (int i=0; i < LED_COUNT * STRIP_COUNT; i++) {
    clearLEDs(true);
    int strip = floor(random(STRIP_COUNT));
    int led = floor(random(LED_COUNT));
    switch (strip) {
      case 0:
        led_a.setPixelColor(led, color);
        led_a.show();
        break;
      case 1:
        led_b.setPixelColor(led, color);
        led_b.show();
        break;
      case 2:
        led_c.setPixelColor(led, color);
        led_c.show();
        break;
      case 3:
        led_d.setPixelColor(led, color);
        led_d.show();
        break;
      case 4:
        led_e.setPixelColor(led, color);
        led_e.show();
        break;
      case 5:
        led_f.setPixelColor(led, color);
        led_f.show();
        break;
    }
    delay(wait);
  }
}
{% endhighlight %}

## Raindrops

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Raindrops.gif" width="228" height="405" class="OB-full">

This is by far the most difficult of the routines. This one sends down cylons (5 LEDs, with the center LED being the brightest and the adjacent LEDs becoming decreasingly bright, so as to give the impression of smoother animation). 

But you should notice that the next raindrop starts when the previous raindrop is half-way down the dress. In order to make it seamless, at the beginning of the routine I actually start another LED at the half-way mark, referred to in the below code as `e_alt`. This means that there is no point at which the dress looks spent and is waiting for the routine to start over.

{% highlight C %}
void raindrops(unsigned long color, byte wait) {
  // weight determines how much lighter the outer "eye" colors are
  const byte weight = 18;  
  // It'll be easier to decrement each of these colors individually
  // so we'll split them out of the 24-bit color value
  byte red = (color & 0xFF0000) >> 16;
  byte green = (color & 0x00FF00) >> 8;
  byte blue = (color & 0x0000FF);
  double sludge = 0.5;
  double a_offset = 0;
  double b_offset = 3;
  double c_offset = 1;
  double d_offset = 2;
  double e_offset = 4;
  double f_offset = 5;

  // Start at closest LED, and move to the outside
  for (int i=0; i<LED_COUNT*(STRIP_COUNT-1)*sludge+LED_COUNT*10; i++) {
    clearLEDs(false);
    double n = i % (int)(LED_COUNT*(STRIP_COUNT+1)*sludge-LED_COUNT*sludge);
    double led_count = (double)LED_COUNT;

    bool a_on = (sludge*a_offset*led_count) <= n && 
                n <= (sludge*a_offset*led_count+led_count);
    bool b_on = (sludge*b_offset*led_count) <= n && 
                n <= (sludge*b_offset*led_count+led_count);
    bool c_on = (sludge*c_offset*led_count) <= n && 
                n <= (sludge*c_offset*led_count+led_count);
    bool d_on = (sludge*d_offset*led_count) <= n && 
                n <= (sludge*d_offset*led_count+led_count);
    bool e_on = (sludge*e_offset*led_count) <= n && 
                n <= (sludge*e_offset*led_count+led_count);
    bool e_alt= (sludge*a_offset*led_count) <= n && 
                n <= (sludge*a_offset*led_count+led_count*sludge);
    bool f_on = (sludge*f_offset*led_count) <= n && 
                n <= (sludge*f_offset*led_count+led_count);

    if (!a_on && !b_on && !c_on && !d_on && !e_on && !f_on) {
      clearLEDs(true);
      break;
    }

    int a = n-a_offset*LED_COUNT*sludge;
    int b = n-b_offset*LED_COUNT*sludge;
    int c = n-c_offset*LED_COUNT*sludge;
    int d = n-d_offset*LED_COUNT*sludge;
    int e = n-e_offset*LED_COUNT*sludge;
    if (e_alt) {
      e = a+(LED_COUNT/2);
    }
    int f = n-f_offset*LED_COUNT*sludge;

    if (a_on) led_a.setPixelColor(a, red, green, blue);
    if (b_on) led_b.setPixelColor(b, red, green, blue);
    if (c_on) led_c.setPixelColor(c, red, green, blue);
    if (d_on) led_d.setPixelColor(d, red, green, blue);
    if (e_on || e_alt) led_e.setPixelColor(e, red, green, blue);
    if (f_on) led_f.setPixelColor(f, red, green, blue);

    // Now set two eyes to each side to get progressively dimmer
    for (int j=1; j<3; j++) {
      byte redWJ = red/(weight*j);
      byte greenWJ = green/(weight*j);
      byte blueWJ = blue/(weight*j);

      if (a-j >= 0 && a_on) 
        led_a.setPixelColor(a-j, redWJ, greenWJ, blueWJ);
      if (b-j >= 0 && b_on) 
        led_b.setPixelColor(b-j, redWJ, greenWJ, blueWJ);
      if (c-j >= 0 && c_on) 
        led_c.setPixelColor(c-j, redWJ, greenWJ, blueWJ);
      if (d-j >= 0 && d_on) 
        led_d.setPixelColor(d-j, redWJ, greenWJ, blueWJ);
      if (e-j >= 0 && e_on) 
        led_e.setPixelColor(e-j, redWJ, greenWJ, blueWJ);
      if (f-j >= 0 && f_on) 
        led_f.setPixelColor(f-j, redWJ, greenWJ, blueWJ);

      if (a-j <= LED_COUNT && a_on) 
        led_a.setPixelColor(a+j, redWJ, greenWJ, blueWJ);
      if (b-j <= LED_COUNT && b_on) 
        led_b.setPixelColor(b+j, redWJ, greenWJ, blueWJ);
      if (c-j <= LED_COUNT && c_on) 
        led_c.setPixelColor(c+j, redWJ, greenWJ, blueWJ);
      if (d-j <= LED_COUNT && d_on) 
        led_d.setPixelColor(d+j, redWJ, greenWJ, blueWJ);
      if (e-j <= LED_COUNT && e_on) 
        led_e.setPixelColor(e+j, redWJ, greenWJ, blueWJ);
      if (f-j <= LED_COUNT && f_on) 
        led_f.setPixelColor(f+j, redWJ, greenWJ, blueWJ);
    }
    led_a.show();
    led_b.show();
    led_c.show();
    led_d.show();
    led_e.show();
    led_f.show();
    delay(wait);
  }
}
{% endhighlight %}

## Spiral

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Spiral.gif" width="228" height="405" class="OB-full">

This routine is better in theory than in practice. The idea is to have a quick succession of LEDs light up in a spiral pattern. This would work a bit better with more LED strands wrapped around the dress.

In this case, I'm simply looping through the strands and lighting up successive LEDs. But the nice thing about this routine is that it has a dramatic crescendo to the top, at which point the hula hoop routine begins and it looks like the action started at the bottom and quickly worked its way up to the top, only to smoothly fall back down. It's a mesmerizing effect.

{% highlight C %}
void spiral(unsigned long color, byte wait) {
  const byte weight = 18;  
  byte red = (color & 0xFF0000) >> 16;
  byte green = (color & 0x00FF00) >> 8;
  byte blue = (color & 0x0000FF);

  for (int level=LED_COUNT-1; level >= 0; level--) {
    for (int strip=0; strip < STRIP_COUNT; strip++) {
      clearLEDs(false);

      switch (strip) {
        case 0:
          led_f.setPixelColor(level, red/weight, green/weight, blue/weight);
          led_a.setPixelColor(level, color);
          led_b.setPixelColor(level, red/weight, green/weight, blue/weight);
          break;
        case 1:
          led_a.setPixelColor(level, red/weight, green/weight, blue/weight);
          led_b.setPixelColor(level, color);
          led_c.setPixelColor(level, red/weight, green/weight, blue/weight);
          break;
        case 2:
          led_b.setPixelColor(level, red/weight, green/weight, blue/weight);
          led_c.setPixelColor(level, color);
          led_d.setPixelColor(level, red/weight, green/weight, blue/weight);
          break;
        case 3:
          led_c.setPixelColor(level, red/weight, green/weight, blue/weight);
          led_d.setPixelColor(level, color);
          led_e.setPixelColor(level, red/weight, green/weight, blue/weight);
          break;
        case 4:
          led_d.setPixelColor(level, red/weight, green/weight, blue/weight);
          led_e.setPixelColor(level, color);
          led_f.setPixelColor(level, red/weight, green/weight, blue/weight);
          break;
        case 5:
          led_e.setPixelColor(level, red/weight, green/weight, blue/weight);
          led_f.setPixelColor(level, color);
          led_a.setPixelColor(level, red/weight, green/weight, blue/weight);
          break;
      }

      led_a.show();
      led_b.show();
      led_c.show();
      led_d.show();
      led_e.show();
      led_f.show();
      delay(wait);
    }
  }  
}
{% endhighlight %}

## Random Colors

Since randomness is the spice that gives this dress its mesmerizing qualities, it's important to have a good list of colors to use.

{% highlight C %}
unsigned long COLORS[] = {
  NAVY, DARKBLUE, MEDIUMBLUE, BLUE, DARKGREEN, GREEN, TEAL, DARKCYAN, 
  DEEPSKYBLUE, DARKTURQUOISE, MEDIUMSPRINGGREEN, LIME, SPRINGGREEN, 
  AQUA, CYAN, MIDNIGHTBLUE, DODGERBLUE, LIGHTSEAGREEN, FORESTGREEN, 
  SEAGREEN, DARKSLATEGRAY, LIMEGREEN, MEDIUMSEAGREEN, TURQUOISE, 
  ROYALBLUE, STEELBLUE, DARKSLATEBLUE, MEDIUMTURQUOISE, INDIGO, 
  DARKOLIVEGREEN, CADETBLUE, CORNFLOWERBLUE, MEDIUMAQUAMARINE, DIMGRAY, 
  SLATEBLUE, OLIVEDRAB, SLATEGRAY, LIGHTSLATEGRAY, MEDIUMSLATEBLUE, 
  LAWNGREEN, CHARTREUSE, AQUAMARINE, MAROON, PURPLE, OLIVE, GRAY, 
  SKYBLUE, LIGHTSKYBLUE, BLUEVIOLET, DARKRED, DARKMAGENTA, SADDLEBROWN, 
  DARKSEAGREEN, LIGHTGREEN, MEDIUMPURPLE, DARKVIOLET, PALEGREEN, 
  DARKORCHID, YELLOWGREEN, SIENNA, BROWN, DARKGRAY, LIGHTBLUE, 
  GREENYELLOW, PALETURQUOISE, LIGHTSTEELBLUE, POWDERBLUE, FIREBRICK, 
  DARKGOLDENROD, MEDIUMORCHID, ROSYBROWN, DARKKHAKI, SILVER, 
  MEDIUMVIOLETRED, INDIANRED, PERU, CHOCOLATE, TAN, LIGHTGRAY, 
  THISTLE, ORCHID, GOLDENROD, PALEVIOLETRED, CRIMSON, GAINSBORO, PLUM, 
  BURLYWOOD, LIGHTCYAN, LAVENDER, DARKSALMON, VIOLET, PALEGOLDENROD, 
  LIGHTCORAL, KHAKI, ALICEBLUE, HONEYDEW, AZURE, SANDYBROWN, WHEAT, 
  BEIGE, WHITESMOKE, MINTCREAM, GHOSTWHITE, SALMON, ANTIQUEWHITE, 
  LINEN, LIGHTGOLDENRODYELLOW, OLDLACE, RED, FUCHSIA, MAGENTA, 
  DEEPPINK, ORANGERED, TOMATO, HOTPINK, CORAL, DARKORANGE, LIGHTSALMON, 
  ORANGE, LIGHTPINK, PINK, GOLD, PEACHPUFF, NAVAJOWHITE, MOCCASIN, 
  BISQUE, MISTYROSE, BLANCHEDALMOND, PAPAYAWHIP, LAVENDERBLUSH, SEASHELL, 
  CORNSILK, LEMONCHIFFON, FLORALWHITE, SNOW, YELLOW, LIGHTYELLOW, IVORY
};

unsigned long randomColor() {
  return COLORS[random(sizeof(COLORS)/sizeof(unsigned long))];
}
{% endhighlight %}

## Dancing to 2014

<img src="https://s3.amazonaws.com/static.newsblur.com/ofbrooklyn/Blue%20EL%20Jacket.jpg" height="405" width="279" class="OB-full">

And what good is a beautiful light-up dress without a well lit dance partner? Here I am decked out in blue EL wire. I spent the better part of three hours sewing this wire into the edges of one of my jackets. But while hand-sewing can take half a day, the result is a great fit and a capable match for Brittany's dress.

The [full source code for this dress](https://gist.github.com/samuelclay/8276775) is available on GitHub.
