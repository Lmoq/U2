import sys
from pathlib import Path

# Resolve paths
root = Path(__file__).resolve().parent
sys.path.extend( [ str( root.parent / 'U2' ) ] )

from Bots.msbot import MSBot


class Bot_Handler:

    def __init__( self, Bot : MSBot ):
        self.bot = Bot
        
        self.name = ""
        self.key_name = ""
        self.instance_num = 0

        # Next activity time stamp
        self.next = 0

    def __repr__( self ):
        return self.name

if __name__=='__main__':
    pass
