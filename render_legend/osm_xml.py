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

def add_osm_element(osm, type, zoom, tags = {}):
    """ add legend element to a given OSM DOM tree

    valid types are:
    * point:     single POI
    * line:      linear element, like e.g. a road
    * smalline:  smaller version of "line"
    * rectangle: rectangular area, twice as wide as high
    * square:    quadratic area
    """
    dlon = 0.006 * (2**13)/(2**zoom)   #length
    dlat = 0.003 * (2**13)/(2**zoom)   #height

    if type == 'point':
        tags['point'] = 'yes'
        osm.append(create_osm_node(1, 0, 0, tags))
        return (-dlon/2, -dlat, dlon/2, dlat)

    if type == 'line':
        osm.append(create_osm_node(1, 0, -dlon/2))
        osm.append(create_osm_node(2, 0, dlon/2))
        osm.append(create_osm_way(3, (1, 2), tags))
        return (-dlon/2, -dlat/2*1.5, dlon/2, dlat/2*1.5)

    if type == 'smallline':
        osm.append(create_osm_node(1, 0, -dlon/2*0.6))
        osm.append(create_osm_node(2, 0, dlon/2*.06))
        osm.append(create_osm_way(3, (1, -2), tags))
        return (-dlon/2, -dlat/2*1.5, dlon/2, dlat/2*1.5)

    if type == 'rectangle':
        osm.append(create_osm_node(1,  dlat/2, -dlon/2))
        osm.append(create_osm_node(2,  dlat/2,  dlon/2))
        osm.append(create_osm_node(3, -dlat/2,  dlon/2))
        osm.append(create_osm_node(4, -dlat/2, -dlon/2))
        tags["area"] = "yes"
        osm.append(create_osm_way(5, (1,2,3,4,1), tags))
        return (-3/4*dlon, -3/4*dlat, 3/4*dlon, 3/4*dlat)

    if type == 'square':
        osm.append(create_osm_node(1,  dlat/2, -dlat/2))
        osm.append(create_osm_node(2,  dlat/2,  dlat/2))
        osm.append(create_osm_node(3, -dlat/2,  dlat/2))
        osm.append(create_osm_node(4, -dlat/2, -dlat/2))
        tags["area"] = "yes"
        osm.append(create_osm_way(5, (1,2,3,4,1), tags))
        return (-3/4*dlon, -3/4*dlat, 3/4*dlon, 3/4*dlat)

    if type == 'rectanglepoint':
        osm.append(create_osm_node(1,  dlat/2, -dlon/2))
        osm.append(create_osm_node(2,  dlat/2,  dlon/2))
        osm.append(create_osm_node(3, -dlat/2,  dlon/2))
        osm.append(create_osm_node(4, -dlat/2, -dlon/2))
        osm.append(create_osm_node(5, 0, 0, tags))
        tags['name'] = 'name'
        tags["area"] = 'yes'
        osm.append(create_osm_way(6, (1,2,3,4,1), tags))
        return (-3/4*dlon, -3/4*dlat, 3/4*dlon, 3/4*dlat)

    if type == 'squarepoint':
        osm.append(create_osm_node(1,  dlat/2, -dlat/2))
        osm.append(create_osm_node(2,  dlat/2,  dlat/2))
        osm.append(create_osm_node(3, -dlat/2,  dlat/2))
        osm.append(create_osm_node(4, -dlat/2, -dlat/2))
        osm.append(create_osm_node(5, 0, 0, tags))
        tags['name'] = 'name'
        tags["area"] = 'yes'
        osm.append(create_osm_way(6, (1,2,3,4,1), tags))
        return (-3/4*dlon, -3/4*dlat, 3/4*dlon, 3/4*dlat)

    raise ValueError("Unknown element type '%s'" % type)
