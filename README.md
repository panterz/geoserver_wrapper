geoserver_wrapper.py
====================


This script is for getting data from geoserver through python command line. The script is exporting
data that are in a Geoserver using the Geoserver WFS in various formats such as:
* Shapefile
* KML
* GML2
* GML3
* Geojson
* CSV


Requirements
=============

pip & virtualenv.

Installation instructions
=========================

.. code-block::
sudo apt-get install python-pip python-dev build-essential
sudo pip install --upgrade pip
sudo pip install --upgrade virtualenv

Installing script locally:

.. code-block::
    $ fab deploy_local

Then you need to go to:

.. code-block::
    $ cd ~/local/geoserver_wrapper/
    $ . bin/activate
    $ cd src
    $ python borders_extractor.py -u='http://localhost:8081/geoserver/wfs' -w='ukb' -n='england_ct_2001' -fr='SHAPE-ZIP' -fi='{"label": [11, 12]}'

