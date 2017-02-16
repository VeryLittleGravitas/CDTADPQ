import esridump

def load_esri_source(url):
    '''
    '''
    return list(esridump.EsriDumper(url))