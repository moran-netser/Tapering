import scipy
from . import line_function
from . import line_segment

class ByTrips:
    def __init__( self, t, x, tripCount ):
        self._envelope = line_function.LineFunction.interpolateFromPoints( t, x )
        tripSegments = self._calculateTrips( tripCount )
        self._tripFunction = line_function.LineFunction( tripSegments )
        self.value = scipy.vectorize( self._tripFunction )

    def _calculateTrips( self, tripCount ):
        totalTime = self._envelope.domainSpan()
        deltaT = totalTime / tripCount
        currentT, currentX = self._envelope.firstPoint()
        tripSegments = []
        sign = -1
        for _ in range( tripCount - 1 ):
            newTime = currentT + deltaT
            newX = sign * self._envelope( newTime )
            trip = line_segment.LineSegment( currentT, currentX, newTime, newX )
            tripSegments.append( trip )
            currentT, currentX = newTime, newX
            sign = -sign

        lastTime, lastX = self._envelope.lastPoint()
        lastTrip = line_segment.LineSegment( currentT, currentX, lastTime, lastX, inclusive = True )
        tripSegments.append( lastTrip )
        return tripSegments

    def tripPoints( self ):
        return self._tripFunction.points()
