---
layout: post
title: Building Grove — interactive trees that come alive to your breath at Burning
  Man 2016
date: '2017-03-31T08:17:43+00:00'

---

Grove is a set of 10 interactive biofeedback sculptures, a conversation between humans and trees. Each tree is made of steel tubes, thousands of LEDs, and custom breathing sensors.

Grove is a <a href="http://burningman.org/culture/history/art-history/archive/#Grove">2016 honorarium installation at Burning Man</a> and is the second installation made by the group that made <a href="http://www.ofbrooklyn.com/2014/09/6/building-pulse-bloom-biofeedback-burning-man-2014/">Pulse &amp; Bloom</a> in 2014. The core team is ten people: [Saba Ghole](https://twitter.com/sabarani), [Shilo Shiv Suleman](https://www.facebook.com/shilosuleman), [Severin Smith](https://twitter.com/thesprky), [Steve Lyon](https://www.facebook.com/notstevelyon), [Hunter Scott](https://hscott.net), [David Wang](https://cambridge.nuvustudio.com/david-wang), [Francis Coelho](https://www.facebook.com/coelho.francis), [Naeemeh Alavi](https://www.facebook.com/naeemeh.alavi), [Luke Iseman](http://lukeiseman.com), and myself, [Samuel Clay](https://twitter.com/samuelclay). Grove was conceptualized by the artist Shilo Shiv Suleman as part of her larger series exploring nature, intimacy and technology called [Beloved](http://melaagency.com/artists/shilo-shiv-suleman/).

Here's how Grove works: you sit down at the base of a tree and a flower opens up in front of you as it senses your presence. As you breathe into a pink flower lit from inside, the tree fills up with your breath, rising white streams overtaking multiple slowly descending green lines. As you breathe, the tree shimmers with light as it becomes a nighttime desert oasis.

<video src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/Grove.mp4" autoplay loop muted></video>

This post offers details on how this installation was built, from the custom circuit boards to the blooming flower and breathing sensors. You can access <a href="https://github.com/samuelclay/Grove">the complete source for Grove on GitHub</a>.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-breathing-nighttime.jpg">

<!--more-->

Grove is made up of ten trees, each of which has its own breath sensor and set of two thousand LEDs across four 5 meter 144 LEDs/meter LED strips and 16 high current LEDs in the leaves. That takes both a lot of power to run and a lot of manpower to setup. This is what that setup looks like.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-build-wide.JPG">

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-party-dancing.jpg">

<h6>This photo and a few others below are by <a href="https://www.facebook.com/laurel.daily">Daily Swa Laurel</a></h6>

<h2>How the electronics are made</h2>

Since the trees light up with your breath, we need to consider how the breath is sensed and then how the thousands of LEDs are driven. 

These are five stages to making the electronics work together:

<ol>
<li><a href="#sensor">Designing a breathing sensor</a></li>
<li><a href="#main">Making the main control board</a></li>
<li><a href="#dispatcher">Driving high current LEDs with a custom lighting board</a></li>
<li><a href="#firmware">Writing the firmware</a></li>
<li><a href="#power">Powering ten trees in Grove</a></li>
</ol>

<h3 id="sensor">1. Designing a breathing sensor</h3>

First things first, we need to focus on how to design a breathing sensor. 

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-flower-breathe.jpg">

#### The plastic lotus flower assembly

This is the plastic lotus flower assembly built and designed by <a href="https://cambridge.nuvustudio.com/studios/long-term-projects/grove-burning-man#tab-portfolio-url">the NuVu team in Boston</a>. It is supported by a 3 foot gooseneck that is tied to the base of the tree. This allows the person sitting down by the tree to pull the flower, that at this point is lit up and has magically opened itself, over to their mouth.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-flower-open.png">

We placed a pair of <a href="https://www.adafruit.com/product/189">passive IR motion sensors</a> a few feet up the base of the tree looking out on both sides to detect when somebody sits down. That signal then directs the servo motor in the flower to open the flower up and make the LEDs inside the flower pulsate. This beckons the person to pull the flower over to them.

The flower has a proximity sensor embedded inside that is more commonly used by paper towel dispensers to detect hand movement. We used the [Si1143](https://moderndevice.com/product/si1143-proximity-sensors/), same as in <a href="http://www.ofbrooklyn.com/2014/09/6/building-pulse-bloom-biofeedback-burning-man-2014/#sensors">the pulse sensor in Pulse &amp; Bloom</a>, to detect proximity. When we detect that a person is positioned directly in front of the flower, we then allow the breath measurements to light up the tree. Otherwise wind would take over and the tree would be constantly lit.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/prototyping-sensor.jpg">

Above you can see the board that is placed inside the flower. There is a trumpet that fits directly over the board and directs airflow over the board. There are two slots in the board that allow your breath to flow over the hot-wire thermistors and out the back of the flower. Otherwise when you breathed into the flower, the flower would send your last breath back out.

<a href="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-pcb-sensor.png"><img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-pcb-sensor.png"></a>

The sensor board and the main board are driven and controlled by their own Teensy 3.2. I cannot say enough good things about the Teensy. We originally used an 8-bit Arduino Uno compatible ATmega328p chip but found the 8K memory limiting when we wanted to address thousands of LEDs at once.

<a href="https://www.pjrc.com/teensy/index.html"><img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-teensy.jpg"></a>

The Teensy gives us plenty of head room and it was easy to get a <a href="https://github.com/samuelclay/grove/blob/master/firmware/sensor/Makefile">GCC-based Makefile deployment setup</a> so all we had to do was run one <code>make</code> command and the board was flashed and rebooted.

#### Detecting your breath

Now we get to the heart of the matter. To detect your breathing, we turn to the <a href="https://moderndevice.com/product/wind-sensor/">Modern Device wind sensor</a>. They use what's called the "hot-wire" technique. This involves heating a couple of thermistors to a constant temperature and then measuring the electrical power required to maintain the heated thermistor at temperature as wind cools it down. The electrical power is directly proportional to the square of the wind speed. 

You can buy anemometers for hundreds of dollars but we made our own following the Modern Device wind sensor. Hot-wire anemometers excel at low wind speed, which is pretty much the same speed as breathing.

While out on the playa we discovered that the plastic trumpet, which is used to channel your breath toward the sensor while keeping out wind, would cover a bit too much of the proximity sensor. We solved this problem by adding ultrasonic sensors (thanks to Frys for letting us buy out their collection of ultrasonic sensors on the way to the burn), pictured below on top of the orange trumpet.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/IMG_9930.jpg">

We spent a couple days adding these ultrasonic sensors into the boards, soldering in the desert and making do with what we had. Thankfully we left a few pins open that we could then use for the new and improved proximity sensors.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/build-severin-soldering.jpg">

You can explore <a href="https://github.com/samuelclay/grove/blob/master/firmware/sensor/src/sensor.cpp">the code we used to sense your breath on Github</a>. There's a few parts that I'll highlight below in the <a href="#firmware">writing the firmware section</a>.

<h3 id="main">2. Making the main control board</h3>

This is the board that talks to the sensor board and the dispatcher board and gets all of the LED strips plugged into it. This is where the main battery connects to the tree and where power is distributed to each of the sensors and LEDs. This board also communicates with the dispatcher board up top in the leaves to make the high current LEDs fade between colors.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-mainboard.jpg">

You'll notice on the left is an <a href="https://www.aliexpress.com/item/2016-Brand-New-1pcs-Step-down-Power-DC-DC-CC-CV-Buck-Converter-Supply-Module-7/32608517078.html">8A DC-to-DC step-down voltage regulator</a> that brought the 12V down to 5V needed for the LED strips and sensor board. The dispatcher board and its 16 high current LEDs needs the full 12V. We originally used a cheaper 3A voltage regulator, but it turns out that the number of LEDs we had on at any given time would regularly hit 5A, so we had to boost the voltage regulator.

<a href="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-pcb-main.png"><img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-pcb-main.png"></a>

You should also note that we used a Teensy here as well. There are some protections built into the circuit to prevent burning out the Teensy if we happen to short somewhere. Thankfully this didn't happen, but we made the Teensy removable and replaceable in case it did.


All of the wire-to-board connectors are <a href="https://www.digikey.com/catalog/en/partgroup/mta-100-series/2660">MTA100 Series female</a> and <a href="https://www.digikey.com/catalog/en/partgroup/mta-100-series/9332">male pin headers</a>. They are an inexpensive connector that you can crimp onto AWG 22 gauge wires and then easily insert into 0.1" male header pins. They even include an optional polarity wedge on the side so that you can ensure the wires are always plugged in the right direction, which is especially helpful when you have people helping you out and you want to ensure that no mistakes are even possible.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-crimp.jpg">

Crimping the MTA100 headers to the wires is pretty fast. You can use either a <a href="http://www.newark.com/te-connectivity-amp/59803-1/insertion-tool/dp/98F2821">$30 insertion tool</a> or a <a href="https://www.digikey.com/product-detail/en/te-connectivity-amp-connectors/58074-1/A2031-ND/30197">$100 crimping tool</a> with a <a href="https://www.digikey.com/products/en?mpart=58246-1&v=17">$163 MTA100-specific crimping head</a>.

The best part about the MTA100 is that the wires are removable, so if you make a mistake you can just pull the wire out of the crimped head and try again. 

Sometimes the connections wouldn't take and they would have to be re-crimped. This happened on a few of the trees. In the future what we would have done is add circuit testing to the mainboard. This would be an in circuit current measurement sensor. On boot we would turn each of the LEDs on individually, sensing whether or not the LEDs are actually drawing current. This way we can identify improperly crimped LEDs (or just plain old broken LEDs) and turn on a status LED on the board to quickly check.

<h3 id="dispatcher">3. Driving high current LEDs with a custom lighting board</h3>

That brings us to the dispatcher board on top. The goal is to have 16 individual 3W ultra-bright LEDs on top of the tree light up as each breath climbs to the top of the tree. These high current LEDs look like they are effectively breathing, turning your breath into the breath of an entire tree. It's a magical effect and to pull it off we're going to need a custom board just to handle these tricky LEDs.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/prototyping-leds.jpg">

Last time with Pulse &amp; Bloom we didn't have a dispatcher board, instead relying on driving the LEDs with loose wires connected directly to PicoBucks. It was a mess. Here's the wiring diagram just for the 9 high current LEDs.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/Pulse%20%26%20Bloom%20-%20Petal%20LEDs%20wiring.png">

This means that there are over a hundred wires (6 per LED) per tree.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/Pulse%20%26%20Bloom%20-%20wired%20picobuck.jpg">

We decided instead to make a board that not only could handle all of this wiring mess but also allow us to easily change out the PicoBucks if they shorted, which is something that happened surprisingly often until we realized that the factory solder jobs on the LEDs themselves could sometimes short.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/prototyping-dispatcher.jpg">

You can see from the schematic below that we simplified the setup by hooking up a set of four high current LEDs per PicoBuck. This let us individually address four sets of lights, giving the tree a mesmerizing pattern of lights that would slowly breathe on their own in green, turning blue when filled with "oxygen" from somebody sitting down and breathing into the breathing sensor at the base of the tree.

<a href="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-pcb-dispatcher.png"><img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-pcb-dispatcher.png"></a>

We also added protection fuses to the dispatcher board in case the LEDs did short. Since each LED draws a quarter amp at 12 V, we needed to make sure that they would be protected. 

There is also a 12 channel SPI DAC. Since the PicoBucks need an analog signal as input to specify the PWM-enabled brightness on the LEDs, we couldn't easily send an analog signal up from the main board since it would have to traverse over 5 meters and be subject to massive voltage drop. Instead we sent a digital signal and converted it to analog on top. This was easy and inexpensive to do with the <a href="http://www.digikey.com/product-detail/en/rohm-semiconductor/BH2221FV-E2/BH2221FV-E2CT-ND/1158686">$4 BH2221FV chip from Rohm</a>.

<h3 id="firmware">4. Writing the firmware</h3>

There are two boards that need their own firmware loaded on to their own Teensy. The <a href="https://github.com/samuelclay/grove/tree/master/firmware/sensor">sensor board</a> and the <a href="https://github.com/samuelclay/grove/tree/master/firmware/main">main board</a> can both be found on Github.

#### The sensor board

Let's go over a few of the more interesting functions that are used to light up your breath.

{% highlight C %}
void loop() {
    readRemoteState();
    updateLEDs();
    updateFlowerServo();
    updatePIR();

    runWindAvgs();
    updateProx();

    evaluateState();
    runBreathDetection();
}
{% endhighlight %}

To begin, the sensor board runs through a tight loop looking for the proximity and PIR motion sensors to trigger so that it can begin to read breath measurements. If the proximity sensor is not firing then that means nobody is in front of the front and we should not be showing any of the breath measurements we might be reading due to wind. 

If we didn't have a working proximity sensor (which happened to a few trees) then we would actually just be showing the Earth breathing, otherwise known as the wind. The Earth breathes differently than you or me. Instead of long pulses of hot air, the wind shows up as a sustained line of many tiny pulses, since it's both cooler and smoother than your breath.

Next we have a finite state machine determine which state we're in. The choices are neutral, motion detected, and proximity detected. 

{% highlight C %}
void evaluateState() {
    switch (overallState) {
        case STATE_NEUTRAL: {
            if (pirState == PIR_ON) {
                overallState = STATE_OPEN;
                openFlower();
            }
            break;
        }
        case STATE_OPEN: {
            long now = millis();
            if (now - openTimeoutLastEvent > openTimeout) {
                overallState = STATE_NEUTRAL;
                closeFlower();
            } else if (isProx()) {
                overallState = STATE_PROX;
            }
            break;
        }
        case STATE_PROX : {
            if (remoteState == STATE_NEUTRAL) {
                overallState = STATE_NEUTRAL;
                closeFlower();
            } else if (!isProx()) {
                overallState = STATE_OPEN;
                breathOff();
            } else {
                runBreathDetection();
            }
            break;
        }
    }
}
{% endhighlight %}

Using a FSM makes it easy to ensure that we always know where we are, even with three separate sensors that all trigger independently of each other, while ensuring that one does not cause a change in the tree without its predecessors.

{% highlight C %}
void runWindAvgs() {
    long now = millis();
    if (now - lastWindSampleTime > windSampleInterval) {
        // Currently tuned to sample every 20ms roughly
        int raw = getRawWind();

        lowWindAvg = lowWindAvg * lowWindAvgFactor + raw * (1 - lowWindAvgFactor);
        highWindAvg = highWindAvg * highWindAvgFactor + raw * (1 - highWindAvgFactor);

        lastBpassWind = bpassWind;
        bpassWind = (int)(highWindAvg-lowWindAvg);
        windHistory[windHistoryIndex++] = bpassWind - lastBpassWind;

        if (windHistoryIndex >= WIND_HIST_LEN) windHistoryIndex = 0;

        lastWindSampleTime = now;
    }
}
{% endhighlight %}

We use the above `runWindAvgs` to average the raw readings and establish a moving average with hysteresis. This means that we want to intentionally avoid rapid switching of states, so we have upper and lower thresholds that move with the average.

#### The main control board

Next we come to the main board. Let's walk through the steps. Instead of showing the code from the main board, I'm going to talk about the various functions. You can view <a href="https://github.com/samuelclay/grove/blob/master/firmware/main/src/grove.cpp">all of the main board's code on Github</a>.

{% highlight C %}
void loop() {
    addRandomDrip();
    advanceRestDrips();

    updatePIR(0);
    updatePIR(1);
    transmitSensor();
    receiveSensor();

    #ifdef RANDOMBREATHS
    if (millis() % (60 * 1000) < 5000) {
        addBreath();
    }
    #else
    if (proximityState == STATE_PIR_ACTIVE && detectedBreath) {
        addBreath();
    }
    #endif
    advanceBreaths();

    runLeaves();
    runBase();

    leds.show();    
}
{% endhighlight %}

What's going to happen is that the tree will randomly add "drips" to the top of the tree. 

{% highlight C %}
addRandomDrip();
advanceRestDrips();    
{% endhighlight %}

These drips are a random length with a random green-tinted color. They will use easing equations to slowly but rhythmically drip down the tree. The effect is that the trees are swimming in their own green waves.

{% highlight C %}
updatePIR(0);
updatePIR(1);
transmitSensor();
{% endhighlight %}

When a person sits down at the base of the tree, the PIR motion sensor fires. We then send this signal over to the sensor board, which then opens up the flower using a servo motor and changes the color of the flower.        

{% highlight C %}
receiveSensor();
{% endhighlight %}
        
The sensor then sends back data about the proximity sensor and the detected breaths.

{% highlight C %}
#ifdef RANDOMBREATHS
if (millis() % (60 * 1000) < 5000) {
    addBreath();
}
#else
if (proximityState == STATE_PIR_ACTIVE && detectedBreath) {
    addBreath();
}
#endif
{% endhighlight %}

Once a breath is detected, we add the head of the breath to the bottom of the tree and guide it upwards.

{% highlight C %}
advanceBreaths();
{% endhighlight %}

The high current LEDs in the leaves are glowing in randomly paced greens. 

{% highlight C %}
runLeaves();
runBase();
{% endhighlight %}

When the head of the breath reaches the top of the tree, the high current LEDs then begin to glow in a whiteish blue. This signals that the tree is breathing at the same pace as the person sitting underneath it.

{% highlight C %}
leds.show();
{% endhighlight %}

Since we've queued up all of the LEDs, it's now time to send the data over the line and update the tree for this loop. There will be dozens of loops per second, enough to make the tree's many LEDs look fluid in their motion.

#### The dispatcher board

Finally, because we're using a 12 channel SPI DAC on the dispatcher so that we can send digital signals up the long trunk of the tree to later be converted to analog signals used to set brightness of the high current LEDs, we need to make the simple transactions over SPI.

{% highlight C %}
/**
 * Set the analog output on the dispatcher board.
 * Channels are numbered 1 to 12 inclusive (THEY DON'T START AT ZERO !!) 
 * value is 0-255 range analog output of the dac/LED brightness
 */
void dispatcher(uint8_t chan, uint8_t value) {
    // We could normalize here to a "real" range
    // There's nothing below 45 because below 0.5 the pico buck is off
    // value = value * 210 / 255;
    // if (value > 0) value += 45;

    // take the SS pin low to select the chip:
    SPI.beginTransaction(dispatcherSPISettings);

    digitalWrite(slaveSelectPin, LOW);
    //  send in the address and value via SPI:
    SPI.transfer(flipByte((chan & 0x0F) << 4));
    SPI.transfer(value);
    // take the SS pin high to de-select the chip:
    digitalWrite(slaveSelectPin,HIGH);

    SPI.endTransaction();
}
{% endhighlight %}

<h3 id="power">5. Powering ten trees in Grove</h3>

Running an electronics installation out in the desert presents a few power problems. First is that there is nowhere to plug in, so all of the energy you're going to need, whether it is stored or rechargeable, is going to have to be brought out there on the playa with you.

We quickly decided on running the installation on solar-powered deep cycle batteries. The cost for the batteries was mitigated slightly by the fact that we already had a 1.2 kW solar array handy. In past years you could affordably rent solar arrays from non-profits (like Black Rock Solar, who have written about <a href="http://www.blackrocksolar.org/news/2015/solarize-the-playa/">how to solarize your playa art installation</a>), but changes in Nevada's energy policy have meant that's no longer an option. It's kind of tragic and the <a href="https://www.nytimes.com/2016/02/01/opinion/nevadas-solar-bait-and-switch.html">New York Times recently covered how Solar City had to move out of the state</a>.

The other option is to use a generator, but while relatively cheap, they are loud and would detract from the serenity of the installation. We could instead choose to run a generator in a baffle box and run AC power over a length 50 meter distance, but that was deemed un-Grove-like and we stuck with batteries.

Let's take a look at what's on the market.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-batteries.png" style="border: none">

Most batteries cost around 20 cents per Watt-hour. Let's perform some calculations to figure out how much we need. Let's look at a single tree. Most of the time a tree is going to be in a "rest" state, where nobody is actively using it. This means the tree is draped in green and the high current LEDs are in a lower power state. 

About 5% of the time we're going to be in active mode, with brighter LED colors on the 4 × 5 meter strips and 16 × high current LED colors.

     95% × ((4 LED strips × 1.50A @ 5V per strip) + (0.25A @ 5V base lighting) + (16 × 0.08A @ 12V))
    + 5% × ((4 LED strips × 1.75A @ 5V per strip) + (0.25A @ 5V base lighting) + (16 × 0.10A @ 12V))

    = 0.95 * (4*1.5*5 + .25*5 + 16*.08*12) + 0.05 * (4*1.75*5 + .25*5 + 16*.1*12)

    ≈ 47W per tree

At 10 trees, that's 470 watts of power. We expect the installation to run 10 hours (8pm - 6am). That's 4,700 Watt-hours. We're looking at a set of batteries that should cost (4700 Wh × $0.20/Wh) = $940.

What we did was put 3 6V 250 Ah batteries in series to boost it up to 18V instead of just using 2 6V batteries at 12V. We did this to limit the DC voltage drop between the battery array and the trees, each of which was between 10 and 20 meters away from the battery array. Since voltage drop is linear with respect to distance, the reduction from 18V to ~15V is a 16% drop but 12V to ~9V is a 25% drop. This prevents the high current LEDs from flickering, since they need a minimum of 10V to work.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/build-solar-array.jpg">

We charged the batteries using Luke's solar array that he just happened to have handy. Here's Luke on the challenges we faced:

> Sam and I had a few 5-minute discussions about how much power we needed, and this was inadequate: our installation often ran out of power around sunrise. I should have brought twice as many batteries and 1.5x the solar panels. By dumb luck, this 'low power mode' produced an interesting 'dead red' effect: the batteries at lowest levels provided only enough power for the red leds to pulse, leaving out all other colors. Unfortunately, the batteries needed desulfated for a month straight after playa and a few were still killed.

> In the future, we'll test *the actual power consumption* of our installation in the real world: with a kill-a-watt or other power meter, how much is your installation actually drawing over the course of 24 hours? Your battery capacity should be at least 4x this: 2x to keep from discharging more than 50%, and another 2x for when somebody (in our case, me) imbibes too much and forgets to move batteries to solar array until noon.</blockquote>

<h2>Installing the Installation</h2>

Before the trees go up we need to assemble them and give them a coat of spray paint. These trees are shaped steel tubes that need some gold applied.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/oakland-trees.jpg">

All of the work is done at American Steel Studios in Oakland, California. We want to do as much work as possible before we get to the playa. Once we're in the desert, anything we may need is going to be 6 hours round trip to Reno, whereas the Home Depot in Oakland is a 5 minute drive away.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/build-electronics-behind.jpg">

Alas, as much as we try to avoid it, there's plenty of firmware debugging to be done on the playa.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/build-severin-heather.jpg">

Naturally, firmware debugging often lasted well into the night.

Putting the trees up is also a ton of work. We prototyped the leaves at a small scale.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-petals-small.jpg">

But once on the playa we realize it's a lot more work to attach 16 individual leaves to each of the 10 trees simply as a matter of scale.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-leaf.jpg">

The trees go up a lot faster than individual subassemblies on the tree. This is a good photo of the Pareto principle for art installations. Putting up the first 80% of the installation by volume only took 20% of the time.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/build-trees.jpg">

<h2>Enjoying the fruits of our labor</h2>


<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-breathing-couple.jpg">
<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-breathing-daytime.jpg">
<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-brittany-breathing-2.jpg">

It's dusty out there!

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/teardown-tornado.jpg">

And as we did with Pulse &amp; Bloom, these cushions are some of the only seating on the playa, offering a beautiful respite and place to recharge and re-energize from the heat of the playa.

<img src="http://static.newsblur.com.s3.amazonaws.com/ofbrooklyn/grove/grove-party-dusty.jpg">

The entire process lasted 3 months and involved 5 people on the electronics team, a half dozen people on fabrication, and another dozen people on assembly and installation. My hope is that others learn from our work and use some of the <a href="https://github.com/samuelclay/grove/">open-source firmware and designs</a> for their own art installations. 

If you'd like to bring Grove to your art or music festival, please contact <a href="mailto:shilo1221@gmail.com">Shilo Shiv Suleman</a>.

I'd love to hear from you if you're inspired or build your own art installation. <a href="https://twitter.com/samuelclay">Reach me @samuelclay on Twitter</a>.

<i>breath (n), breathe (v)</i>
