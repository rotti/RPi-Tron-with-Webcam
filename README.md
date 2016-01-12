Rottis RPi-Tron-Radio Clone
=============================
All kudos should go to the initial project. I just forked it and made some further improvements (see below).

[![Flattr this git repo](http://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?\user_id=5Volt-Junkie&url=https://github.com/5Volt-Junkie/RPi-Tron-Radio&title=RPi-Tron-Radio&\description=Raspberry_Pi_Internet_Radio&language=&\tags=github&category=software)

![Player](https://raw.githubusercontent.com/5Volt-Junkie/RPi-Tron-Radio/master/docu/RPi-Internet-Radio.png)

Small web radio with Raspberry Pi B+ and 2.8" 320x240 TFT Touchscreen. The interface of the web radio was written in python/pygame.

Watch demo video on YouTube.com: https://www.youtube.com/watch?v=QzvNIHI-k-4

See the [Installation guide](https://github.com/5Volt-Junkie/RPi-Tron-Radio/blob/master/docu/Installation.md)

Also, you can visit the German Raspberry Pi Forum, where some guys made a bunch of fancy improvements.
[http://www.forum-raspberrypi.de/Thread-rpi-tron-radio-raspberry-pi-webradio-im-tronstyle](http://www.forum-raspberrypi.de/Thread-rpi-tron-radio-raspberry-pi-webradio-im-tronstyle)


Important: I'm testing it with [soma.fm streams] (http://somafm.com/) only. I don't know how good it works with another stations.
Additional note: Works fine for the other stations I wanted. See 'add\_stations.sh' for my stations.

## Original Features
* RPi-Tron-Radio runs through mpd and mpc.
* 8 skin colors
* Displays station data
* Displays current playing song
* Displays volume in %
* Displays time and date
* Displays IP address
* Displays CPU temp
* Screensaver (screen burn prevention)
* Can write the title of the current song to the text file.
 

* Buttons:
Menu 1
  * Play
  * Pause
  * Volume Up
  * Volume Down
  * Mute
  * Next
  * Previous
  * -> Menu 2

  * Fav
  * Switch skin color
  * Run stream in background
  * Close/stop radio
  * Poweroff
  * Reboot
  * Reserved for on/off RGB-LED
  * -> Menu 1



## Added Features
* Display weather data:
  * New skin
  * Use API from openwaethermap.org
  * Current weather for your location
  * Forecast for your location
  * Location can be set via ID from openweathermap.org
  * Reload function
  * Runs on screen 2
* Radio Player
  * Pause is now Pause/Play
  * Unmute restores set volume
  * Hidden button (upper left to the middle) to favorite song
  * Favorite a song stores metadata (time, date) with song title
* Status Screen
  * Used and free memory
  * CPU usage in %
  * Number of running processes
  * Disk free in % of /
  * Runs on screen 3
* Confirmation Screen. We want to be sure for
  * shutdown
  * reboot
  * quit
  * run background


##Openweather
The Openweather API wants a key. For my own privacy reasons i wont push it up to github. The python script looks for the key in the file "openweather.key" in the same directory the radio script runs.


##Known Issues
* Because graphics isn't my business there is no color switch for weather and confirmation screen.
* The image "Jessie" images listed on https://github.com/watterott/rpi-display made problems with the resolution. Better stay on "Wheezy"
  

## Further tipps
I installed [ympd](https://gist.github.com/nerab/37429abeaf4828484ab7) to get a small web service for the mpd. So I can operate the radio with my smartphone (or every other device with a web browser).
