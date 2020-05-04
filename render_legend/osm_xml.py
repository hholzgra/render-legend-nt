"""
Simple helpers for creating and pouplating an OSM XML file

Far froma complete library, only providing the most basic
parts really needed by render_legend
"""

from lxml import etree

def create_osm_tree():
    """ create OSM XML dom tree object
    version and lat/lon bounds are hard coded
    """
    osm = etree.Element("osm", {'version': '0.6', 'generator': 'create-legend'})
    osm.append(etree.Element("bounds", {'minlat': '-85', 'maxlat': '85', 'minlon': '-180', 'maxlon': '180'}))
    return etree.ElementTree(osm)

def create_osm_node(id, lat, lon, tags = {}):
    """ create OSM XML node element
    only caring about node id, position, and tags, none of the other node attributes
    """ 
    node = etree.Element('node', {'id': str(id), 'lat': str(lat), 'lon': str(lon), 'visible': 'true'})
    for key, value in tags.items():
        node.append(etree.Element('tag', {'k': key, 'v': str(value)}))
    return node

def create_osm_way(id, nodes, tags = {}):
    """ create OSM XML way element
    only caring about way id, node ids, and tags, none of the other way attributes
    """ 
    way = etree.Element('way', {'id': str(id), 'visible': 'true'})
    for node in nodes:
        way.append(etree.Element('nd', {'ref': str(node)}))
    for key, value in tags.items():
        way.append(etree.Element('tag', {'k': key, 'v': str(value)}))
    return way
