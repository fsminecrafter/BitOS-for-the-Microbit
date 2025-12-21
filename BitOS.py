#BitOS made by fsminecrafter 2025-nov-20

AppmenuActive = True
digits = "0123456789"
Apps = ["Uninitialized"]
AppsLogos = ["09090:00000:00000:09990:90009"]
messages = ["Hello!", "(:", "):", "How are you doing?", "Isnt BitOS great!?", "Lets add some more messages..."]
appindex = 0
debug = False
ActiveApp = "None"
PlayerY = 3
rockX = 5
rockY = 2

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
    music.ring_tone(Note.F)
    basic.pause(250)
    music.stop_all_sounds()
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
    global PlayerY
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
    elif app == "Pattern":
        basic.clear_screen()
        while AppmenuActive == False:
            Showimage("90909:05050:90009:05050:90909")
            basic.pause(250)
            Showimage("09090:50505:05250:50505:09090")
            basic.pause(250)
    elif app == "Game":
        basic.clear_screen()
        Showimage("00000:00000:00000:90000:99999")

def ExitApplication():
    basic.clear_screen()
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

def Lose():
    basic.clear_screen()
    music._play_default_background(music.built_in_playable_melody(Melodies.FUNERAL), music.PlaybackMode.IN_BACKGROUND)
    basic.show_string("You Lost!")
    ActiveApp = "None"
    ExitApplication()
    basic.clear_screen()

def GameFrame():
    global PlayerY
    global rockX
    global rockY
    rockX = 5
    rockY = randint(2, 3)
    random = randint(0, 10)
    if random == 7:
        for i in range(7):
            if not i == 1:
                led.unplot(rockX + 1, rockY)
            led.plot(rockX, rockY)
            if i == 6:
                led.unplot(0, rockY)
                break
            if rockX == 0 and rockY == PlayerY:
                rockX = 5
                Lose()
                break
            rockX -= 1
            basic.pause(100)

def Jump():
    global PlayerY
    global rockX
    global rockY
    PlayerY = 2
    led.unplot(0, PlayerY + 1)
    led.plot(0, PlayerY)
    if rockX == 0 and rockY == PlayerY:
        Lose()
    music.play(music.tone_playable(Note.E, music.beat(BeatFraction.QUARTER)), music.PlaybackMode.IN_BACKGROUND)
    basic.pause(250)
    PlayerY = 3
    led.unplot(0, PlayerY - 1)
    led.plot(0, PlayerY)

def InitApplications():
    music.set_volume(255)
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
    RegisterApplication("Pattern", "00000:09090:00900:09090:00000")
    RegisterApplication("Game", "00000:00000:00900:00000:99999")
    while True:
        if AppmenuActive:
            Showimage(AppsLogos[appindex])
        if ActiveApp == "Game":
            GameFrame()
        basic.pause(100)

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
    elif ActiveApp == "Game":
        Jump()

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
