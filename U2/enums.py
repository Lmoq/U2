
class Wtype:
    clickable = "android.widget.TextView"
    text = "android.view.ViewGroup"
    button = "android.widget.Button"
    editText = "android.widget.EditText"
    image = "android.widget.ImageView"


class ActionType:
    action = 0
    click = 1
    swipe = 2
    write = 3
    wait = 4
    check = 5


class TaskType:
    check = 1000
    wait = 2000


class Direction:
    left = "left"
    up = "up"
    right = "right"
    down = "down"


# Custom enums
class ButtonInstancePos:
    # Center position of each button instance
    i3 = ( 360, 601 )
    i4 = ( 360, 745 )
    i5 = ( 360, 889 )
    i6 = ( 360, 1033 )

class ButtonInstanceBounds:
    # Instance check bounds
    i3 = { 'number' : 3, 'bounds' : {'bottom': 725, 'left': 0, 'right': 720, 'top': 581} }
    i4 = { 'number' : 4, 'bounds' : {'bottom': 869, 'left': 0, 'right': 720, 'top': 725} }
    i5 = { 'number' : 5, 'bounds' : {'bottom': 1013, 'left': 0, 'right': 720, 'top': 869} }
    i6 = { 'number' : 6, 'bounds' : {'bottom': 1157, 'left': 0, 'right': 720, 'top': 1013} }


