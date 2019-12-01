import scipy

class DirectProblemSolver:
    """
    solves the direct problem
    given L(x) and the initial radius,
    calculates the r(z) function implicitly,
    e.g. as two vectors r, and z

    exposes: r, z
    """
    def __init__( self, L, x, rInitial, name = '' ):
        dx = scipy.diff( x )
        integral = -0.5 * ( dx / L[:-1] ).cumsum()
        integral = scipy.concatenate( ( scipy.array( [ 0 ] ), integral ) )
        self.r = rInitial * scipy.exp( integral )
        self.z = 0.5 * ( L[ 0 ] + x - L )
        self.name = name
