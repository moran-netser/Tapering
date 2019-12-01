from matplotlib import pyplot as plt
import scipy
import pandas
import logging
import IPython
logging.basicConfig( level = logging.INFO, format = '%(asctime)s %(levelname)s: %(message)s' )
import argparse
import box
from tapering import infer_hotzone


def hotzoneVsElongation( inferHotzone ):
    simpleGraph( inferHotzone.elongation[ 1: ], inferHotzone.hotZone, 'hotzone vs. elongation' )

def flame( xRight, xLeft, time ):
    flame = 0.5 * ( xRight + xLeft )
    simpleGraph( time, flame, 'flame vs. time' )

def simpleGraph( t, y, title ):
    figure = plt.figure()
    figure.suptitle( title )
    axes = figure.subplots()
    axes.plot( t, y )

def readViennaCSV( csvFile ):
    result = box.Box()
    dataFrame = pandas.read_csv( csvFile )
    result.xLeft = dataFrame.dxLeft.cumsum()
    result.xRight = dataFrame.dxRight.cumsum()
    result.vLeft = dataFrame.dvLeft
    result.vRight = dataFrame.dvRight
    result.time = dataFrame.dtime.cumsum()
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument( '--ipython', action='store_true', help='open IPython shell once done' )
    parser.add_argument( '--plot', action='store_true', help='plot some graphs' )
    parser.add_argument( 'stagesTrajectoryCSV',
                         metavar='STAGES-TRAJECTORY-CSV-FILE',
                         help='csv file with the stages trajectories' )
    arguments = parser.parse_args()
    viennaValues = readViennaCSV( arguments.stagesTrajectoryCSV )
    inferHotzone = infer_hotzone.InferHotzone( scipy.array( viennaValues.xLeft ), scipy.array( viennaValues.xRight ), initialSeparation = 0 )
    if arguments.ipython:
        IPython.embed()
    if arguments.plot:
        hotzoneVsElongation( inferHotzone )
        flame( viennaValues.xRight, viennaValues.xLeft, viennaValues.time )
        simpleGraph( viennaValues.time, viennaValues.xRight, 'xRight vs. time' )
        simpleGraph( viennaValues.time, viennaValues.vRight, 'vRight vs. time' )
        plt.show()
