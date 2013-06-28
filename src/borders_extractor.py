import sys, argparse, ast, csv, os
from xml.etree.ElementTree import Element, SubElement, Comment, ElementTree, tostring
import requests, logging
from logging import handlers

"""
example:
python borders_extractor.py -u='http://localhost:8081/geoserver/wfs' -w='ukb' -n='england_ct_2001' -fr='SHAPE-ZIP' -fi='{"label": [11, 12]}'
"""

def getLogger(app):
    logger = logging.getLogger(app)
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    #fh = logging.FileHandler(config.get("path","log_file"))
    fh = handlers.TimedRotatingFileHandler(os.path.join(os.environ["HOME"], "local/geoserver_wrapper/logs/geoserver_wrapper.log"), when='midnight')
    fh.setLevel(logging.DEBUG)
    # create formatter and add it to the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    return logger

log = getLogger('Geoserver-Wrapper')

class GeoserverExtractor(object):
    
    def __init__(self, url, workspace, name, frmt, filters=None):
        """
        initialize
        """
        self.workspace = workspace
        self.name = name
        self.frmt = frmt
        self.filters = filters
        self.url = url
        log.debug("init with workspace %s, name %s, format %s, filters %s and url %s" % (self.workspace, self.name, self.frmt, self.filters, self.url))
    
    def get_data(self):
        """
        do get request for getting the data
        """
        exts = {"SHAPE-ZIP": "zip", "CSV": "csv", "JSON": "json", "GML2": "xml", "GML3": "xml", "OGR-KML": "kml", "OGR-TAB": "zip", "OGR-TAB": "zip", "OGR-CSV": "csv"}
        params = {'service': 'WFS', 'request': 'GetFeature', 'version': '1.0.0', 'typeName': '%s:%s' %(self.workspace, self.name), 'outputFormat': self.frmt}
        if self.filters:
            params["filter"] = self.create_filter()
        try:
            r = requests.get(self.url, params=params)
        except Exception as e:
            log.debug("Failed to connect to tomcat. Start tomcat and try again.")
            sys.exit()
        #print r.content
        log.debug("The format is %s" % exts[self.frmt])
        if self.frmt.upper() == "CSV":
            name = 'tmp'
        else:
            name = self.name
        f = open('%s.%s' % (name, exts[self.frmt]), 'w')
        f.write(r.content)
        f.close()
        if self.frmt.upper() == "CSV":
            self.csv_remove_geom()
    
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
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', help='geoserver url')
    parser.add_argument('-w', help='data workspace')
    parser.add_argument('-n', help='data name')
    parser.add_argument('-fr', help='format')
    parser.add_argument('-fi', help='filters')
    args = parser.parse_args()
    url = args.u
    if url:
        workspace = args.w
        name = args.n
        frmt = args.fr
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
    app = GeoserverExtractor(url, workspace, name, frmt, filters)
    app.get_data()