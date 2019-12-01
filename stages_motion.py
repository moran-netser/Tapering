import scipy
import logging
from . import derivative
from . import  triangular_wave

class StagesMotion:
    """
    converts the solution of the reverse problem (given here with the reverseProblemSolver parameter)
    to the motion of the stages, assuming an oscillatory model for the motion of the flame.

    parameters:
        elongationRate - microns/sec constant rate of the elongation of the taper
        flameTrips - number of trips that the flame is going to make (actually, number of oscillations*2 that the stages perform)
        initialStagesSeparation - initial distance between the stages
        reverseProblemSolver - a ReverseProblemSolver object containing an L(x) solution
        assertFastFlame - Enforces the condition that the flame motion is much more rapid that the elongation rate.
                          Set this to True to be a good physicist.
                          Set this to False if the enforcing fails and you want to debug it.

    exposes the following properties:
        envelope = the envelope of the flame oscilations
        time = time axis
        xFlame = motion of the center of oscilations in lab frame
        xRight = motion of right stage in lab frame
        xLeft = motion of left stage in lab frame
    """
    def __init__( self, elongationRate, flameTrips, initialStagesSeparation, reverseProblemSolver, assertFastFlame, style ):
        assert style in [ 'harmonic', 'by-trips', 'by-slope' ]
        solver = reverseProblemSolver
        time = solver.x / elongationRate
        periodTime = time[ -1 ] / ( 0.5 * flameTrips )
        flameOscillationFrequency = 2 * scipy.pi / periodTime

        _, L_changeRate = derivative.derivative( solver.L, time )
        relativeLChangeRate = L_changeRate / solver.L[ 1: ]
        hotzoneMaxRelativeChangeRate = max( abs( relativeLChangeRate ) )
        logging.info( f'hotzoneMaxRelativeChangeRate={hotzoneMaxRelativeChangeRate} flameOscillationFrequency={flameOscillationFrequency} ratio={flameOscillationFrequency / hotzoneMaxRelativeChangeRate}' )
        #if flameOscillationFrequency / hotzoneMaxRelativeChangeRate < 1.5:
        #   logging.error( f'flameOscillationFrequency={flameOscillationFrequency}, L_dot/L={hotzoneMaxRelativeChangeRate}' )
        #   logging.error( f'flameOscillationFrequency / (L_dot/L) = {flameOscillationFrequency / hotzoneMaxRelativeChangeRate}' )
        #if assertFastFlame == 'yes':
        #    raise Exception( 'Bad physics: L should change slowly relative to flame trips (we require omega/LchangeRate >= 1.5)' )

        logging.info( f'time spans: {time[0]} until {time[-1]}' )
        if style == 'harmonic':
            xFlame = 0.5 * solver.L * scipy.sin( flameOscillationFrequency * time )
        elif style == 'by-slope':
            triangularWaveBySlope = triangular_wave.by_slope.BySlope( envelope = ( time, 0.5 * solver.L ), slope = 1000 )
            xFlame = triangularWaveBySlope.value( time )
        else:
            triangularWave = triangular_wave.by_trips.ByTrips( time, 0.5 * solver.L, flameTrips )
            xFlame = triangularWave.value( time )
        xLeft = xFlame - 0.5 * ( solver.x + initialStagesSeparation )
        xRight = xFlame + 0.5 * ( solver.x + initialStagesSeparation )

        self.envelope = 0.5 * solver.L
        self.time = time
        self.xFlame = xFlame
        self.xRight = xRight
        self.xLeft = xLeft

        time1, vLeft = derivative.derivative( xLeft, time )
        time2, aLeft = derivative.derivative( vLeft, time1 )

        _, vRight = derivative.derivative( xRight, time )
        _, aRight = derivative.derivative( vRight, time1 )

        self.time1 = time1
        self.time2 = time2
        self.vLeft = vLeft
        self.vRight = vRight
        self.aLeft = aLeft
        self.aRight = aRight
