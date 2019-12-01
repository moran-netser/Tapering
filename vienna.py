import scipy

rInitial = 62.5
r1 = 43.5
r2 = 6
a = 0.005
b = 0.002
alpha = scipy.arctan( a )
beta = scipy.arctan( b )
k = 0.0004
rFinal = 0.1

if __name__ == '__main__':
    print( '=== VIENNA PARAMETERS ===' )
    params = dict( globals() )
    for k, v in params.items():
        if k.startswith( '_' ):
            continue
        print( f'{k} = {v}' )
