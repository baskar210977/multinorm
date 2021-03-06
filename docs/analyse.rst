.. include:: references.txt

.. _analyse:

Analyse
=======

Example
-------

A basic example and properties of `MultiNorm` were shown in :ref:`gs`.

On this page we continue with analysis methods using same example::

    from multinorm import MultiNorm
    mean = [10, 20, 30]
    covariance = [[1, 0, 0], [0, 4, 0], [0, 0, 9]]
    names = ["a", "b", "c"]
    mn = MultiNorm(mean, covariance, names)

Scipy
-----

For most computations, `Multinorm` uses `scipy`_. The :meth:`~MultiNorm.scipy`
property is a frozen `scipy.stats.multivariate_normal`_ object. It is cached,
accessing it multiple times doesn't incur any extra computations.
Note that `scipy.stats.multivariate_normal`_ has a ``cov_info`` object,
which contains a covariance matrix decomposition which is computed once and
cached. It is at this time undocumented, but it is a public property
and is what powers most computations in the scipy and in this class.

.. code-block:: python

    >>> s = mn.scipy
    >>> type(s)
    scipy.stats._multivariate.multivariate_normal_frozen


To present a consistent and complete API, `MultiNorm` re-exposes the functionality
of `scipy.stats.multivariate_normal`_, it is a wrapper.

Draw random samples from the distribution using :meth:`~MultiNorm.sample`::

    >>> points = mn.sample(size=2, random_state=0)
    >>> points
    array([[10.97873798, 20.80031442, 35.29215704],
           [ 9.02272212, 23.73511598, 36.7226796 ]])

Points are always given as arrays with shape ``(n_dim, n_points)``.

Evaluate the probability density function (PDF), call :meth:`~MultiNorm.pdf`::

    >>> mn.pdf(points)
    array([1.27661616e-03, 9.31966590e-05])

For ``log(pdf)`` (natural logarithm), call :meth:`~MultiNorm.logpdf`::

    >>> mn.logpdf(points)
    array([-6.66354232, -9.28079868])

There is also a ``cdf`` and ``logcdf`` method for the cumulative distribution function,
as well as ``entropy``. Since these are rarely needed, we didn't wrap them. But you
can still access them via the :meth:`~MultiNorm.scipy` property.

Marginal
--------

TODO: marginal

.. _analyse-conditional:

Conditional
-----------

TODO: conditional

.. _analyse-scipy:


Error propagation
-----------------

TODO: to_uncertainties, to_soerp, to_mcerp


Sigmas
------

TODO: sigma_distance
