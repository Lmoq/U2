import time, sys 
import uiautomator2 as u2
from pathlib import Path

# Resolve paths
root = Path(__file__).resolve().parent

bots_dir = str(root.parent)
U2_dir = str( root.parent / 'U2' )

sys.path.extend( [ str( root ), U2_Dir, bots_dir  ] )

from U2.enums import ButtonInstancePos, ButtonInstanceBounds
from U2.actions import vibrate, switch_keyboard

from U2.debug import NotifLog, notif_
from U2.process import start_adb_shell_pipes
from U2.notif import notif


# U2 bots
from U2.base import U2_Device
from Bots.msbot import MSBot

from bot_one.main import Bot1
from bot_two.main import Bot2

from bot_handler import Bot_Handler
from config import extractJsonData, saveJson, loadJson
from utils import updateNotif, switchFocus


running = True

BotList = []
BotDis = []
BotJson = {}

jsonData = "./data/data.json"

def altRun():
    global running, BotList, BotJson, BotDis, jsonData
    
    # Handlers
    B1 = Bot_Handler( Bot1 )
    
    B1.task1 = 55
    B1.task2 = 55
    B1.name = "💙Bot1💙"
    B1.key_name = "Bot1"
    # --------------------

    B2 = Bot_Handler( Bot2 )
    
    B2.task1 = 35
    B2.task2 = 35
    B2.name = "✨Bot2✨"
    B2.key_name = "Bot2"
    # --------------------
    tmp = [ B1, B2 ]

    # Set designated button instances based on the order U2 Bots on tmp list
    button_instances = [ getattr( ButtonInstancePos, attr ) \
                         for attr in dir( ButtonInstancePos ) \
                         if not attr.startswith('__') ]
    
    zip_ = zip( tmp, button_instances )
    [ setattr( bot.bot, 'button_instance', tup ) for bot,tup in zip_ ]

    # Load data base
    loadJson( tmp, BotJson, path=jsonData )

    for bot in tmp:
        # Merge atrributes set from db to bots attributes
        jsonInfo = BotJson[ bot.key_name ]
        bot.bot.__dict__ |= jsonInfo

    # Filter restricted bots
    for bot in tmp:
        # Allow bots to lift restrictions
        bot.bot.restricted = bot.bot.timeRestricted() or bot.bot.pointsReachedLimit()
        
        if bot.bot.restricted:
            # Append to discarded list
            BotDis.append( bot )
            continue

        # Share single device
        bot.bot.tag = bot.name
        bot.bot.name = bot.key_name
        
        # Set universal properties for multi bot
        bot.bot.multi_bot = True

        # Add to botlist if not time restricted
        BotList.append( bot )

    if BotList: Bot = BotList[0]
    del tmp

    # Init bots' device session
    MSBot.init_device_session( u2.connect(), 'com.packange.name' )


    # Main loop
    while BotList and not MSBot.sig_term:
        try:
            # Display latest notif update
            updateNotif( BotList )

            # Every bots' self.check self.running will be 
            # disabled to allow others to run 
            Bot.bot.running = True
            Bot.bot.mainloop()
 
            if MSBot.sig_term:
                print("Sigterm")
                continue

            # Get current task and estimated time wait
            interval = Bot.bot.get_next_task().next_wait_time

            allowance = 5
            Bot.next = time.time() + ( interval - allowance )

            # Choose the quickest wait time if all Bot have done task and time wait
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
                    # Restart app w/o click depending on next bot for switchFocus to not do pressBack anymore
                    Bot.bot.restartTarget(
                        buttonBounds = Bot.bot.button_bounds,
                        include_click = False if Bot != next_bot else True
                    )
                    restarted = True
                    Bot.bot.interval.reset_avg()

                # Prevents calling switch instance if Bot reference did not change
                if Bot != next_bot:
                    Bot = next_bot 
                     
                    # Switch bot ui focus 
                    # Will not do pressBack if prev_bot restarted
                    switchFocus( 
                        buttonBounds = Bot.bot.button_bounds,
                        pressBack = True if not restarted else False,
                        bot = Bot.bot
                    )
                continue

            # Switch until all bots have done some task
            for b in BotList:
                if not b.next:
                    Bot = b
                    # Switch bot ui focus
                    switchFocus( buttonBounds = Bot.bot.button_bounds, bot = Bot.bot )
                    break

        except KeyboardInterrupt:
            running = False
            break

    # Save bots attributes changes to data base
    BotList.extend( BotDis )
    saveJson( BotList, BotJson, path=jsonData )


def main():
    # Start adb shell pipe
    start_adb_shell_pipes()
    notif( content = "Switch Keyboard", b1 = "Switch", b1_action = "~/share/bash/disable_keyboard.sh")

    NotifLog.capacity = 7

    switch_keyboard( 'off' )
    altRun()
    
    notif_( 1, "No bots running" )
    switch_keyboard( 'on' )


if __name__=='__main__':
    main()
