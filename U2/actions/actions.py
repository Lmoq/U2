import os, subprocess, sys, time
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent.parent) )
from U2.enums import Direction


def adbClick( uiBounds : dict, offsetx : int = 0, offsety : int = 0, log = False):
    # Click center of UiObject
    coo = uiBounds
    
    left = coo['left']
    right = coo['right']

    top = coo['top']
    bottom = coo['bottom']

    x = left + int(( right - left) / 2) + offsetx
    y = top + int(( bottom - top ) / 2) + offsety
    if log: print( f"Tapped {x} {y}" )
    os.system( f"echo input tap {x} {y} > ~/pipes/adbpipe &" )


def adbClickNoUi( coo : tuple, log = False ):
    # Click directly using adb shell
    x,y = coo
    if log: print( f"Tapped {x} {y}" )
    os.system( f"echo input tap {x} {y} > ~/pipes/adbpipe &" )


def adbSwipeUi( uiBounds : dict, direction : str, points : int, duration : int = 50 ):
    assert hasattr( Direction, direction ), "direction : left, up, right, down"

    coo = uiBounds

    left = coo['left']
    right = coo['right']

    top = coo['top']
    bottom = coo['bottom']

    x = left + int(( right - left) / 2)
    y = top + int(( bottom - top ) / 2)

    cm = ""

    match direction:
        case Direction.left:
            cm = f"input swipe {x} {y} {x-points} {y} {duration}"
        case Direction.up:
            cm = f"input swipe {x} {y} {x} {y-points} {duration}"
        case Direction.right:
            cm = f"input swipe {x} {y} {x+points} {y} {duration}"
        case Direction.down:
            cm = f"input swipe {x} {y} {x} {y+points} {duration}"

    os.system( f"echo '{cm}' > ~/pipes/adbpipe" )


def adbType( text : str ):
    command = f'''echo input text "{repr(text)}" > ~/pipes/adbpipe &'''
    os.system( command )


def adbKeyCombo( combo = [], key = None ):
    # combo - list of keys to press in combination
    # key - proceeding key to press
    # See https://gist.github.com/arjunv/2bbcca9a1a1c127749f8dcb6d36fb0bc for keylist
    keyS = " ".join( [f"{k}" for k in combo] )
    keyS += f"; input keyevent {key}" if key else ""

    os.system( f"echo input keycombination '{keyS}' > ~/pipes/adbpipe &" )


def vibrate( duration, times ):
    duration = int( duration * 1000 )
    cm = []
    for i in range( times ): 
        cm.append( f"termux-vibrate -f -d {duration} &" )
        time.sleep(0.2)
        subprocess.run(cm,shell=True)


def switch_keyboard( toggle : str = "on/off" ):
    # Set default ime
    if toggle.lower() == "on":
        subprocess.run( "adb shell ime set com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME", stdout=subprocess.DEVNULL, shell=True )
    # Disable keyboard
    elif toggle.lower() == "off":
        subprocess.run( "adb shell ime set com.wparam.nullkeyboard/.NullKeyboard", stdout=subprocess.DEVNULL, shell=True )


if __name__=='__main__':
    pass


