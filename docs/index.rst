.. kubeconf documentation master file, created by
   sphinx-quickstart on Mon Oct 22 09:33:20 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

KubeConf
========

**Lightweight Python module for creating, manipulating, and editing kubeconfig files**

Why not use or wrap ``kubectl config``? ``kubectl config`` is great and writing a Python wrapper is a fine solution. However, ``kubectl config`` is quite limited in functionality. I wanted more control over my kubernetes config. kubeconfig gives me that control. It doesn't use kubectl at all. Rather, it reads, edits, and writes config files entirely on its own.

Contents
========

.. contents::
    :local:
    :depth: 2

Basic Usage
-----------

1. Import the ``KubeConf`` object and create an instance. If no ``path`` argument is given *kubeconf* will look for a config following kubectl's method. First, it will look a ``$KUBECONFIG`` environment variable pointing to a config file. Otherwise, it will look for a config file in the ``~/.kube/`` directory.
2. ``.open()`` the file.
3. Make your changes.
4. ``.close()`` the file to write your changes to the file.  

.. code-block:: python

    # Import KubeConf
    from kubeconf import KubeConf

    # Initialize your file.
    k = KubeConf(path='path/to/config')

    # Add a cluster
    k.add_cluster(
        name='mycluster',
        server='...',
        certificate_authority_data='...',
    )

    # Commit change to the file.
    k.close()

API documentation
-----------------

.. autoclass:: kubeconf.KubeConf
    :members:


Contributing
------------


Download and install this repo from source, and move into the base directory.

.. code-block:: bash

    git clone https://github.com/Zsailer/kubeconf
    cd kubeconf

If you use pipenv, you can install a developement version:

.. code-block:: bash

   pipenv install --dev

Otherwise you can install a development version using pip

.. code-block:: bash
    
    pip install -e .



Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
