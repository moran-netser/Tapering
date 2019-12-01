import scipy
import logging

def movingAverage( array, startIndex, windowSize ):
    logging.info( f'movingAverage on array of size {len( array )}, startIndex={startIndex}, windowSize={windowSize}' )
    result = []
    s = scipy.sum( array[ startIndex - windowSize + 1: startIndex ] )
    for i in range( startIndex, len( array ) ):
        s += array[ i ]
        mean = s / windowSize
        result.append( mean )
        s -= array[ i - windowSize + 1 ]

    return scipy.concatenate( ( array[ :startIndex ], scipy.array( result ) ) )

def test_main():
    assert list( movingAverage( scipy.array( range( 10 ) ), 6, 3 ) ) == [ 0, 1, 2, 3, 4, 5, 5, 6, 7, 8 ]
    assert list( movingAverage( scipy.array( range( 10 ) ), 6, 4 ) ) == [ 0, 1, 2, 3, 4, 5, 4.5, 5.5, 6.5, 7.5 ]


if __name__ == '__main__':
    import time
    start = time.time()
    movingAverage( scipy.array( range( 500000 ) ), 1000, 100 )
    duration = time.time() - start
    print( f'it took {duration:.2f} seconds' )
