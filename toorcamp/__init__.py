import ugfx, badge, appglue

ugfx.init()
ugfx.input_init()
ugfx.clear(ugfx.BLACK)
ugfx.flush()
ugfx.clear(ugfx.WHITE)
ugfx.flush()

def clearGhosting():
    ugfx.clear(ugfx.WHITE)
    ugfx.flush()
    badge.eink_busy_wait()
    ugfx.clear(ugfx.BLACK)
    ugfx.flush()
    badge.eink_busy_wait()

switch = False

def go_home(pushed):
    if(pushed):
        appglue.home()

def switchme(pushed):
    global switch
    if(pushed):
        if switch:
            print("ToorCamp")
            switch = False
            #clearGhosting()
            ugfx.clear(ugfx.WHITE)
            badge.eink_png(0,0,'/lib/toorcamp/toorcamp.png')
            badge.eink_busy_wait()
        else:
            print("ToorCon")
            switch = True
            #clearGhosting()
            ugfx.clear(ugfx.WHITE)
            badge.eink_png(0,0,'/lib/toorcamp/toorcon.png')
            badge.eink_busy_wait()

clearGhosting()
ugfx.input_attach(ugfx.BTN_B, go_home)
ugfx.input_attach(ugfx.BTN_A, switchme)
badge.eink_png(0,0,'/lib/toorcamp/toorcamp.png')
ugfx.flush()
