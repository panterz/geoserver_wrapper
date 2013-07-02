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
* MIF
* TAB


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

    fab deploy_local

Then you need to go to:

.. code-block::

    cd ~/local/geoserver_wrapper/
    . bin/activate
    cd src
    python borders_extractor.py -u='http://localhost:8081/geoserver/wfs' -w='<workspace>' -n='<name of dataset>' -fr='SHAPE-ZIP' -fi='{"label": [11, 12]}'


The arguments for th format are:
* Shapefile  --> -fr='SHAPE-ZIP'
* KML --> -fr='OGR-KML'
* GML2 --> -fr='GM2'
* GML3 --> -fr='GML3'
* Geojson --> -fr='JSON'
* CSV --> -fr='OGR-CSV'
* MIF --> fr-'OGR-MIF'
* TAB --> fr-'OGR-TAB'

