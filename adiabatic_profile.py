import scipy
import logging

class AdiabaticProfile:
    """
    an AdiabaticProfile object represents a profile function r(z)
    that is, the radius as a function of z.

    Once created the object is callable just like a function.

    The profile is made of three segments
    * strong slope linear segments
    * weak slope linear segments
    * exponentialy decaying segment c*exp(-k*z)

    parameters:
    alpha = strong linear slope angle
    beta = weaker linear slope angle
    rInitial = radius at z=0
    r1 = radius at the transition from the first slope to the second
    r2 = radius at the transition from the second linear segment to the exponential segment
    rFinal = radius at the beginning of the waist
    k = decay constant for exponential segment
    """

    def __init__( self, ** kwargs ):
        EXPECTED_PARAMETERS = { 'alpha', 'beta', 'k', 'r1', 'r2', 'rFinal', 'rInitial' }
        if set( kwargs.keys() ) != EXPECTED_PARAMETERS:
            raise Exception( f'you must provide: {EXPECTED_PARAMETERS}' )
        self.__dict__.update( kwargs )
        self._calculate()

    def _calculate( self ):
        alpha, beta, k, r1, r2, rFinal, rInitial = self.alpha, self.beta, self.k, self.r1, self.r2, self.rFinal, self.rInitial
        tanAlpha, tanBeta = scipy.tan( alpha ), scipy.tan( beta )
        z1 = self.z1 = ( rInitial - r1 ) / tanAlpha
        z2 = self.z2 = z1 + ( r1 - r2 ) / tanBeta;
        c = self.c = rInitial + z1 * ( tanBeta - tanAlpha )
        A = self.A = scipy.exp( k * z2 ) * ( c - z2 * tanBeta )
        self.zFinal = scipy.log( A / rFinal ) / k
        logging.info( f'zFinal(AdiabaticProfile version) = {self.zFinal:.4f}' )


    def __call__( self, z ):
        alpha, beta, k, z1, z2, rFinal, rInitial = self.alpha, self.beta, self.k, self.z1, self.z2, self.rFinal, self.rInitial
        tanAlpha, tanBeta = scipy.tan( alpha ), scipy.tan( beta )
        c = self.c
        A = self.A

        if z < z1:
            return rInitial - z * tanAlpha
        if z < z2:
            return c - z * tanBeta

        return A * scipy.exp( -k * z )
