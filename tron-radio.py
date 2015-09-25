"""
RPi-Tron-Radio Clone ... added some more features (weather, confirmation, ...)

BIG THANKS TO:
Raspberry Pi Web-Radio with 2.8" TFT Touchscreen and Tron-styled graphical interface
GitHub: http://github.com/5volt-junkie/RPi-Tron-Radio
Blog: http://5volt-junkie.net

MIT License: see license.txt

"""

import pygame
from pygame.locals import *
import time
import datetime
import sys
import os
import glob
import subprocess
import re
import requests
import json
import urllib2

os.environ["SDL_FBDEV"] = "/dev/fb1"
os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
os.environ["SDL_MOUSEDRV"] = "TSLIB"

#colors     R    G    B
white   = (255, 255, 255)
red     = (255,   0,   0)
green   = (  0, 255,   0)
blue    = (  0,   0, 255)
black   = (  0,   0,   0)
cyan    = ( 50, 255, 255)
magenta = (255,   0, 255)
yellow  = (255, 255,   0)
orange  = (255, 127,   0)

#my vars. usally for counters
vol_set = "0" 
wd_count = 0 #0 if we have not looked up for new wd
wd = "" #weater_data
fc = "" #forecast_data
confirm_reason = "" #reboot, halt, quit, background
weather_id = "2871198" #there is no place like 127.0.0.1

#screen size
width  = 320
height = 240
size = (width, height)
screen = pygame.display.set_mode(size)

pygame.init()

#disable mouse cursor
pygame.mouse.set_visible(False)

#define font
font = pygame.font.Font(None, 25)

#screensaver 
screensaver_timer = 2     #time until screensaver will be enabled, in minutes
screensaver = False

#load default skin
menu = 1
skin_number = 1
max_skins = 8
font_color = cyan
skin1 = pygame.image.load("skins/skin_tron_m1.png")
skin2 = pygame.image.load("skins/skin_tron_m2.png")
skin3 = pygame.image.load("skins/skin_tron_m3.png")
skin4 = pygame.image.load("skins/skin_confirm.png")
skin = skin1

screen.blit(skin, (0, 0))

#initial volume settings
subprocess.call('mpc volume 100' , shell=True)

reboot_label = font.render("rebooting...", 1, (font_color))
poweroff_label = font.render("shutting down", 1, (font_color))

song_title = " "
playlist = " "

#functions
def internet_on():
    try:
       #response=urllib2.urlopen('http://173.194.40.247', timeout=1)
       response=urllib2.urlopen('http://www.google.com', timeout=1)
       return True
    except urllib2.URLError as err: pass
    return False


def execute_action(action):
    if action == "background":
       run_background()
    if action == "quit":
       quit_radio()
    if action == "halt":
       poweroff()
    if action == "reboot":
       reboot()


def poweroff():
    screen.fill(black)
    screen.blit(poweroff_label, (10, 100))
    pygame.display.flip()
    time.sleep(5)
    subprocess.call('mpc stop' , shell=True)
    subprocess.call('poweroff' , shell=True)


def reboot():
    screen.fill(black)
    screen.blit(reboot_label, (10, 100))
    pygame.display.flip()
    time.sleep(5)
    subprocess.call('mpc stop' , shell=True)
    subprocess.call('reboot' , shell=True)


def quit_radio():
    subprocess.call('mpc stop', shell=True)
    pygame.quit()
    sys.exit()


def run_background():
    pygame.quit()
    sys.exit()


def get_forecast():
    global fc
    if internet_on():
       request = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?id=' + weather_id, '&units=metric')
       fc = request.json()
    return fc


def get_weather():
    global wd
    if internet_on():
       request = requests.get('http://api.openweathermap.org/data/2.5/weather?id=' + weather_id, '&units=metric')
       wd = request.json()
    return wd


def show_confirm(action):
    if action == "background":
       reason = "Do you want to SEND BACKGROUND?"
    if action == "quit":
       reason = "Do you want to QUIT?"
    if action == "halt":
       reason = "Do you want to SHUTDOWN?"
    if action == "reboot":
       reason = "Do you want to REBOOT?"

    skin = skin4
    screen.blit(skin, (0, 0))
    confirm = font.render(reason, 1, (font_color))
    screen.blit(confirm, (17, 150))


def show_weather(fc, wd):
    skin = skin3
  
    day1_temp_day = fc['list'][1]['temp']['day']
    day2_temp_day = fc['list'][2]['temp']['day']
    day3_temp_day = fc['list'][3]['temp']['day']
    day1_condition = fc['list'][1]['weather'][0]['description'] 
    day2_condition = fc['list'][2]['weather'][0]['description'] 
    day3_condition = fc['list'][3]['weather'][0]['description'] 

    location = wd['name']
    temp_now = wd['main']['temp']
    temp_min_now = wd['main']['temp_min']
    temp_max_now = wd['main']['temp_max']
    wind_now = wd['wind']['speed']
  
    title = font.render("Day temp. (12:00) with condition ", 1, (font_color))
  
    day1_temp_day = font.render("+1 Days: " + unicode(day1_temp_day), 1, (font_color))
    day2_temp_day = font.render("+2 Days: " + unicode(day2_temp_day), 1, (font_color))
    day3_temp_day = font.render("+3 Days: " + unicode(day3_temp_day), 1, (font_color))
    day1_condition = font.render(unicode(day1_condition), 1, (font_color))
    day2_condition = font.render(unicode(day2_condition), 1, (font_color))
    day3_condition = font.render(unicode(day3_condition), 1, (font_color))

    location = font.render("Weather in: "+ location, 1, (font_color))
    temp_now = font.render("Temperature: " + unicode(temp_now), 1, (font_color))
    temp_min_now = font.render("Temp. min: " + unicode(temp_min_now), 1, (font_color))
    temp_max_now = font.render("Temp. max: " + unicode(temp_max_now), 1, (font_color))
    wind_now = font.render("Wind speed: " + unicode(wind_now), 1, (font_color))
            
    screen.blit(skin, (0, 0))
    screen.blit(title, (17, 15))
 
    screen.blit(day1_temp_day, (17, 40))
    screen.blit(day2_temp_day, (17, 60))
    screen.blit(day3_temp_day, (17, 80))
    screen.blit(day1_condition, (150, 40))
    screen.blit(day2_condition, (150, 60))
    screen.blit(day3_condition, (150, 80))
 
    screen.blit(location, (17, 130))
    screen.blit(temp_now, (17, 150))
    screen.blit(temp_min_now, (17, 170))
    screen.blit(temp_max_now, (17, 190))
    screen.blit(wind_now, (17, 210))



#copy playing title to favorite.txt and add metadata like date   
def favorite():
    #print song_title
    
    f = open ('/var/www/favorite.txt' , 'a')
    timestamp = time.strftime("%c")
    f.write(timestamp + ' - ' + song_title + '\n')
    f.close()


#function runs if touchscreen was touched (and screensaver is disabled)
def on_touch():
      #x_min           x_max   y_min            y_max
    if  13 <= pos[0] <=  75 and 121 <= pos[1] <= 173:
        #print "button1 was pressed"
        button(1)

    if  90 <= pos[0] <= 152 and 121 <= pos[1] <= 173:
        #print "button2 was pressed"
        button(2)

    if 167 <= pos[0] <= 229 and 121 <= pos[1] <= 173:
        #print "button3 was pressed"
        button(3)

    if 244 <= pos[0] <= 306 and 121 <= pos[1] <= 173:
        #print "button4 was pressed"
        button(4)            
        

    if  13 <= pos[0] <=  75 and 181 <= pos[1] <= 233:
        #print "button5 was pressed"
        button(5)

    if  90 <= pos[0] <= 152 and 181 <= pos[1] <= 233:
        #print "button6 was pressed"
        button(6)

    if 167 <= pos[0] <= 229 and 181 <= pos[1] <= 233:
        #print "button7 was pressed"
        button(7)

    if 244 <= pos[0] <= 306 and 181 <= pos[1] <= 233:
        #print "button8 was pressed"
        button(8)

    #button 9 is bigger than the others
    if 13 <= pos[0] <= 152 and 11 <= pos[1] <= 113:
        #print "button9 was pressed"
        button(9)

    if 90 <= pos[0] <= 152 and 36 <= pos[1] <= 87:
        #print "button10 was pressed"
        button(10)

    if 167 <= pos[0] <= 229 and 36 <= pos[1] <= 87:
        #print "button11 was pressed"
        button(11)

#which button (and which menu) was presed on touch            
def button(number):
        global menu
        global confirm_reason
        
        if menu == 1:
            if number == 1:
                subprocess.call('mpc play' , shell=True)
                #print "play"

            if number == 2:
                lines = subprocess.check_output('mpc', shell=True).split("\n")
                status = re.search(r"\[(\w+)\]", lines[1])
                status = status.group(1)
                if status == "playing":
                   print "pausing"
                   subprocess.call('mpc pause' , shell=True)
                   #print "pause"
                if status == "paused":  
                   print "playing"
                   subprocess.call('mpc play' , shell=True)

            if number == 3:
                subprocess.call('mpc volume +5' , shell=True)
                #print "vol +x"

            if number == 4:
                lines = subprocess.check_output('mpc volume', shell=True).split("\n")
                vol_string = re.findall('\d+', lines[0])
                vol_value = vol_string[0]
                global vol_set

                #when muted restore original volume
                if vol_value == "0":
                   subprocess.call('mpc volume ' + vol_set + '' , shell=True)
                else: 
                   vol_set = vol_value
                   subprocess.call('mpc volume 0' , shell=True)
                   #print "vol 0"

            if number == 5:
                subprocess.call('mpc prev' , shell=True)
                #print "prev"

            if number == 6:
                subprocess.call('mpc next' , shell=True)
                #print "next"

            if number == 7:
                subprocess.call('mpc volume -5' , shell=True)
                #print "vol -x"

            if number == 8:
                #print "go to menu 2"
                menu = 2
                update_screen()
                return
            
            if number == 9:
                favorite()


        if menu == 2:
            if number == 4:
                get_weather()
                get_forecast()
                update_screen()

            if number == 8:
                #print "go to menu 1"
                menu = 3
                update_screen()
                return


        if menu == 3:
            if number == 1:
                favorite()

            if number == 2:
                #print "switch skin"
                global skin_number
                skin_number = skin_number+1
                #print skin_number
                update_screen()

            if number == 3:
                confirm_reason = "background"
                menu = 4
                update_screen()
                return

            if number == 4:
                confirm_reason = "quit"
                menu = 4
                update_screen()
                return

            if number == 5:
                print "power off"
                confirm_reason = "halt"
                menu = 4
                update_screen()
                return

            if number == 6:
                print "reboot"
                confirm_reason = "reboot"
                menu = 4
                update_screen()
                return

            if number == 7:
                print "update screen"
                update_screen()

            if number == 8:
                #print "go to menu 1"
                menu = 1
                update_screen()
                return
       

        if menu == 4:
            if number == 10:
                print "execute the stuff"
                execute_action(confirm_reason)
            
            if number == 11:
                #print "go to menu 3"
                confirm_reason = ""
                menu = 3
                update_screen()
                return



        
#function to update screen
def update_screen():
    global skin_number
    if skin_number == 9:
        skin_number = 1
        
    if skin_number == 1:
        skin1 = pygame.image.load("skins/skin_tron_m1.png")
        skin2 = pygame.image.load("skins/skin_tron_m2.png")
        font_color = cyan
    if skin_number == 2:
        skin1 = pygame.image.load("skins/skin_blue_m1.png")
        skin2 = pygame.image.load("skins/skin_blue_m2.png")
        font_color = blue
    if skin_number == 3:
        skin1 = pygame.image.load("skins/skin_green_m1.png")
        skin2 = pygame.image.load("skins/skin_green_m2.png")
        font_color = green
    if skin_number == 4:
        skin1 = pygame.image.load("skins/skin_magenta_m1.png")
        skin2 = pygame.image.load("skins/skin_magenta_m2.png")
        font_color = magenta
    if skin_number == 5:
        skin1 = pygame.image.load("skins/skin_orange_m1.png")
        skin2 = pygame.image.load("skins/skin_orange_m2.png")
        font_color = orange
    if skin_number == 6:
        skin1 = pygame.image.load("skins/skin_red_m1.png")
        skin2 = pygame.image.load("skins/skin_red_m2.png")
        font_color = red
    if skin_number == 7:
        skin1 = pygame.image.load("skins/skin_white_m1.png")
        skin2 = pygame.image.load("skins/skin_white_m2.png")
        font_color = white
    if skin_number == 8:
        skin1 = pygame.image.load("skins/skin_yellow_m1.png")
        skin2 = pygame.image.load("skins/skin_yellow_m2.png")
        font_color = yellow
    
        
    global menu
    global confirm_reason

    if screensaver == False:
        
        current_time = datetime.datetime.now().strftime('%H:%M  %d.%m.%Y')
        time_label = font.render(current_time, 1, (font_color))
        
        if menu == 1:
            skin = skin1
            screen.blit(skin, (0, 0))
            
            lines = subprocess.check_output('mpc current', shell=True).split(":")
            if len(lines) == 1:
                line1 = lines[0]
                line1 = line1[:-1]
                station_label = font.render("Station: no data", 1, (font_color))

            else:
                line1 = lines[0]
                line2 = lines[1]
                line1 = line1[:30]
                station_label = font.render('Station: ' + line1 + '.', 1, (font_color))

            lines = subprocess.check_output('mpc -f [%title%]', shell=True).split("\n")
            line1 = lines[0]
            
            
            if line1.startswith("volume"):
                title_label = font.render("Title: no data! Try with PLAY!", 1, (font_color))
    
            else:
                line1 = lines[0]
                line2 = lines[1]
                global song_title
                song_title = line1
                line1 = line1[:30]
                
                title_label = font.render(line1 + '.', 1, (font_color))
                

            title = font.render("Now playing:", 1, (font_color))
            screen.blit(skin, (0, 0))
            screen.blit(station_label, (23, 15))

            screen.blit(title, (23, 40))
            screen.blit(title_label, (23, 60))

            screen.blit(time_label, (160, 90))

            lines = subprocess.check_output('mpc volume', shell=True).split("\n")
            line1 = lines[0]
            volume_label = font.render(line1, 1, (font_color))
            screen.blit(volume_label, (23, 90))
               
            pygame.display.flip()
            
    
        if menu == 2:
            skin = skin3

            global wd
            global fc
            global wd_count

            if wd_count == 0:
               wd = get_weather()
               fc = get_forecast()
               wd_count = 1

            #no data at all or empty wd string
            if (wd is None) or (not wd):  
               screen.blit(skin, (0, 0))
               nildata = font.render('no data available', 1, (font_color))
               screen.blit(nildata, (17, 150))
               pygame.display.flip()

            else:
               show_weather(fc, wd)
               pygame.display.flip()


        if menu == 3:
            skin = skin2
            
            screen.blit(skin, (0, 0))
            #get and display ip
            ip = subprocess.check_output('hostname -I', shell=True).strip()
            ip_label = font.render('IP: ' + ip, 1, (font_color))
            screen.blit(ip_label, (23, 15))

            #get and display cpu temp
            cpu_temp = subprocess.check_output('/opt/vc/bin/vcgencmd measure_temp', shell=True).strip()
            temp = font.render('cpu ' + cpu_temp, 1, (font_color))
            screen.blit(temp, (23, 35))
            
            #get and display ram
            ram = subprocess.check_output('/usr/bin/free -h | /bin/grep Mem', shell=True).split()
            ram = ram[0], '/'.join(ram[2:4])
            ram = str(ram)
            chars_to_remove = ['\'', '(', ')', ',']
            ram = ram.translate(None, ''.join(chars_to_remove))
            ram = font.render(ram, 1, (font_color))
            screen.blit(ram, (23, 55))

            #get current time
            screen.blit(time_label, (90, 90))

            #procs
            procs = subprocess.check_output('/bin/ps -e | /usr/bin/wc -l', shell=True).split()
            procs = font.render('Procs: ' + procs[0], 1, (font_color))
            screen.blit(procs, (165, 15))

            #cpu usage
            cpu = subprocess.check_output('/usr/bin/vmstat', shell=True).split()
            cpu = str(100 - int(cpu[36]))
            cpu = font.render('CPU usage: ' + cpu + '%', 1, (font_color))
            screen.blit(cpu, (165, 35))

            #diskfree
            df = subprocess.check_output('/bin/df -h .', shell=True).split()
            df = font.render('Disk: ' + df[11], 1, (font_color))
            screen.blit(df, (165, 55))
            
            pygame.display.flip()


        if menu == 4:
            print confirm_reason
            show_confirm(confirm_reason)
            pygame.display.flip()
        
       

    if screensaver == True:
        screen.fill(white)
        pygame.display.flip()


  
minutes = 0
#userevent on every 1000ms, used for screensaver
pygame.time.set_timer(USEREVENT +1, 60000)
subprocess.call('mpc play' , shell=True)
update_screen()
running = True

while running:
        
        for event in pygame.event.get():

            if event.type == USEREVENT +1:
                minutes += 1
            
            if event.type == pygame.QUIT:
                print "Quit radio"
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print "Quit radio"
                    pygame.quit()
                    sys.exit()

            #if screensaver is enabled and the screen was touched,
            #just disable screensaver, reset timer and update screen
            #no button state will be checked
            if event.type == pygame.MOUSEBUTTONDOWN and screensaver == True:
                minutes = 0
	        subprocess.call('echo 0 | sudo tee /sys/class/backlight/*/bl_power' , shell=True)
                screensaver = False
                update_screen()
                break
                
            #if screen was touched and screensaver is disabled,
            #get position of touched button, call on_touch(), reset timer and update screen
            if event.type == pygame.MOUSEBUTTONDOWN and screensaver == False:
                pos = (pygame.mouse.get_pos() [0], pygame.mouse.get_pos() [1]) 
                minutes = 0
                on_touch()
                update_screen()
                
        
        #enable screensaver on timer overflow
        if minutes > screensaver_timer:
            screensaver = True
	    subprocess.call('echo 1 | sudo tee /sys/class/backlight/*/bl_power' , shell=True)	
            update_screen()
            update_screen()
            time.sleep(0.1)
