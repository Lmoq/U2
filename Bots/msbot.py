import sys, os, time
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent) )

from U2.base import sb # subprocess
from U2.bot import Bot

from U2.enums import Wtype, ButtonInstancePos, ButtonInstanceBounds
from U2.debug import NotifLog, notif_, infoLog, debugLog, boxArea
from U2.actions import adbClick, adbClickNoUi


class MSBot( Bot ):
    

    def __init__( self, **kwargs ):
        # Track points
        self.points = 0
        self.task_number_points_add = 0

        self.points_increment = 0
        self.points_limit = 99

        # Restart
        self.restart_time = 0
        
        self.button_pos : ButtonInstancePos = None
        self.button_bounds : ButtonInstanceBounds = None

        self.end_task_number = 0
        self.multi_bot = False

        super().__init__( **kwargs )


    def intervalExceed( self ) -> bool:
        # Check if average interval takes longer time than usual
        if self.interval.avgTime.seconds > self.restart_time:
            return True
        return False


    def incrementPoints( self, increment ):
        # Update points
        self.points = round( self.points + increment, 2 )


    def pointsReachedLimit( self ):
        if self.points >= self.points_limit:
            return True
        return False


    def doCheck( self ):
        super().doCheck()

        # Increment points at specific task
        if self.prev_task_number == self.task_number_points_add:
            self.incrementPoints( self.points_increment )

        if self.prev_task_number == self.end_task_number:
            # Avoid self checks by returning early for multi bot
            if self.multi_bot:
                self.running = False
                return

            if self.intervalExceed():
                # Restart target if cycle interval take longer than usual
                debugLog( f"Restart action <reason : interval exceeds[{self.interval.avgTime}]> @endTask[{self.current_task.number}]")
                print(f"[MSBot] Reset avg : {self.interval.avgTime}")

                self.restartTarget( buttonBounds = self.button_bounds )
                self.interval.reset_avg()


    def restartTarget( self, buttonBounds : ButtonInstanceBounds = None, buttonPos : ButtonInstancePos = None, include_click = True ):
        # Restart target app when interval time exceeds average time cycle
        sb.run( f"adb shell am force-stop {self.target_package}; sleep 0.3; adb shell am start -n {self.launch_activity}", shell=True, stdout=sb.DEVNULL )

        self.device.wait_activity( self.launch_activity.split('/')[1] )
        #time.sleep(0.5)

        NotifLog.restarts += 1

        if not include_click: 
            return

        if buttonPos:
            adbClickNoUi( buttonPos )
            return

        # Perform search for ui element using instance number
        # tailored by ui bounds checking to verify if it's the correct element
        while True:
            # Search ui
            buttonUi = None
            while not buttonUi:
                buttonUi = self.waitElement({"className" : Wtype.button, "instance" : buttonBounds['number']}, timeout=0.2)

            # Get info
            info = self.getInfo( buttonUi )
            info_bounds = info['bounds']
            ins_bounds = buttonBounds['bounds']

            # Compare bounds
            if info_bounds == ins_bounds:
                adbClick( info_bounds )
                break
            else:
                log = f"Restart search : different bounds | info:{info_bounds} != iNBounds:{ins_bounds}"
                debugLog( log )


if __name__=='__main__':
    pass
