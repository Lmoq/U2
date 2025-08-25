import time


class Time:


    def __init__( self ):
        self.str = "00:00"
        self.seconds = 0


    def set_seconds( self, n : int ):
        if not isinstance( n, int ):
            self.str = "Error"
            return
        self.seconds = n

        # Convert int to time string
        hour = ( n // 3600 ) % 24
        mins = ( n // 60 ) % 60
        secs = ( n % 60 )

        _str = ""
        _str += f"{hour:02d}:" if hour else ""
        _str += f"{mins:02d}:{secs:02d}"
        self.str = _str


    def set_string( self, s : str ):
        if not isinstance( s, str ):
            self.seconds = 0
            self.str = "Error"
            return
        self.str = s

        # Convert time string to seconds
        _split = s.split( ':' )

        hour = int( _split[0] ) * 3600 if len( _split ) > 2 else 0
        mins = int( _split[-2] ) * 60
        secs = int( _split[-1] )

        self.seconds = hour + mins + secs


    def __repr__( self ):
        return self.str


class Tracker( Time ):


    def __init__( self, min_interval = 0 ):
        super().__init__()
        # List containers for tracked time
        self.shortL = []
        self.longL = []

        # Sum of every elapsed time calculated
        self.total_intervals = 0
        self.interval_list = []
        self.track_calls = 0

        # Limit
        self.min_interval = min_interval
        self.average_of_n = 0

        # Time class for average time interval
        self.avgTime = Time()


    def trackS( self ):
        self.shortL.append( time.time() )

        if len( self.shortL ) > 1:
            t = self.shortL
      
            interval = int( t[1] - t[0] )

            # Set a minimum interval to prevent messing with average interval
            if interval > self.min_interval:
                self.total_intervals += interval
                self.interval_list.append( t[1] )
                
                self.track_calls += 1

                # Calculate average
                aoN = self.average_of_n
                avg = self.get_total_avg() if not aoN else self.get_avg_of_n( aoN )

                self.avgTime.set_seconds( avg )
            self.set_seconds( interval )
            del t[0]


    def get_total_avg( self ):
        if self.track_calls:
            return self.total_intervals // self.track_calls
        return 0
            

    def get_avg_of_n( self, aoN : int ):
        if aoN and len( self.interval_list ) == aoN:
            return sum( self.interval_list ) / aoN
        return 0


    def reset_avg( self ):
        # Reset recorded avg time
        self.set_seconds( 0)
        self.avgTime.set_seconds( 0 )

        self.total_intervals = 0
        self.track_calls = 0

        self.shortL.clear()
        self.interval_list.clear()


    def __lt__( self, n ):
        assert isinstance( n, int )
        if not self.track_calls:
            return False
        return self.seconds < n


    def __gt__( self, n ):
        assert isinstance( n, int )
        if not self.track_calls:
            return False
        return self.seconds > n


    def __le__( self, n ):
        assert isinstance( n, int )
        if not self.track_calls:
            return False
        return self.seconds <= n


    def __ge__( self, n ):
        assert isinstance( n, int )
        if not self.track_calls:
            return False
        return self.seconds >= n


if __name__=='__main__':
    pass


