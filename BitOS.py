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

# Compute Inc Game vars
Money = 1000
BitsCoins = 0.00
OwnedComputerModules = ["Uninitialized"]
ComputeModuleCost = 600
MemoryModuleCost = 300
StorageModuleCost = 100
BitsValue = 10
MarketGoingUp = True
MarketGoingUpBy = 0.2
TimeSinceLastChange = 0
InShop = False
SelectedItem = "cpu"

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
    elif app == "ComputerInc":
        basic.clear_screen()
        Showimage("99999:90009:90009:90009:99999")

def Csell():
    global BitsCoins
    global BitsValue
    global Money

    if BitsCoins > 0.0001:
        Money += BitsCoins * BitsValue
        BitsCoins = 0.0000

def RatioScore(a, b, c):
    if a <= 0 or b <= 0 or c <= 0:
        return 0

    small = min(a, b)
    smallest = min(small, c)
    na = a / smallest
    nb = b / smallest
    nc = c / smallest

    # Target ratio
    ta = 3
    tb = 2
    tc = 1

    error = abs(na - ta) + abs(nb - tb) + abs(nc - tc)
    ratio_points = max(0, 100 - error * 20)
    size_points = (a + b + c) / 3
    return ratio_points + size_points

def CGameFrame():
    global BitsCoins
    global OwnedComputerModules
    global BitsValue
    global MarketGoingUp
    global MarketGoingUpBy
    global TimeSinceLastChange

    Power = 0
    Cpus = 0
    Mems = 0
    Hrds = 0
    for i in OwnedComputerModules:
        if i == "ComputeModule":
            Cpus += 1
        elif i == "MemoryModule":
            Mems += 1
        else:
            Hrds += 1
    Power = RatioScore(Cpus, Mems, Hrds)
    BitsCoins += Power / 13570
    # --- Market movement ---
    drift = randint(0, 2)  # small natural movement

    if MarketGoingUp:
        MarketGoingUpBy += drift
    else:
        MarketGoingUpBy -= drift

    # Clamp market speed (VERY IMPORTANT)
    if MarketGoingUpBy > 10:
        MarketGoingUpBy = 10
    elif MarketGoingUpBy < -10:
        MarketGoingUpBy = -10

    TimeSinceLastChange += 1

    # --- Reversal chance increases over time ---
    chance = randint(0, 100)

    if TimeSinceLastChange > 300:
        if chance < 30:
            MarketGoingUp = not MarketGoingUp
            TimeSinceLastChange = 0

    elif TimeSinceLastChange > 200:
        if chance < 20:
            MarketGoingUp = not MarketGoingUp
            TimeSinceLastChange = 0

    elif TimeSinceLastChange > 100:
        if chance < 10:
            MarketGoingUp = not MarketGoingUp
            TimeSinceLastChange = 0

    # --- Apply market to value ---
    BitsValue += MarketGoingUpBy

    # Prevent negative market value
    if BitsValue < 0:
        BitsValue = 0


# This function updates the Home UI.
def CHomeUpdate():
    global InShop
    global OwnedComputerModules
    InShop = False
    pointerX = 1
    pointerY = 1
    Showimage("99999:90009:90009:90009:99999")
    for i in OwnedComputerModules:
        led.plot(pointerX, pointerY)
        if pointerX == 3:
            pointerX = 1
            pointerY += 1
        else:
            pointerX += 1
    

# This function updates the Shop UI.
def CShopUpdate():
    global SelectedItem
    global InShop
    InShop = True
    basic.clear_screen()
    if SelectedItem == "cpu":
        Showimage("99999:99999:00000:00000:00000")
    elif SelectedItem == "mem":
        Showimage("00000:00000:99999:99999:00000")
    else:
        Showimage("00000:00000:00000:00000:99999")

def cut(value, decimals):
    sign = ''
    if value < 0:
        sign = '-'
        value = -value

    mult = 1
    for i in range(decimals):
        mult = mult * 10

    # Cut the number
    cut_value = int(value * mult) / mult

    text = str(cut_value)

    if '.' not in text:
        return sign + text + '.' + (0 * decimals)

    whole = text.split('.')[0]
    dec = text.split('.')[1]

    while len(dec) < decimals:
        dec = dec + '0'

    return sign + whole + '.' + dec


def PurchaseItem(cost, item):
    global OwnedComputerModules
    global Money
    if Money >= cost:
        Money -= cost
        OwnedComputerModules.append(item)
    else:
        basic.clear_screen()
        basic.show_icon(IconNames.NO)
        basic.pause(1000)
        CShopUpdate()

def LogoTouch():
    global ActiveApp
    global ComputeModuleCost
    global MemoryModuleCost
    global StorageModuleCost
    global InShop
    if ActiveApp == "ComputerInc":
        if InShop:
            if SelectedItem == "cpu":
                PurchaseItem(ComputeModuleCost, "ComputeModule")
            elif SelectedItem == "mem":
                PurchaseItem(MemoryModuleCost, "MemoryModule")
            else:
                PurchaseItem(StorageModuleCost, "StorageModule")
        else:
            basic.clear_screen()
            basic.show_string('$' + str(Money) + "{B}" + cut(BitsCoins, 3))
            CHomeUpdate()

def GestureShake():
    global SelectedItem
    global ComputeModuleCost
    global MemoryModuleCost
    global StorageModuleCost
    global InShop
    if ActiveApp == "RadioChat":
        radio.send_string(messages[appindex])
    elif ActiveApp == "ComputerInc":
        if InShop:
            if SelectedItem == "cpu":
                basic.show_string(str(ComputeModuleCost))
                CShopUpdate()
            elif SelectedItem == "mem":
                basic.show_string(str(MemoryModuleCost))
                CShopUpdate()
            else:
                basic.show_string(str(StorageModuleCost))
                CShopUpdate()
        else:
            basic.show_string("Value: " + str(BitsValue))

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
    global Apps
    global AppsLogos
    global OwnedComputerModules
    music.set_volume(255)
    while len(Apps) > 0:
        Apps.pop()
    while len(AppsLogos) > 0:
        AppsLogos.pop()
    while len(OwnedComputerModules) > 0:
        OwnedComputerModules.pop()


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
    RegisterApplication("ComputerInc", "99999:90909:90909:90909:99999")
    while True:
        if AppmenuActive:
            Showimage(AppsLogos[appindex])
        if ActiveApp == "Game":
            GameFrame()
        if ActiveApp == "ComputerInc":
            CGameFrame()
        basic.pause(100)

def AB_Button():
    global AppmenuActive
    global ActiveApp
    global InShop
    if AppmenuActive == True:
        AppEntryPoint()
    elif ActiveApp == "ComputerInc":
        if InShop:
            CHomeUpdate()
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
    basic.show_number(Dice)

def A_Button():
    global SelectedItem
    global InShop
    global AppmenuActive
    global ActiveApp

    if AppmenuActive == True:
        Left()
    elif ActiveApp == "RadioChat":
        Left()
    elif ActiveApp == "Dice":
        RollDice()
    elif ActiveApp == "Game":
        Jump()
    elif ActiveApp == "ComputerInc":
        if InShop:
            if SelectedItem == "cpu":
                SelectedItem = "hrd"
                CShopUpdate()
            elif SelectedItem == "hrd":
                SelectedItem = "mem"
                CShopUpdate()
            else:
                SelectedItem = "cpu"
                CShopUpdate()
        else:
            Csell()

def B_Button():
    global SelectedItem
    global InShop
    global AppmenuActive
    global ActiveApp

    if AppmenuActive == True:
        Right()
    elif ActiveApp == "RadioChat":
        Right()
    elif ActiveApp == "ComputerInc":
        if InShop:
            if SelectedItem == "cpu":
                SelectedItem = "mem"
                CShopUpdate()
            elif SelectedItem == "mem":
                SelectedItem = "hrd"
                CShopUpdate()
            else:
                SelectedItem = "cpu"
                CShopUpdate()
        else:
            CShopUpdate()

input.on_button_pressed(Button.B, B_Button)
input.on_button_pressed(Button.A, A_Button)
input.on_button_pressed(Button.AB, AB_Button)
input.on_gesture(Gesture.SHAKE, GestureShake)
input.on_logo_event(TouchButtonEvent.PRESSED, LogoTouch)

Boot()
Appmenu()
