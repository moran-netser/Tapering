import dataclasses

@dataclasses.dataclass
class LineSegment:
    t0: float
    x0: float
    t1: float
    x1: float
    inclusive: bool = False

    def __post_init__( self ):
        assert self.t1 > self.t0, f"must have t1 > t0, but t1={self.t1} and t0={self.t0}"
        self.slope = ( self.x1 - self.x0 ) / ( self.t1 - self.t0 )

    def __contains__( self, t ):
        if self.inclusive:
            return self.t0 <= t <= self.t1
        else:
            return self.t0 <= t < self.t1

    def x( self, t ):
        if not ( self.t0 <= t <= self.t1 ):
            raise Exception( f'can only evaluate x if t is between {self.t0} and {self.t1}, however t={t}' )

        return self.x0 + self.slope * ( t - self.t0 )

    def intersection( self, point, slope ):
        mySlope = ( self.x1 - self.x0 ) / ( self.t1 - self.t0 )
        if mySlope == slope:
            raise Exception( "parallel lines do not intersect, or are the same line, anyway - I'm out!" )

        t_p, x_p = point
        tIntersection = ( self.x0 - x_p - mySlope * self.t0 + slope * t_p ) / ( slope - mySlope )
        if tIntersection not in self:
            return None
        xIntersection = self.x0 + mySlope * ( tIntersection - self.t0 )
        return tIntersection, xIntersection
