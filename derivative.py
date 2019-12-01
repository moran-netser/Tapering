import scipy

def _noZero( delta, epsilon = 0.01 ):
    if delta == 0:
        return epsilon
    return delta

def _derivativeWithDivideByZeroCompensation( y, x ):
    dy = scipy.diff( y )
    xDeltas = scipy.diff( x )
    dx = scipy.array( [ _noZero( delta ) for delta in xDeltas ] )
    assert all( dx != 0 ), "effect of _noZero should be evident"
    midpoints = ( x[ 1: ] + x[ :-1 ] ) / 2
    return midpoints, dy / dx

def derivative( y, x ):
    dy = scipy.diff( y )
    dx = scipy.diff( x )
    midpoints = ( x[ 1: ] + x[ :-1 ] ) / 2
    return midpoints, dy / dx
