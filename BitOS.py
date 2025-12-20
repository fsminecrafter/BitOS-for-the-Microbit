#BitOS made by fsminecrafter 2025-nov-20

AppmenuActive = True
digits = "0123456789"
Apps = ["Uninitialized"]
AppsLogos = ["09090:00000:00000:09990:90009"]
messages = ["Hello!", "(:", "):", "How are you doing?", "Isnt BitOS great!?", "Lets add some more messages..."]
appindex = 0
debug = False
ActiveApp = "None"

def char_to_int(c: str):
    i = 0
    while i < 10:
        if digits[i] == c:
            return i
        i += 1
    return 0

def Showimage(img: str):
    basic.clear_screen()
    for y in range(5):
        for x in range(5):
            idx = y * 6 + x
            val = char_to_int(img[idx])
            led.plot_brightness(x, y, val * 28)

def Boot():
    Showimage("90009:99099:90909:90009:00000")
    basic.pause(500)
    Showimage("90009:99099:90909:90009:90000")
    basic.pause(500)
    Showimage("90009:99099:90909:90009:99000")
    basic.pause(500)
    Showimage("90009:99099:90909:90009:99900")
    basic.pause(500)
    Showimage("90009:99099:90909:90009:99990")
    basic.pause(500)
    Showimage("90009:99099:90909:90009:99999")
    basic.pause(1000)
    return

def on_received_string(receivedString):
    basic.show_string(str(receivedString))

def GestureShake():
    if ActiveApp == "RadioChat":
        radio.send_string(messages[appindex])

def AppEntryPoint():
    global Apps
    global appindex
    global AppmenuActive
    global ActiveApp
    global messages
    AppmenuActive = False
    app = Apps[appindex]
    ActiveApp = app

    if app == "Flashlight":
        basic.show_leds("""
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            # # # # #
            """)
        led.set_brightness(255)
    elif app == "RadioChat":
        appindex = 0
        radio.set_group(1)
        radio.on_received_string(on_received_string)
    elif app == "Dice":
        basic.clear_screen()

def InitApplications():
    while len(Apps) > 0:
        Apps.pop()
    while len(AppsLogos) > 0:
        AppsLogos.pop()

def RegisterApplication(Name: str, Image: str):
    Apps.append(Name)
    AppsLogos.append(Image)

def Appmenu():
    basic.clear_screen()
    InitApplications()
    RegisterApplication("Flashlight", "90909:09090:90909:09090:90909")
    RegisterApplication("RadioChat", "99900:90090:90090:09990:00009")
    RegisterApplication("Dice", "00000:09090:09090:09090:00000")
    while True:
        if AppmenuActive:
            Showimage(AppsLogos[appindex])
        basic.pause(100)
    
def ExitApplication():
    global AppmenuActive
    global Apps
    global AppsLogos
    global appindex
    global debug
    global ActiveApp

    AppmenuActive = True
    appindex = 0
    debug = False
    ActiveApp = "None"


def AB_Button():
    global AppmenuActive
    if AppmenuActive == True:
        AppEntryPoint()
    else:
        ExitApplication()

def Left():
    global appindex
    global messages
    global ActiveApp
    global Apps
    appindex -= 1
    if appindex < 0:
        appindex = len(Apps) - 1
    if ActiveApp == "RadioChat":
        basic.show_string(str(messages[appindex]))

def Right():
    global appindex
    global messages
    global ActiveApp
    global Apps
    if appindex >= len(Apps) - 1:
        appindex = 0
    else:
        appindex += 1
    if ActiveApp == "RadioChat":
        basic.show_string(str(messages[appindex]))

def RollDice():
    Dice = randint(1, 6)
    basic.show_string(str(Dice))

def A_Button():
    if AppmenuActive == True:
        Left()
    elif ActiveApp == "RadioChat":
        Left()
    elif ActiveApp == "Dice":
        RollDice()

def B_Button():
    if AppmenuActive == True:
        Right()
    elif ActiveApp == "RadioChat":
        Right()

input.on_button_pressed(Button.B, B_Button)
input.on_button_pressed(Button.A, A_Button)
input.on_button_pressed(Button.AB, AB_Button)
input.on_gesture(Gesture.SHAKE, GestureShake)

Boot()
Appmenu()
