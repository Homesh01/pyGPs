#================================================================================
#    Marion Neumann [marion dot neumann at uni-bonn dot de]
#    Daniel Marthaler [marthaler at ge dot com]
#    Shan Huang [shan dot huang at iais dot fraunhofer dot de]
#    Kristian Kersting [kristian dot kersting at cs dot tu-dortmund dot de]
#
#    This file is part of pyGP_PR.
#    The software package is released under the BSD 2-Clause (FreeBSD) License.
#
#    Copyright (c) by
#    Marion Neumann, Daniel Marthaler, Shan Huang & Kristian Kersting, 30/09/2013
#================================================================================

from pyGPs.Core import *
import numpy as np

# Example demo for pyGP prediction of carbon dioxide concentration using 
# the Mauna Loa CO2 data [Pieter Tans, Aug 2012]. 
#
# The data is constantly updated and publically available under the link:
# ftp://ftp.cmdl.noaa.gov/ccg/co2/trends/co2_mm_mlo.txt
#
# The used covariance function was proposed in [Gaussian Processes for 
# Machine Learning,Carl Edward Rasmussen and Christopher K. I. Williams, 
# The MIT Press, 2006. ISBN 0-262-18253-X]. 
# 
# Copyright (c) by Marion Neumann and Daniel Marthaler, 20/05/2013



if __name__ == '__main__':

    # LOAD data
    infile = 'data_for_demo/mauna.txt'	# Note: Samples with value -99.99 were dropped.
    f      = open(infile,'r')
    year   = []
    co2    = []
    for line in f:
        z  = line.split('  ')
        z1 = z[1].split('\n')
        if float(z1[0]) != -99.99:
            year.append(float(z[0]))
            co2.append(float(z1[0]))
    X  = [i for (i,j) in zip(year,co2) if i < 2004]
    y  = [j for (i,j) in zip(year,co2) if i < 2004]
    xx = [i for (i,j) in zip(year,co2) if i >= 2004]
    yy = [j for (i,j) in zip(year,co2) if i >= 2004]

    x = np.array(X)
    y = np.array(y)
    x = x.reshape((len(x),1))
    y = y.reshape((len(y),1))
    n,D = x.shape

    # TEST POINTS
    xs = np.arange(2004+1./24.,2024-1./24.,1./12.)     
    xs = xs.reshape(len(xs),1)

    # DEFINE parameterized covariance function
    k1 = cov.RBF(np.log(67.), np.log(66.))
    k2 = cov.Periodic(np.log(1.3), np.log(1.0), np.log(2.4)) * cov.RBF(np.log(90.), np.log(2.4))
    k3 = cov.RQ(np.log(1.2), np.log(0.66), np.log(0.78))
    k4 = cov.RBF(np.log(1.6/12.), np.log(0.18)) + cov.Noise(np.log(0.19))
    k  = k1 + k2 + k3 + k4 
    
    # STANDARD GP (prediction)  
    model = gp.GPR()
    model.setData(x,y)
    model.plotData_1d()
    model.setPrior(kernel=k)
    model.predict(xs)


    # STANDARD GP (training)
    from time import clock
    t0 = clock()
    model.train(x,y)
    t1 = clock()
    model.predict(xs)

    print 'Time to optimize = ', t1-t0
    print 'Optimized mean = ', model.meanfunc.hyp
    print 'Optimized covariance = ', model.covfunc.hyp
    print 'Optimized liklihood = ', model.likfunc.hyp
    print 'Final negative log marginal likelihood = ', round(model._neg_log_marginal_likelihood_,3)
    
    model.plot()