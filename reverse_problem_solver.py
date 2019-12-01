import scipy
import logging
import fractions
import tapering.tail_smoother

class ReverseProblemSolver:
    """
    ReverseProblemSolver does what its name suggests for a particular profile.
    parameters:
        profile: a Profile object
        waistLength: the length of the waist of the taper (also=final hotzone length)
        resolution: how many points to use on the z-axis
        smoothing: a tuple (startFraction, windowSize) - performs a moving
                   average smoothing starting at startFraction (e.g. 0.80 to start at 80% along the z-axis before the waist)
                   using windowSize points for the moving average window.

    the object exposes z, L, x, and also pre-smoothing vectors originalL, originalX
    """
    def __init__( self, profile, waistLength, resolution, smoothing ):
        logging.info( 'starting ReverseProblemSolver' )
        LInitial = profile.r( 0 )**(-2) * ( 2 * profile.integrate( profile.zFinal ) + profile.waistRadius**2 * waistLength )
        logging.info( f'LInitial={LInitial}' )
        zPoints = scipy.linspace( 0, profile.zFinal, resolution )

        rPoints = scipy.array( list( map( profile.r, zPoints ) ) )
        LPoints = ( profile.r( 0 )**2 * LInitial - 2 * profile.integrate( zPoints ) ) / ( rPoints**2 )
        xPoints = 2 * zPoints + LPoints - LInitial

        startFraction, windowSize = smoothing
        startIndex = int( len( LPoints ) * startFraction )
        logging.info( f'startIndex={startIndex} startX={xPoints[startIndex]}' )
        smoothL = tapering.tail_smoother.movingAverage( LPoints, startIndex, windowSize )
        smoothX = 2 * zPoints + smoothL - LInitial
        self._assertMonotinicallyIncreasing( smoothX )

        self.profile = profile
        self.z = zPoints
        self.L = smoothL
        self.x = smoothX
        self.originalL = LPoints
        self.originalX = xPoints
        logging.info( 'finishing ReverseProblemSolver' )

    def _assertMonotinicallyIncreasing( self, x ):
        for i, delta in enumerate( scipy.diff( x ) ):
            if delta < 0:
                raise AssertionError( f'x not monotonically increasing: index={i} x[{i}]={x[i]} x[{i+1}]={x[i+1]}' )
