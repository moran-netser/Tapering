from matplotlib import pyplot as plt

MU = '\u03bc'

def setTitles( axes, x, y ):
    axes.set_xlabel( x )
    axes.set_ylabel( y )

def reverseProblemSolutionVSVienna( solver, inferHotzone ):
    figure = plt.figure()
    figure.suptitle( 'hotzone L(x)' )
    axes = figure.subplots()
    axes.plot( solver.x, solver.L, '-b', inferHotzone.elongation[ 1: ], inferHotzone.hotZone, '-r' )
    setTitles( axes, f'elongation ({MU}m)', f'hot zone length ({MU}m)' )
    return figure

def reverseProblemSolution( solver ):
    figure = plt.figure()
    figure.suptitle( 'hotzone L(x)' )
    axes = figure.subplots()
    axes.plot( solver.x, solver.L )
    setTitles( axes, f'elongation ({MU}m)', f'hot zone length ({MU}m)' )
    return figure

def directSolution( * solvers ):
    figure = plt.figure()
    names = [ solver.name for solver in solvers ]
    figure.suptitle( f'profile r(z) {names}' )
    axes = figure.subplots()
    args = []
    colors = 'br'
    for solver, color in zip( solvers, colors ):
        args.append( solver.z )
        args.append( solver.r )
        args.append( color )
    axes.plot( * args )
    setTitles( axes, f'z ({MU}m)', f'r ({MU}m)' )
    return figure

def reverseProblemSolutionNoSmoothing( solver ):
    figure = plt.figure()
    figure.suptitle( 'hotzone no-smoothing L(x)' )
    axes = figure.subplots()
    axes.plot( solver.originalX, solver.originalL )
    setTitles( axes, f'elongation ({MU}m)', f'hot zone length ({MU}m)' )
    return figure

def flame( stagesMotion ):
    figure = plt.figure()
    figure.suptitle( 'flame' )
    axes = figure.subplots()
    axes.plot( stagesMotion.time, stagesMotion.xFlame )
    axes.plot( stagesMotion.time, stagesMotion.envelope )
    axes.plot( stagesMotion.time, -stagesMotion.envelope )
    setTitles( axes, 'time (s)', f'position ({MU}m)' )
    return figure

def stages( stagesMotion ):
    figure = plt.figure()
    figure.suptitle( 'stages motion' )
    axes = figure.subplots()
    axes.plot( stagesMotion.time, stagesMotion.xLeft )
    axes.plot( stagesMotion.time, stagesMotion.xRight )
    setTitles( axes, 'time (s)', f'position ({MU}m)' )
    return figure

def smoothedStagesMotion( smoothEnds, side ):
    t, x, v = smoothEnds.newTrajectory()
    figure = plt.figure()
    figure.suptitle( f'smoothed stages motion - {side}' )
    axesArray = figure.subplots( 2, 1 )
    position, velocity = axesArray

    position.plot( t, x )
    setTitles( position, 'time (s)', f'position ({MU}m)' )

    velocity.plot( t[ :-1 ], v )
    setTitles( velocity, 'time (s)', f'velocity ({MU}m/s)' )
    return figure
