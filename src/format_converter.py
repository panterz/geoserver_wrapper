import sys, subprocess, os, argparse
from logtool import getLogger

"""
example user case

python format_converter.py -n=<name> -inf=<input format> -of=<output format> -ifo=<input file> -ofo=<output folder> -ct=<conversion type>
e.g.
python format_converter.py -n=test -inf=england_ct_2001.shp -of=england_ct_2001.kml -ifo=test/resources -ofo=test/resources -ct=ogr
"""

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='name')
    parser.add_argument('-inf', help='input file')
    parser.add_argument('-of', help='output file')
    parser.add_argument('-ifo', help='input folder')
    parser.add_argument('-ofo', help='output folder')
    parser.add_argument('-ct', help='coversion type')
    return parser.parse_args()


class Convertor(object):
    
    def __init__(self, ifrmt, ofrmt, ifolder, ofolder, ctype):
        """
        constructor for data covertor
        ifrmt --> input format
        ofrmt --> output format
        ofolder --> output folder
        ctype --> convertor type, it has to be OGR or FME
        """
        self.name = ifrmt.split(".")[0]
        self.ifrmt = ifrmt.split(".")[1]
        self.ofrmt = ofrmt.split(".")[1]
        self.ifolder = ifolder
        self.ofolder = ofolder
        self.ctype = ctype
        self.valid_formats = ['KML', 'GEOJSON', 'SHP', 'GML2', 'GML3', 'MAPINFO', 'MIF', 'CSV', 'DXF']
    
    def check_for_valid_format(self):
        """
        check if input and output format are valid
        """
        if self.ifrmt.upper() in self.valid_formats and self.ofrmt.upper() in self.valid_formats:
            return True
        else:
            return False
    
    
    def translate(self):
        """
        do the conversion
        """
        formats = {"KML": "KML", "GeoJSON": "GeoJSON", "Shp": "ESRI Shapefile", "GML": "GML", "CSV": "CSV", "DXF": "DXF", "MIF": "MapInfo File"}
        exts = {"KML": "kml", "GeoJSON": "json", "Shp": "shp", "GML": "xml", "CSV": "csv", "DXF": "dxf", "MIF": "mif"}
        if self.check_for_valid_format():
            cmd = ['ogr2ogr', '-f', formats[self.ofrmt.upper()], '%s/%s.%s' % (self.ifolder, self.name, exts[self.ofrmt.upper()]), "%s/%s.%s" % (self.ifolder, self.name, self.ifrmt)]
            print " ".join(cmd)
            subprocess.call(cmd)

if __name__ == '__main__':
    args = get_arguments()
    if args.n:
        convertor = Convertor(args.inf, args.of, args.ifo, args.ofo, args.ct)
        convertor.translate()