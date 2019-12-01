import logging
import functools
import tapering
import scipy.optimize
import scipy.integrate

class Profile:
    """
    a Profile object takes a profile function r(z) and the waist radius.
    The object can the perform an integral of particular interest to the reverse-problem,
    and also calculate the z value at which the r(z) profile reaches the waist radius (known as zFinal).
    """
    def __init__( self, rOfZ, waistRadius ):
        self.r = rOfZ
        self.waistRadius = waistRadius
        self.integrate = scipy.vectorize( self._integrate )

    @property
    def zFinal( self ):
        return self._calculateFinalZ()

    @functools.lru_cache()
    def _calculateFinalZ( self ):
        zFinalFinder = lambda z: self.r(z) - self.waistRadius
        zFinal = scipy.optimize.bisect( zFinalFinder, 0, 10 * tapering.CENTIMETER )
        logging.info( f'zFinal(Profile version)={zFinal:.4f}' )
        return zFinal

    def _integrate( self, z ):
        rSquared = lambda z: self.r(z) ** 2
        result, error = scipy.integrate.quad( rSquared, 0, z )
        return result
