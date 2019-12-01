from . import line_segment

class LineFunction:
    def __init__( self, lineSegments ):
        self._segments = lineSegments

    def firstPoint( self ):
        firstSegment = self._segments[ 0 ]
        return firstSegment.t0, firstSegment.x0

    def lastPoint( self ):
        lastSegment = self._segments[ -1 ]
        return lastSegment.t1, lastSegment.x1

    def points( self ):
        points = [ ( segment.t0, segment.x0 ) for segment in self._segments ]
        lastSegment = self._segments[ -1 ]
        points.append( ( lastSegment.t1, lastSegment.x1 ) )
        return points

    def domainSpan( self ):
        return self._segments[ -1 ].t1 - self._segments[ 0 ].t0

    @staticmethod
    def interpolateFromPoints( t, x ):
        segments = []
        currentT, currentX = t[ 0 ], x[ 0 ]
        for t_, x_ in list( zip( t, x ) )[ 1: ]:
            segment = line_segment.LineSegment( currentT, currentX, t_, x_ )
            segments.append( segment )
            currentT, currentX = t_, x_

        segments[ -1 ].inclusive = True
        return LineFunction( segments )

    def __call__( self, t ):
        segment = self._findSegment( t )
        return segment.x( t )

    def _findSegment( self, t ):
        for segment in self._segments:
            if t in segment:
                return segment

        assert False, f'could not find segment for {t}'

    def intersection( self, point, slope ):
        for segment in self._segments:
            intersection = segment.intersection( point, slope )
            if intersection is not None:
                return intersection

        return None
