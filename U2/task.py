import sys
from pathlib import Path; sys.path.append( str(Path(__file__).parent.parent) )
from U2.enums import ActionType, TaskType


class Task( dict ):

    __preset__ = {
        "number" : 100,

        # Parent Match Selector
        "match_selector" : {},
        "match_alt" : {},
        "match_selector_timeout" : 10,

        "match_class_inclusion_list" : [],
        "match_function" : None,

        "next_function" : None,

        # Actions
        "action_type" : ActionType.action,
        "action_match_selector" : {},

            # Click
        "offsetx" : 0,
        "offsety" : 0,
        "noUiClick" : None,

            # Swipe
        "swipe_direction" : "up/left/right/down",
        "swipe_points" : 0,
        "swipe_duration" : 100,

            # Write
        "write_text" : "",

        # Callback function
        "callback" : None,
        "bHandle_callback" : True,

        # Check
        "check_selector" : {},

        # Task values
        "next_task_number" : int,
        "prev_task_number" : int
    }


    def __init__( self, *args, **kwargs ):        
        super().__init__( *args, **kwargs )
        self |= Task.__preset__


    def __getattr__( self, attr ):
        if not attr in self:
            raise AttributeError( f"Task has no attribute named '{attr}'")
        return self[ attr ]


    def __setattr__( self, attr, value ):
        if not attr in self:
            raise AttributeError( f"Task has no attribute named '{attr}'")
        self[ attr ] = value


if __name__=='__main__':
    pass
