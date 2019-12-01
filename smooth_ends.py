import scipy
from tapering import derivative

class SmoothEnds:
    """
    attaches to a given motion (x and t vectors representing x(t) ) a pre and post "tail",
    such that the result is a motion that starts and ends at rest and
    attaches seemlessly to the original motion.
    """
    def __init__( self, x, t, tailDuration, resolution ):
        self._vFirst = ( x[ 1 ] - x[ 0 ] ) / ( t[ 1 ] - t[ 0 ] )
        self._vLast = ( x[ -1 ] - x[ -2 ] ) / ( t[ -1 ] - t[ -2 ] )
        self._x, self._t = x, t
        self._tailDuration = tailDuration
        self._resolution = resolution

    def _parameters( self, x, v, side ):
        assert side in [ 'left', 'right' ], "side must be 'right' or 'left'"
        alpha = v / ( 2 * self._tailDuration )
        beta = v
        gamma = x
        if side == 'right':
            alpha = - alpha
        return alpha, beta, gamma

    def _tailTrajectory( self, timePoint, side, parameters ):
        alpha, beta, gamma = parameters
        epsilon = self._tailDuration / self._resolution
        if side == 'left':
            start, stop = timePoint - self._tailDuration, timePoint
            stop -= epsilon
        else:
            start, stop = timePoint, timePoint + self._tailDuration
            start += epsilon
        tailTime = scipy.linspace( start, stop, self._resolution )
        tailPoints = alpha * ( tailTime - timePoint ) ** 2 + beta * ( tailTime - timePoint ) + gamma
        return tailTime, tailPoints

    def newTrajectory( self ):
        """
        returns a tuple (t, x, v) which represents the new motion
        in effect giving you x(t) and v(t)
        """
        x, t = self._x, self._t
        leftTailTime, leftTailX = self._tailTrajectory( t[ 0 ],
                                                        'left',
                                                        self._parameters( x[ 0 ], self._vFirst, 'left' ) )
        rightTailTime, rightTailX = self._tailTrajectory( t[ -1 ],
                                                         'right',
                                                         self._parameters( x[ -1 ], self._vLast, 'right' ) )
        newTime = scipy.concatenate( ( leftTailTime, t, rightTailTime ) )
        newX = scipy.concatenate( ( leftTailX, x, rightTailX ) )
        _, newV = derivative.derivative( newX, newTime )
        return newTime, newX, newV
