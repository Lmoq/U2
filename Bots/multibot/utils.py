import sys, time, os
from pathlib import Path

root = Path(__file__).resolve().parent
sys.path.extend( [ str( root.parent / 'U2' ) ] )

from U2.base import U2_Device
from U2.enums import Wtype, ButtonInstancePos, ButtonInstanceBounds
from U2.debug import NotifLog, notiflog, debugLog
from U2.actions import adbClick, adbClickNoUi


def updateNotif( bot_list, ext="" ):
    # Log future time string
    strings = []
    for bot in bot_list:

        timestr = time.strftime( "%H:%M:%S", time.localtime( bot.next ) )
        strings.append( f"{bot.name} • {timestr} • {bot.bot.interval.avgTime} • {bot.bot.points:.2f} • {bot.bot.current_task_number}" )
    
    # Replace notiflog list 
    notiflog.list = strings
    NotifLog.title = f'U2 | RC : {NotifLog.recheck} | GI : {NotifLog.gInfo} | RS : {NotifLog.restarts}'

    cm = f'''echo 'cmd notification post -S inbox {notiflog} -t "{NotifLog.title}" notif logs &> /dev/null' > ~/pipes/adbpipe'''
    os.system(cm)


def switchFocus( num = 0, buttonPos:ButtonInstancePos = None, 
                buttonBounds:ButtonInstanceBounds = None, 
                pressBack = True, bot: U2_Device = None  
    ):
    assert isinstance( bot, U2_Device )

    if pressBack: os.system( "echo 'input keyevent 4' > ~/pipes/adbpipe" )
    time.sleep(0.7)

    # Direct click with xy tuple
    if buttonPos:
        adbClickNoUi( buttonPos )
        return

    # Perform a search for ui element using instance number
    # refined by ui bounds checking to ensure it's the correct element
    while True:
        # Search ui
        buttonUi = None
        while not buttonUi:
            buttonUi = bot.waitElement({"className" : Wtype.button, "instance" : buttonBounds['number']}, timeout=0.2)

        # Get info
        info = bot.getInfo( buttonUi )
        info_bounds = info['bounds']
        ins_bounds = buttonBounds['bounds']

        # Verify bounds
        if info_bounds == ins_bounds:
            adbClick( info_bounds )
            break
        else:
            log = f"Restart search : different bounds | info:{info_bounds} != iNBounds:{ins_bounds}"
            debugLog( log )

