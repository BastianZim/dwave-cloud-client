.. _resources_cloud:

=======
Clients
=======

The :term:`solver`\ s that provide sampling for solving :term:`Ising` and :term:`QUBO` problems, such
as a D-Wave 2000Q QPU or a software :term:`sampler` such as the `dimod <https://github.com/dwavesystems/dimod>`_
simulated annealing sampler, are typically remote resources. The D-Wave Cloud Client
:class:`~dwave.cloud.client.Client` class manages such remote solver resources.

Preferred use is with a context manager---a :code:`with Client.from_config(...) as`
construct---to ensure proper closure of all resources. The following example snippet
creates a client based on an auto-detected configuration file and instantiates
a solver.

>>> with Client.from_config() as client:   # doctest: +SKIP
...     solver = client.get_solver(num_qubits__gt=2000)

Alternatively, the following example snippet creates a client for software resources
that it later explicitly closes.

>>> client = Client.from_config(software=True)   # doctest: +SKIP
>>> # code that uses client
>>> client.close()    # doctest: +SKIP

Typically you use the :class:`~dwave.cloud.client.Client` class. By default, it instantiates
a QPU client. You can also use the specialized QPU and CPU/GPU clients directly.


Client (Base Client)
====================

.. automodule:: dwave.cloud.client
.. currentmodule:: dwave.cloud.client

Class
-----

.. autoclass:: Client

Properties
----------

.. autosummary::
   :toctree: generated

   Client.DEFAULTS

Methods
-------

.. autosummary::
   :toctree: generated

   Client.from_config
   Client.get_regions
   Client.get_solver
   Client.get_solvers
   Client.solvers
   Client.is_solver_handled
   Client.retrieve_answer
   Client.close


Specialized Clients
===================

Typically you use the :class:`~dwave.cloud.client.Client` class. By default, it instantiates
a QPU client. You can also instantiate a QPU or CPU/GPU client directly.

QPU Client
----------

.. automodule:: dwave.cloud.qpu
.. currentmodule:: dwave.cloud.qpu

Class
~~~~~

.. autoclass:: dwave.cloud.qpu.Client


Hybrid-Samplers Client
------------------------

.. automodule:: dwave.cloud.hybrid
.. currentmodule:: dwave.cloud.hybrid

Class
~~~~~

.. autoclass:: dwave.cloud.hybrid.Client


Software-Samplers Client
------------------------

.. automodule:: dwave.cloud.sw
.. currentmodule:: dwave.cloud.sw

Class
~~~~~

.. autoclass:: dwave.cloud.sw.Client
