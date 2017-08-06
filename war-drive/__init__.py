import ugfx, network, badge, ubinascii, appglue # dialogs

encription = { 0: "Open", 1: "WEP", 2: "WPA", 3: "WPA2", 4: "WPA*", 5: "802.11x" }
scroll = 0
max_scroll = 0
scanResults = list()

def clearGhosting():
    ugfx.clear(ugfx.WHITE)
    ugfx.flush()
    badge.eink_busy_wait()
    ugfx.clear(ugfx.BLACK)
    ugfx.flush()
    badge.eink_busy_wait()

ugfx.init()
ugfx.input_init()
clearGhosting()

def home(pressed):
  if pressed:
    appglue.home()

def run(pressed):
  if pressed:
    scan()


def up_pressed(pressed):
    print("Up")
    global scroll, max_scroll
    if pressed:
        if scroll > 0:
            scroll -= 4
            re_draw()


def down_pressed(pressed):
    print("Down")
    global scroll, max_scroll
    if pressed:
        if scroll < (max_scroll - 4):
            scroll += 4
            re_draw()

def re_draw():
    global scroll, max_scroll
    print("redraw:"+str(scroll))
    ugfx.clear(ugfx.WHITE)
    y=0
    ugfx.string(0, y, "SSID", "pixelade13", ugfx.BLACK)
    ugfx.string(110, y, "Enc", "pixelade13", ugfx.BLACK)
    ugfx.string(150, y, "Ch", "pixelade13", ugfx.BLACK)
    ugfx.string(175, y, "dB", "pixelade13", ugfx.BLACK)
    ugfx.string(210, y, "BSSID", "pixelade13", ugfx.BLACK)
    ugfx.string(270, y, '{:d}/{:d}'.format(scroll, max_scroll), "pixelade13", ugfx.BLACK)
    ugfx.line(0, 12, 296, 12, ugfx.BLACK)
    y+=15
    for net in scanResults[scroll:]:
        # (ssid, bssid, channel, RSSI, authmode, hidden)
        # (b'SHA2017-legacy', b"\xa8\xbd'z\xd1\xc0", 1, -55, 5, False)
        print(net)
        bssid = ubinascii.hexlify(net[1]).upper()
        ssid = net[0]
        if net[5] == True:
            ssid = "<hidden>"
        ugfx.string(0, y, '{:40}'.format(ssid), "pixelade13", ugfx.BLACK)
        ugfx.string(110, y, '{}'.format(encription.get(net[4],"?")), "pixelade13", ugfx.BLACK)
        ugfx.string(150, y, '{:2d}'.format(net[2]), "pixelade13", ugfx.BLACK)
        ugfx.string(175, y, '{:3d}'.format(net[3]), "pixelade13", ugfx.BLACK)
        ugfx.string(210, y, '{:2}:{:2}:{:2}:{:2}:{:2}:{:2}'.format(bssid[0:2],bssid[2:4],bssid[4:6],bssid[6:8],bssid[8:10],bssid[10:12]), "pixelade13", ugfx.BLACK)
        y += 14
    ugfx.flush()

def scan():
    global scroll, max_scroll, scanResults
    print("Scanning")
    ugfx.clear(ugfx.WHITE)
    ugfx.string(100,50,'Scanning...','Roboto_Regular18',ugfx.BLACK)
    ugfx.flush()

    sta_if = network.WLAN(network.STA_IF); sta_if.active(True)
    scanResults = sta_if.scan()

    sorted(scanResults, key=lambda net: net[3], reverse=True)
    max_scroll = len(scanResults)
    scroll = 0

    re_draw()


scan()


ugfx.input_attach(ugfx.BTN_A, run)
ugfx.input_attach(ugfx.BTN_B, home)
ugfx.input_attach(ugfx.JOY_UP, up_pressed)
ugfx.input_attach(ugfx.JOY_DOWN, down_pressed)
