import sys, time
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent ) )
from U2.enums import ActionType, TaskType, Wtype, Direction

from U2.actions import vibrate, adbClick, adbType, adbSwipeUi, adbClickNoUi, switch_keyboard, adbKeyCombo
from U2.debug import notif_, NotifLog, debugLog, infoLog, boxArea
from U2._bot import _Bot
from U2.notif import Stime, Tracker


class Bot( _Bot ):


    def __init__( self, **kwargs ):
        # App will not run on given time frame
        self.start_time_restriction: Stime = None
        self.end_time_restriction: Stime = None
        self.ignore_time_restriction = False

        # Time Trackers
        self.interval = Tracker()
        self.elapsed = Tracker()

        # Bool
        self.running = True
        self.restricted = False

        super().__init__( **kwargs )


    # Default actions callbacks
    def click_function( self, ui_info ):
        infoLog(f"Clicking {self.current_task.match_selector} @task[{self.current_task.number}]")

        bounds = ui_info[ 'bounds' ]
        adbClick( bounds, self.current_task.offsetx, self.current_task.offsety )

        self.elapsed.trackS()
        return True


    def swipe_function( self, ui_info ):
        # Swipe
        infoLog(f"Swiping {self.current_task.match_selector} @task[{self.current_task.number}]", stdout=True)

        bounds = ui_info[ 'bounds' ]
        adbSwipeUi( bounds, self.current_task.swipe_direction, self.current_task.swipe_points )
        
        self.elapsed.trackS()
        return True


    def write_function( self, ui_info = None ):
        # Write
        infoLog(f"Writing {self.current_task.write_text} @task[{self.current_task.number}]")
        text = self.current_task.write_text

        # Clear text field first
        adbKeyCombo( ['KEYCODE_CTRL_LEFT','KEYCODE_A'], 'KEYCODE_DEL' )
        adbType( text )

        self.current_task.check_selector = {'text' : text, 'className' : Wtype.editText}
        self.elapsed.trackS()
        return True


    def doWait( self, ui_info ):
        self.elapsed.trackS()
        return True


    # No handle methods
    def doCheck( self ):
        # Wait for check ui to exists before switching task
        prev_task = self.tasks[ self.prev_task_number ]

        ui = self.waitElement( self.check_selector, timeout=prev_task.check_selector_timeout )
        if ui == None:
            NotifLog.recheck += 1
            notif_(1, f"Check failed:{prev_task.check_selector}")

            log = f"[{self}] check timedout [{prev_task.check_selector}] @task[{prev_task.number}]"
            debugLog( log )
            boxArea( name = log, overlap = False )

            self.current_task_number = self.prev_task_number
            return

        elif ui == "FAILED":
            return

        self.elapsed.trackS()

        notif_( 1, f"Checked[ {prev_task.number} ] [ {self.elapsed} ]")
        infoLog( f"Checked[{self.check_selector}] @task[{prev_task.number}]" )

        self.current_task_number = self.next_task_number


    def timeRestricted( self ):
        # Checks if runs at valid time
        if self.ignore_time_restriction or ( not self.start_time_restriction or not self.end_time_restriction ):
            return False
        stime = Stime()

        return stime.in_range( self.start_time_restriction, self.end_time_restriction )


if __name__=='__main__':
    pass
