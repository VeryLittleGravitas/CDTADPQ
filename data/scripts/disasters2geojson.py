#!/usr/bin/env python
''' Output a line of GeoJSON for each disaster in sources.csv.
'''
import os, csv, sys, esridump

def iterate_features(filename):
    ''' Generate a stream of features for disasters.
    '''
    with open(filename) as file:
        for source in csv.DictReader(file):
            print('Reading {name} from {group}'.format(**source), file=sys.stderr)
            for feature in esridump.EsriDumper(source['url']):
                yield feature

def main():
    filename = os.path.join(os.path.dirname(__file__), 'sources.csv')
    for feature in iterate_features(filename):
        print(feature)

if __name__ == '__main__':
    exit(main())
