import time, sys, os, json
import uiautomator2 as u2
from pathlib import Path

# Resolve paths
root = Path(__file__).resolve().parent
sys.path.extend( [str( root.parent / 'U2' / 'Bots' ), str( root ), str( root.parent / 'U2' ), str(root.parent)] )

from threading import Thread
from pprint import pp

from U2.enums import TaskType, Wtype, ButtonInstancePos
from U2.notif import Stime
from U2.actions import adbClick, adbClickNoUi, vibrate, switch_keyboard

from U2.debug import NotifLog, notif_, notiflog
from U2.process import start_adb_shell_pipes



# U2 bots
#from cecb.main import CECB
#from fbmb.main import FBMB
#from mmcb.main import MMCB
#from dmcb.main import DMCB
#from aems.main import AEMS
from ecnl.main import ECNL
from msbot import MSBot


running = True
BotList = []
BotDis = []
BotJson = {}


class Bot_Handler:

    def __init__( self, Bot : MSBot ):
        self.bot = Bot
        
        self.name = ""
        self.key_name = ""
        self.instance_num = 0

        # Time interval
        self.task1 = 0
        self.task2 = 0

        # Next activity time stamp
        self.next = 0

    def __repr__( self ):
        return self.name


def extractJsonData( bot_list, out_json ):
    # Save Bot attributes to outjson
    base_json = {
        "current_task_number" : 0.0,

        "points" : 0.0,
        "points_limit" : 0,
        
        "points_increment" : (0,1),

        "start_time_restriction" : "",
        "end_time_restriction" : "",
        "restricted" : False,
    }
    for b in bot_list:
        key = b.key_name
        
        # Fill dict value of unassigned key( bot name )
        if not key in out_json:
            out_json[ key ] = {}
            
        contents = out_json[ key ]
        contents |= base_json

        # Replace Stime object as string to save as json key
        if isinstance ( b.bot.start_time_restriction, Stime ):
            b.bot.start_time_restriction = b.bot.start_time_restriction.str

        if isinstance ( b.bot.end_time_restriction, Stime ):
            b.bot.end_time_restriction = b.bot.end_time_restriction.str

        # Extract the updated map of BotList to outjson
        # that contains keys based from base_json
        for k in contents.keys():
            contents[ k ] = b.bot.__dict__[ k ]


def saveJson( bot_list ):
    # Save updated data base
    global BotJson

    # Retrieve and set json data from botlist to BotJson
    extractJsonData( bot_list, BotJson ) 
    with open( 'data.json', 'w' ) as f:
        json.dump( BotJson, f, indent=4 )

    pp( BotJson )


def loadJson( BotList ):
    # Load data base to BotJson
    global BotJson

    if not os.path.exists( 'data.json' ):
        # Fill data base contents
        saveJson( BotList )
        print( 'Created data.json' )

    else:
        with open( 'data.json', 'r' ) as f:
            BotJson = json.load( f )

            compare_json = {}
            extractJsonData( BotList, compare_json )

            # Get difference
            diff = set( BotJson.keys() ) ^ set( compare_json.keys() )

            if diff:
                # Update BotJson with new keys from compare_json
                compare_json |= BotJson
                # Then update those keys with right values from botjson
                BotJson |= compare_json

        print( 'Existing data loaded' )


def updatenotif( BotList, ext="" ):
    # Log future time string
    strings = []
    for bot in BotList:

        timestr = time.strftime( "%H:%M:%S", time.localtime( bot.next ) )
        strings.append( f"{bot.name} • {timestr} • {bot.bot.interval.avgTime} • {bot.bot.points:.2f} • {bot.bot.current_task_number}" )
    
    # Replace notiflog list 
    notiflog.list = strings
    NotifLog.title = f'U2 | RC : {NotifLog.recheck} | GI : {NotifLog.gInfo} | RS : {NotifLog.restarts}'

    cm = f'''echo 'cmd notification post -S inbox {notiflog} -t "{NotifLog.title}" notif logs &> /dev/null' > ~/pipes/adbpipe'''
    os.system(cm)


def switchInstance( num = 0, noUi:tuple = None, pressBack = True ):
    global device

    if pressBack: os.system( "echo 'input keyevent 4' > ~/pipes/adbpipe" )
    time.sleep(0.7)

    # Direct click with xy tuple
    if noUi:
        adbClickNoUi( noUi )
        return

    # Click with ui selector search
    ui = None
    while ui is None:
        try:
            # Messenger chat tabs' className is Wtype.button
            ui = device( className = Wtype.button, instance = num )
        
        except Exception as e:
            print(e)
            continue

    info = None
    while not info:
        try:
            info = ui.info

        except Exception:
            continue

    bounds = info['bounds']
    adbClick( bounds )


def altRun():
    global running, device, BotList, BotJson, BotDis
    
    # Handlers
    ## Bot 1 --------------
    #B1 = Bot_Handler( CECB )

    #B1.task1 = 368
    #B1.task2 = 369
    #B1.name = "💙CECB💙"
    #B1.key_name = "CECB"
    ## --------------------

    ## Bot 2 --------------
    #B2 = Bot_Handler( FBMB )
    #
    #B2.task1 = 258
    #B2.task2 = 259
    #B2.name = "🌸FBMB🌸"
    #B2.key_name = "FBMB"
    ## --------------------

    ## Bot 3 --------------
    #B3 = Bot_Handler( DMCB )
    #
    #B3.task1 = 252
    #B3.task2 = 302
    #B3.name = "🌟DMCB🌟"
    #B3.key_name = "DMCB"
    ## --------------------
    #
    ## Bot 4 --------------
    #B4 = Bot_Handler( MMCB )
    #
    #B4.task1 = 139
    #B4.task2 = 139
    #B4.name = "💫MMCB💫"
    #B4.key_name = "MMCB"
    ## --------------------

    #B5 = Bot_Handler( AEMS )
    #
    #B5.task1 = 55
    #B5.task2 = 55
    #B5.name = "💙AEMS💙"
    #B5.key_name = "AEMS"
    ## --------------------

    B6 = Bot_Handler( ECNL )
    
    B6.task1 = 35
    B6.task2 = 35
    B6.name = "✨ECNL✨"
    B6.key_name = "ECNL"
    # --------------------
    tmp = [ B6 ]

    # Set designated button instances based on the order U2 Bots on tmp list
    button_instances = [ getattr( ButtonInstancePos, attr ) \
                         for attr in dir( ButtonInstancePos ) \
                         if not attr.startswith('__') ]
    
    zip_ = zip( tmp, button_instances )
    [ setattr( bot.bot, 'button_instance', tup ) for bot,tup in zip_ ]

    # Load data base
    loadJson( tmp )

    for bot in tmp:
        # Set bot atrributes based from db
        jsonInfo = BotJson[ bot.key_name ]
        bot.bot.__dict__ |= jsonInfo

    # Setup bots to run
    for bot in tmp:
        # Lift restrictions
        bot.bot.restricted = bot.bot.timeRestricted() or bot.bot.pointsReachedLimit()
        
        # Include only non restricted bots to run
        if bot.bot.restricted:
            BotDis.append( bot )
            continue

        # Share single device
        bot.bot.tag = bot.name
        bot.bot.name = bot.key_name
        
        # Set universal properties for multi bot
        bot.bot.multi_bot = True
        bot.bot.task_points_add = TaskType.t1

        # Add to botlist if not time restricted
        BotList.append( bot )

    if BotList: Bot = BotList[0]
    del tmp

    # Init bots' device session
    MSBot.init_device_session( u2.connect(), 'com.facebook.orca' )

    # Main loop
    while BotList and not MSBot.sig_term:
        try:
            # Display latest notif update
            updatenotif( BotList )

            # Every bots' self.check self.running will be 
            # disabled to allow others to run 
            Bot.bot.running = True
            Bot.bot.mainloop()
 
            if MSBot.sig_term:
                print("Sigterm")
                continue

            # Get current task and estimated time wait
            task = Bot.bot.current_task_number
            interval = Bot.task1 if Bot.bot.current_task_number == 1 else Bot.task2

            allowance = 5
            Bot.next = time.time() + ( interval - allowance )

            # Choose the smallest time wait if all Bot had task and time wait done
            if all( b.next for b in BotList ):
                
                BotList = sorted( BotList, key=lambda b : b.next )
                next_bot = BotList[0]

                # Check next bot time restriction
                if next_bot.bot.restricted:
                    
                    # Move bot from discarded list
                    BotDis.append( BotList.pop( 0 ) )

                    if not BotList: 
                        vibrate( 2, 1 )
                        break 

                    next_bot = BotList[0]
 
                # Check interval limit
                restarted = False
                
                if not Bot.bot.restricted and Bot.bot.intervalExceed():
                    # Restart app w/o click depending on next bot
                    Bot.bot.restartTarget(
                        buttonBounds = Bot.bot.button_bounds,
                        click = False if Bot != next_bot else True
                    )
                    restarted = True
                    Bot.bot.interval.reset_avg()

                # Prevents calling switch instance if Bot reference did not change
                if Bot != next_bot:
                    Bot = next_bot 
                     
                    # Switch bot ui focus 
                    switchInstance( 
                        noUi = Bot.bot.button_pos,
                        pressBack = True if not restarted else False
                    )
                continue

            # Switch to other bot that has no next time stamp set
            for b in BotList:
                if not b.next:
                    Bot = b
                    # Switch bot ui focus
                    switchInstance( noUi = Bot.bot.button_instance )
                    break

        except KeyboardInterrupt:
            running = False
            break

def main():
    global BotList, BotDis
    
    # Start adb shell pipe
    start_adb_shell_pipes()

    NotifLog.capacity = 7

    switch_keyboard( 'off' )
    altRun()
    
    notif_( 1, "No bots running" )
    switch_keyboard( 'on' )

    # Save data base
    BotList.extend( BotDis )
    saveJson( BotList )

if __name__=='__main__':
    main()
