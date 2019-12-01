import logging
logging.basicConfig( level = logging.INFO, format = '%(asctime)s %(levelname)s: %(message)s' )
import box
import argparse
import scipy
import tapering.reverse_problem_solver
import tapering.profile
import tapering.plots
import tapering.stages_motion
import tapering.smooth_ends
import tapering.scripts.infer_hotzone
from tapering import adiabatic_profile
from tapering import direct_problem_solver
from tapering import infer_hotzone
from tapering import vienna

PROBLEMS = box.Box( {
    'constant-hotzone': { 'profile': tapering.profile.Profile( rOfZ = lambda z: 62.5 * scipy.exp( -z*0.002), waistRadius = 0.22  ),
                          'waistLength': 5000,
                          'elongationRate': 100,
                          'trips': 80,
                          'help': 'waistLength==Linitial= decay length in exponential profile'
                         },
    'linear-profile': { 'profile': tapering.profile.Profile( rOfZ = lambda z: 62.5 - 0.005 * z, waistRadius = 0.1  ),
                        'waistLength': 5000,
                        'elongationRate': 1 / 0.015,
                        'trips': 80,
                        'help': '' },
    'vienna': {  'profile': tapering.profile.Profile( rOfZ = adiabatic_profile.AdiabaticProfile(
                                                                            alpha = vienna.alpha,
                                                                            beta = vienna.beta,
                                                                            k = vienna.k,
                                                                            r1 = vienna.r1,
                                                                            r2 = vienna.r2,
                                                                            rFinal = vienna.rFinal,
                                                                            rInitial = vienna.rInitial ),
                                                      waistRadius = vienna.rFinal  ),
                            'waistLength': 11000,
                            'elongationRate': 100,
                            'trips': 70,
                             'help': '' },
    }
)

def saveToCSV( filename, smoothEndsLeft, smoothEndsRight, solver, directSolver, stagesMotion ):
    logging.info( f'saving results into csv file: {filename}' )
    t, xLeft, vLeft = smoothEndsLeft.newTrajectory()
    _, xRight, vRight = smoothEndsRight.newTrajectory()
    time = stagesMotion.time
    xL = stagesMotion.xLeft
    xR = stagesMotion.xRight
    vL = stagesMotion.vLeft
    vR = stagesMotion.vRight

    #dxLeft = scipy.diff( xLeft ) / 1000
    #dxRight = scipy.diff( xRight ) / 1000
    #vLeft = vLeft / 1000
    #vRight = vRight / 1000
    #dt = scipy.diff( t )
    #assert len( dt ) == len( dxLeft ) == len( dxRight ) == len( vLeft ) == len( vRight )

    with open( filename, 'w' ) as f:
        f.write( 't,xLeft,xRight,vLeft,vRight\n' )
        for t, xLeft, xRight, vLeft, vRight in zip( t, xLeft, xRight, vLeft, vRight ):
            f.write( f'{t},{xLeft},{xRight},{vLeft},{vRight}\n' )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( 'problem', choices=PROBLEMS.keys() )
    parser.add_argument( 'style', choices=[ 'harmonic', 'by-trips', 'by-slope' ], help = 'calculate flame motion using one of these methods' )
    parser.add_argument( '--assert-fast-flame', dest='assertFastFlame', choices=[ 'yes', 'no' ], default='yes' )
    parser.add_argument( '--resolution', '-r', type=int, default=1000 )
    parser.add_argument( '--format', '-f', default='svg', help='format to use for plots, e.g. png, jpg, svg' )
    parser.add_argument( '--no-plot', dest='noPlot', action='store_true' )
    parser.add_argument( '--smoothing', default='(0.8, 100)', metavar='(startFraction, windowSize)' )
    # 0.8 100
    parser.add_argument( '--csv', default=None, metavar='FILENAME', help='save results to FILENAME in CSV format' )
    arguments = parser.parse_args()
    problem = PROBLEMS[ arguments.problem ]
    startFraction, windowSize = eval( arguments.smoothing )
    solver = tapering.reverse_problem_solver.ReverseProblemSolver(
            problem[ 'profile' ],
            waistLength = problem[ 'waistLength' ],
            resolution = arguments.resolution,
            smoothing = ( startFraction, windowSize ) )
    stagesMotion = tapering.stages_motion.StagesMotion( problem.elongationRate, problem.trips, tapering.CENTIMETER, solver, arguments.assertFastFlame, arguments.style )
    smoothEndsLeft = tapering.smooth_ends.SmoothEnds( stagesMotion.xLeft, stagesMotion.time,  tailDuration = 10, resolution = 250 )
    smoothEndsRight = tapering.smooth_ends.SmoothEnds( stagesMotion.xRight, stagesMotion.time,  tailDuration = 10, resolution = 250 )
    directSolver = direct_problem_solver.DirectProblemSolver( solver.L, solver.x, problem.profile.r( 0 ) )
    viennaValues = tapering.scripts.infer_hotzone.readViennaCSV( './vienna_microns.csv' )
    inferHotzone = infer_hotzone.InferHotzone( scipy.array( viennaValues.xLeft ), scipy.array( viennaValues.xRight ), initialSeparation = 0 )
    VIENNA_INITIAL_RADIUS_MICRONS = 62.5
    viennaDirectSolver = direct_problem_solver.DirectProblemSolver( inferHotzone.L, inferHotzone.x[ 1: ], VIENNA_INITIAL_RADIUS_MICRONS, 'Vienna' )

    figures = {'L_of_x': tapering.plots.reverseProblemSolution( solver ),
               'L_of_x_nosmoothing': tapering.plots.reverseProblemSolutionNoSmoothing( solver ),
               'flame': tapering.plots.flame( stagesMotion ),
               'stagesMotion': tapering.plots.stages( stagesMotion ),
               'smoothLeft': tapering.plots.smoothedStagesMotion( smoothEndsLeft, 'left' ),
               'smoothRight': tapering.plots.smoothedStagesMotion( smoothEndsRight, 'right' ),
               'directSolver': tapering.plots.directSolution( directSolver ),
               'tel_aviv_vs_vienna': tapering.plots.reverseProblemSolutionVSVienna( solver, inferHotzone ),
               'tel_aviv_vs_vienna_direct_solvers': tapering.plots.directSolution( directSolver, viennaDirectSolver )
               }


    for name, figure in figures.items():
        figure.savefig( f'{name}.{arguments.format}' )

    if arguments.csv is not None:
        saveToCSV( arguments.csv, smoothEndsLeft, smoothEndsRight, solver, directSolver, stagesMotion )

    if arguments.noPlot:
        logging.info( 'skipping plot due to user request' )
        return

    tapering.plots.plt.show()
