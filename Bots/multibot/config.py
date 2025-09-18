import os, json, sys
from pprint import pp
from pathlib import Path

root = Path(__file__).resolve().parent
sys.path.extend( [ str( root.parent / 'U2' ) ] )

from U2.notif import Stime


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


def saveJson( bot_list, save_json, path:Path=None ):
    # Save updated data base
    # Retrieve and set bot data from botlist to save_json
    extractJsonData( bot_list, save_json ) 

    if not isinstance( path, Path ):
        path = Path( path )

    path.parent.mkdir( parents = True, exist_ok = True )
    path.touch( exist_ok = True )

    with open( path, 'w' ) as f:
        json.dump( save_json, f, indent=4 )

    pp( save_json )


def loadJson( bot_list, out_json, merge=True, path:Path=None ):
    # Load data base to out_Json
    # If not merge, out_json will be refreshed and will only contain
    # keys from preset base_json or json file contents
    if not merge: out_json.clear()

    if not isinstance( path, Path ):
        path = Path( path )

    if not path.exists():
        # Fill data base contents
        saveJson( bot_list, out_json, path=path )
        print( f'Created {path}' )

    else:
        with open( path, 'r' ) as f:
            out_json |= json.load( f )

            compare_json = {}
            extractJsonData( bot_list, compare_json )

            # Check key differences whenever preset or json file keys gets updated
            diff = set( out_json.keys() ) ^ set( compare_json.keys() )

            if diff:
                # Sync the preset base_json and json file keys
                compare_json |= out_json
                out_json |= compare_json

        print( 'Existing data loaded' )
