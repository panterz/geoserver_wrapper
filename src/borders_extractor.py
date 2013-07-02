import sys, argparse, ast, csv, os, zipfile, time
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring
import requests
from logtool import getLogger
from format_converter import Convertor

"""
example:
python borders_extractor.py -u='http://localhost:8081/geoserver/wfs' -w='ukb' -n='england_ct_2001' -fr='SHAPE-ZIP' -fi='{"label": [11, 12]}' -o='output'
"""

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='geoserver url')
    parser.add_argument('-w', help='data workspace')
    parser.add_argument('-n', help='data name')
    parser.add_argument('-fr', help='format')
    parser.add_argument('-fi', help='filters')
    parser.add_argument('-o', help='output folder')
    return parser.parse_args()

log = getLogger('Geoserver-Wrapper')

class GeoserverExtractor(object):
    
    def __init__(self, url, workspace, name, frmt, output, filters=None):
        """
        initialize
        """
        self.workspace = workspace
        self.name = name
        self.frmt = frmt
        self.filters = filters
        self.url = url
        self.output = output
        log.debug("init with workspace %s, name %s, format %s, filters %s, url %s and output folder %s" % (self.workspace, self.name, self.frmt, self.filters, self.url, self.output))
        self.start_time = time.time()
    
    def get_data(self):
        """
        do get request for getting the data
        """
        exts = {"SHAPE-ZIP": "zip", "CSV": "csv", "JSON": "json", "GML2": "xml", "GML3": "xml", "OGR-KML": "kml", "OGR-TAB": "zip", "OGR-TAB": "zip", "OGR-CSV": "csv", "DXF": "dxf"}
        params = {'service': 'WFS', 'request': 'GetFeature', 'version': '1.0.0', 'typeName': '%s:%s' %(self.workspace, self.name), 'outputFormat': self.frmt}
        if self.filters:
            params["filter"] = self.create_filter()
        try:
            if self.frmt == "DXF":
                params["outputFormat"] = "SHAPE-ZIP"
            r = requests.get(self.url, params=params)
        except Exception as e:
            log.debug("Failed to connect to tomcat. Start tomcat and try again.")
            sys.exit()
        if self.frmt.upper() == "CSV":
            name = 'tmp'
        else:
            name = self.name
        
        fil = os.path.join(os.environ["HOME"], 'local', 'geoserver_wrapper', 'data', self.output)
        if not os.path.exists(fil):
            os.mkdir(fil)
        try:
            log.debug("The format is %s" % exts[self.frmt])
            f = open(os.path.join('%s' % fil, '%s.%s' % (name, exts[self.frmt])), 'w')
            f.write(r.content)
            f.close()
        except Exception as e:
            log.debug("Wrong extension")
            sys.exit()
        if self.frmt == "DXF":
            #fh = open(os.path.join('%s' % fil, '%s.%s' % (name, exts[self.frmt])), 'rb')
            with zipfile.ZipFile(os.path.join('%s' % fil, '%s.%s' % (name, exts[self.frmt])), "r") as z:
                z.extractall(fil)
            
            convertor = Convertor("%s.%s" % (self.name, 'shp'), "%s.%s" % (self.name, exts[self.frmt]), fil, fil, "ogr")
            convertor.translate()
        if self.frmt.upper() == "CSV":
            self.csv_remove_geom()
        print time.time() - self.start_time, "seconds"
    
    def csv_remove_geom(self):
        """
        remove geom 
        """
        csv.field_size_limit(sys.maxint)
        with open("tmp.csv", "rb") as source:
            rdr = csv.reader(source)
            with open("%s.csv" % self.name, "wb") as result:
                wtr = csv.writer(result)
                l=0
                for r in rdr:
                    row = []
                    if l == 0:
                        n = self.find_geom_col(r)
                    if n >= 0:
                        row = self.create_row(r, n)
                    else:
                        row = r
                    print row
                    wtr.writerow(row)
                    l += 1
    
    def find_geom_col(self, row):
        """
        find which col is geom
        """
        i=0
        for el in row:
            if el == "the_geom":
                return i
            i += 1
        return -1
    
    def create_row(self, r, n):
        """
        create the new csv row
        """
        row = []
        j=0
        for el in r:
            #print el, n, j
            if n != j:
                print n, j
                row.append(el)
            j += 1
        return row
    
    def create_filter(self):
        """
        create filter
        """
        root = Element('wfs:GetFeature')
        root.set('service', 'WFS')
        child = SubElement(root, 'wfs:Query')
        child.set('typeName', self.name)
        if self.filters:
            filt = SubElement(child, 'ogc:Filter')
            filt.set('xmlns:ogc', '"http://www.opengis.net/ogc')
            filt1 = SubElement(filt, 'ogc:Or')
            label = ''
            for f in self.filters:
                label = f
                filters = self.filters[f]
            for fi in filters:
                filt2 = SubElement(filt1, 'ogc:PropertyIsLike')
                filt2.set('wildCard', '*')
                filt2.set('escapeChar', '#')
                filt2.set('singleChar', '!')
                filt3 = SubElement(filt2, 'ogc:PropertyName')
                filt3.text = label
                filt4 = SubElement(filt2, 'ogc:Literal')
                filt4.text = "%s*" % fi
        return tostring(root, 'utf8')

if __name__ == '__main__':
    args = get_arguments()
    url = args.u
    if url:
        workspace = args.w
        name = args.n
        frmt = args.fr
        output = args.o
        if args.fi:
            filters = ast.literal_eval(args.fi)
        else:
            filters = None
    else:
        url = 'http://localhost:8081/geoserver/wfs'
        workspace = 'ukb'
        name = 'england_ct_2001'
        frmt = 'SHAPE-ZIP'
        filters = {'label': [11, 12]}
    app = GeoserverExtractor(url, workspace, name, frmt, output, filters)
    app.get_data()