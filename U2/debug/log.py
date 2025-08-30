import os, logging, sys
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent.parent) )
from U2.notif import getHour, getHourSec


class NotifLog:
    title = "U2"
    recheck = 0
    gInfo = 0
    timeout = 0
    total_duration = ""
    restarts = 0

    capacity = 4

    def __init__( self ):
        self.list = []


    def __lt__( self, string ):
        self.list.append( string )
        
        if len( self.list ) > NotifLog.capacity:
            self.list.pop( 0 )


    def __repr__( self ):
        l = self.list
        # Added layer of string quote marks
        # for termux notif content arg
        return ' '.join([f'--line "{t}"' for t in l ])

    
    def updateTitle( self ):
        NotifLog.title = f'U2 | RC : {NotifLog.recheck} | DR : {NotifLog.total_duration} | RS : {NotifLog.restarts}'

notiflog = NotifLog()

def notif_( timeStamp, log ):
    # Log to adb shell notifciation
    stamp = "" if not timeStamp else f"[ {getHourSec()} ] "
    log_ = stamp + log

    notiflog < log_
    notiflog.updateTitle()

    cm = f'''echo 'cmd notification post -S inbox {notiflog} -t "{NotifLog.title}" notif logs &> /dev/null' > ~/pipes/adbpipe'''
    os.system(cm)


# Setup Logging Module

# Get logger moules

class Logger:

    init = False

    def __init__( self, dir_="u2log" ):
        if Logger.init:
            return

        # Setup logger path
        self.dir_ = Path(".") / dir_
        ld = self.dir_

        ld.mkdir( parents = True, exist_ok = True )
            
        print(f"init logger : {Logger.init}")
        Logger.init = True
        print(f"Toggled init : {Logger.init}")

        # Call only once to avoid handlers being readded
        self.debug_logger = logging.getLogger( 'DebugLogger' )
        self.debug_logger.setLevel( logging.ERROR )

        self.info_logger = logging.getLogger( 'InfoLogger' )
        self.info_logger.setLevel( logging.INFO )

        # Setup file handlers
        debug_file_handler = logging.FileHandler( self.dir_ / "debug.log" )
        debug_file_handler.setLevel( logging.ERROR )

        info_file_handler = logging.FileHandler( self.dir_ / "info.log" )
        info_file_handler.setLevel( logging.INFO )

        # Set formatter
        self.formatter = logging.Formatter( fmt = "%(asctime)s | %(levelname)s : %(message)s", datefmt = "%Y-%m-%d %H:%M:%S" )

        debug_file_handler.setFormatter( self.formatter )
        info_file_handler.setFormatter( self.formatter )

        # Add filehandlers to logger handlers
        if not self.debug_logger.hasHandlers():
            self.debug_logger.addHandler( debug_file_handler )

        if not self.info_logger.hasHandlers():
            self.info_logger.addHandler( info_file_handler )

        self.debug_logger.propagate = False
        self.info_logger.propagate = False


logger = Logger(dir_ = "logs")


def debugLog( message : str ):
    logger.debug_logger.error( message )


def infoLog( message : str):
    logger.info_logger.info( message )

if __name__=='__main__':
    pass
