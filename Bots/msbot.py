import sys, os, time
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent) )

from U2.base import sb # subprocess
from U2.bot import Bot
from U2.enums import Wtype, ButtonInstancePos, ButtonInstanceBounds
from U2.debug import NotifLog, notif_, infoLog, debugLog, boxArea
from U2.actions import adbClick, adbClickNoUi
from U2.notif import Tracker


class MSBot( Bot ):
    

    def __init__( self, **kwargs ):
        # Time trackers
        self.elapsed = Tracker()
        self.interval = Tracker()

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
        # Wait for check ui to exists before switching task
        ui = self.waitElement( self.check_selector, timeout=10 )
        prev_task = self.tasks[ self.prev_task_number ]

        if ui == None:
            NotifLog.recheck += 1
            notif_(1, f"Check failed:{prev_task.check_selector}")

            log = f"[{self}] check timedout [{prev_task.match_selector}] @task[{prev_task.number}]"
            debugLog( log )
            boxArea( name = log, overlap = False )

            self.current_task_number = self.prev_task_number
            return

        elif ui == "FAILED":
            return
        self.elapsed.trackS()

        # Increment points at specific task
        if self.prev_task_number == self.task_number_points_add:
            self.incrementPoints( self.points_increment )

        notif_( 1, f"Checked[ {prev_task.check_selector} ] [ {self.elapsed} ]")
        infoLog( f"Checked[{self.check_selector}] @task[{prev_task.number}]" )

        self.current_task_number = self.next_task_number
    
        # Avoid self checks with early return for multi bot
        if self.multi_bot and self.current_task_number == self.end_task_number:
            self.running = False
            return

        # Restart target if cycle interval take longer than usual
        if self.intervalExceed():
            print(f"Interval exceeds : {self.interval.avgTime}")
            debugLog( f"Restart action <reason : interval exceeds[{self.interval.avgTime}]>")
            self.restartTarget( buttonBounds = self.button_bounds )


    def restartTarget( self, buttonBounds : ButtonInstanceBounds = None, buttonPos : ButtonInstancePos = None, include_click = True ):
        if not include_click: return

        # Restart target app when interval time exceeds average time cycle
        sb.run( f"adb shell am force-stop {self.target_package}; sleep 0.3; adb shell am start -n {self.launch_activity}", shell=True, stdout=sb.DEVNULL )

        self.device.wait_activity( self.launch_activity.split('/')[1] )
        time.sleep(0.5)

        self.interval.reset_avg()
        print(f"Reset avg : {self.interval.avgTime}")
        NotifLog.restarts += 1

        if buttonPos:
            adbClickNoUi( buttonPos )
            return

        # Todo // via instance number // Forcec search
        while True:
            # Search ui
            buttonUi = None
            while not buttonUi:
                buttonUi = self.waitElement({"className" : Wtype.button, "instance" : buttonBounds['number']}, timeout=0.2)

            # Get info
            info = None
            while not info:
                info = self.getInfo( buttonUi )
            
            info_bounds = info['bounds']
            ins_bounds = buttonBounds['bounds']

            # Compare bounds
            if info_bounds == ins_bounds:
                adbClick( info_bounds )
                break
            else:
                log = f"Restart Action : different bounds | info:{info_bounds} != iNBounds:{ins_bounds}"
                debug( log )


if __name__=='__main__':
    pass
