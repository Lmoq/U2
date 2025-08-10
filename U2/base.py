import traceback, sys, subprocess as sb

from pathlib import Path
sys.path.append( str(Path(__file__).parent.parent ) )

from U2.notif import Tracker, Stime
from U2.debug import NotifLog


class U2_Device:

    sig_term = False
    device = None # : uiautomator2.Device

    target_package = ""
    launch_activity = ""


    @staticmethod
    def init_device_session( device = None, package_name = None ):
        # Assign device attribute infos
        U2_Device.device = device
        package = package_name if package_name else device.info['currentPackageName'] 
        
        U2_Device.target_package = package
        U2_Device.launch_activity = U2_Device.get_launch_activity( package )


    @staticmethod
    def get_launch_activity( package_name ):
        result = sb.run( f"adb shell cmd package resolve-activity --brief {package_name} | tail -1", shell=True, capture_output=True )
        return result.stdout.decode().strip()


    def __init__( self, **kwargs ):
        self.tag = ""
        self.str = ""

        print("called base init")
        for k,v in kwargs.items():
            setattr( self, k, v )


    def waitElement( self, selector, timeout ):
        # Wait until ui element exists then returns UiObject
        try: 
            ui = self.__class__.device( **selector )

            return ui \
            if ui.wait( timeout=timeout ) \
            else None
        
        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stdout)
            return 'FAILED'


    def waitSiblingElement( self, base={}, sibling={}, timeout=0 ):
        try:
            ui = self.__class__.device( **base ).sibling( **sibling )

            return ui \
            if ui.wait( timeout=timeout ) \
            else None

        except Exception as e:
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stdout)
            return 'FAILED'


    def getInfo( self, ui ):
        success = False
        
        retries = 0
        info = None
        
        while not info:
            try:
                info = ui.info       
            except Exception:
                retries += 1
                if retries > NotifLog.gInfo:
                    NotifLog.gInfo = retries

        return info


    def __repr__( self ):
        return self.str or self.tag or str( self.__class__ ).split(".")[-1][:-2]



if __name__=='__main__':
    pass
