
import numpy

"""
A method that will be used to solve a nonlinear system of equations using the Newton Raphson method.
So, F(x) is a vector with the follwing components [f1(X), f2(X), ...] , where X is the vector of variables.
Using Taylor's theorem, the following statement can be obtained:

F(X) = F(X0) + DF(X0)*(delta X), where DF(X0) is the jacobian.

In this module, we will take a variable n which will say how many equations and variables have to be sovled.
It will then take the functions as a vector (which will lambda expressions or defined
functions). It is on the user that the functions from the user take in the same number of arguments as the number n
given. An iterative process using the numpy libraries then, the deltaX vector will be solved for until it becomes close
to machine 0 which means that the solution has been found.

"""
#The dx variable used for calculating the jacobian
CONST_dx = 0.001

CONST_Tolerance = 0.01

#args holds the functions
def NewtonSolve(N, initialGuess , systemOfFunctions):

    counter = 0
    X0 = initialGuess
    while(True):
        Jacobian = calculateJacobian(N,systemOfFunctions, X0)

        #create the system of equations to solve. DF(X0) * DeltaX = - F(X0). From this,
        #DeltaX can be solved for. DF(X0) is the Jacobian variable from the line before.
            #Now, create the vector F(X0)
        size = (N,1)
        MinusFX0 = numpy.zeros(size)

        for i in range(N):
            MinusFX0[i] = -systemOfFunctions[i](X0)

        deltaXVector = numpy.linalg.solve(Jacobian, MinusFX0)

        #deltaXVector = X1 - X0. Calculate X1 and use it for the next iteration
        #deltaXVector + X0 = X1
        for i in range(N):
            X0[i] = deltaXVector[i][0] + X0[i]

        counter+=1
        #to make sure an infinite loop isnt entered
        if(counter>100):
            break

        #if the delta x vector's norm is sufficiently small then quit the loop:
        norm = 0
        for i in range(N):
            norm += deltaXVector[i]**2

        norm = norm**(1./float(N))
        if(norm < CONST_Tolerance):
            break

    #returning the solution vector
    return X0


#Each function has to take a vector as input. the vector is the vector of variables X
#X0 is the vector about which the jacobian is calculated
def calculateJacobian(N,systemOfFunctions, X0):

    #create an N*N matrix of zeros for the jacobian
    size = (N,N)
    Jacobian = numpy.zeros(size)

    for r in range(N):
        for c in range(N):
            #r is the row of interest and c is the column of interest. The loop will go through one row at a time

            #the column value will dictate which element in the X vector to perturb. Perturb this x position at the
            #beginning of the loop and then remove the perturbation after calculate an approximation of the partial
            delfrBydelXcAtX0 = -systemOfFunctions[r](X0)/CONST_dx
            X0[c] = X0[c] + CONST_dx
            delfrBydelXcAtX0 += systemOfFunctions[r](X0)/CONST_dx

            Jacobian[r][c] = delfrBydelXcAtX0
            X0[c] = X0[c] - CONST_dx

    return Jacobian

