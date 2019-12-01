import scipy
from . import line_function

class BySlope:
    def __init__( self, *, envelope, slope ):
        t, x = envelope
        self._slope = slope
        self._envelopes = { 'top': line_function.LineFunction.interpolateFromPoints( t, x ),
                            'bottom': line_function.LineFunction.interpolateFromPoints( t, -x ) }
        self._caluculateTrips()
        self.value = scipy.vectorize( self.evaluate )

    def _caluculateTrips( self ):
        OTHER = { 'top': 'bottom', 'bottom': 'top' }
        current = self._envelopes[ 'top' ].firstPoint()
        points = [ current ]
        slope = -self._slope
        side = 'bottom'
        while True:
            nextPoint = self._envelopes[ side ].intersection( current, slope )
            if nextPoint is None:
                break
            points.append( nextPoint )
            slope = -slope
            side = OTHER[ side ]
            current = nextPoint

        otherEnvelope = self._envelopes[ OTHER[ side ] ]
        points.append( self._lastPoint( current, otherEnvelope, slope ) )

        t = [ pair[ 0 ] for pair in points ]
        x = [ pair[ 1 ] for pair in points ]
        self._wave = line_function.LineFunction.interpolateFromPoints( t, x )

    def _lastPoint( self, current, otherEnvelope, slope ):
        currentT, currentX = current
        lastPointT, _ = otherEnvelope.lastPoint()
        xFinal = currentX + slope * ( lastPointT - currentT )
        return lastPointT, xFinal

    def evaluate( self, t ):
        return self._wave( t )
