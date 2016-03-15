import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import fiona
import numpy as np


class USMap(object): 
    """This docstring will describe how to interact with the USMap class. 

    This class will instantiate and create a US map (built on top of a 
    Basemap) object that can then be interacted with. For the time being, 
    this class will primarily be used as a base class for a State or 
    County object map in which I can plot an individual state or county.

    Parameters: 
    ----------
        shapefile_path: str
            holds a path to the shapefile that the map will be built on 
            top of. 
        geo_level: str
            holds the geographical level of granularity (state, county, etc.)
            that is in the inputted shapefile_path. 
    """

    def __init__(self, shapefile_path, geo_level): 
        self.geo_level = geo_level 
        self._initialize_map(shapefile_path)

    def _initialize_map(self, shapefile_path): 
        """Initalize the Basemap that holds the US map of counties.
        
        Args
        ----
            shapefile_path: str
                Holds the pathname to the shapefile for the map
        """

        fig = plt.figure(figsize=(20, 10))
        self.geo_map = Basemap(projection='aea', width=4750000, height=3500000, 
                    lat_1=24.,lat_2=55.,lat_0=38.5,lon_1=-125., 
                    lon_2 = -65., lon_0 = -97.5)
        self.geo_map.readshapefile(shapefile_path, self.geo_level)

class Statemap(): 
    """This docstring will describe how to interact with the Statemap class. 

    this class will take the instantiated usmap from the usmap class, and then 
    take it down to the state level by restricting it to the inputted state. 

    parameters: 
    -----------
        shapefile_path: str
            holds a path to the shapefile that the map will be built on 
            top of. 
        geo_level: str
            holds the geographical level of granularity (state, county, etc.)
            that is in the inputted shapefile_path. 
        state_name: str
    """

    fips_dict = {'Alabama': '01', 'Alaska': '02', 'Arizona': '04', 
            'Arkansas': '05', 'California': '06', 'Colorado': '08', 
            'Connecticut': '09', 'Deleware': '10', 
            'District of Columbia': '11', 'Florida': '12', 'Georgia': '13', 
            'Hawaii': '15', 'Idaho': '16', 'Illinois': '17', 'Indiana': '18', 
            'Iowa': '19' , 'Kansas': '20', 'Kentucky': '21', 'Lousiana': '22',
            'Maine': '23', 'Maryland': '24', 'Massachusetts': '25', 
            'Michigan': '26', 'Minnesota': '27', 'Mississippi': '28', 
            'Missouri': '29', 'Montana': '30', 'Nebraska': '31', 
            'Nevada': '32', 'New Hampshire': '33', 'New Jersey': '34', 
            'New Mexico': '35', 'New York': '36', 'North Carolina': '37', 
            'North Dakota': '38', 'Ohio': '39', 'Oklahoma': '40', 
            'Oregon': '41', 'Pennsylvania': '42', 'Rhode Island': '44', 
            'South Carolina': '45', 'South Dakota': '46', 'Tennessee': '47', 
            'Texas': '48', 'Utah': '49', 'Vermont': '50', 'Virgina': '51', 
            'Washington': '53', 'West Virginia': '54', 'Wisconsin': '55', 
            'Wyoming': '56'}

    def __init__(self, shapefile_path, geo_level, state_name): 
        self.state_name = state_name
        self.state_fips = fips_dict[self.state_name]
        self.geo_level = geo_level
        self._initialize_map(shapefile_path)
        self.lat_pnts = []
        self.lng_pnts = []

    def self._initialize_map(self, shapefile_path): 
        """Initalize the Basemap that holds the state map of counties.

        Args: 
        ----
            shapefile_path: str
                Holds a path to the shapefile that the map will be built
                on top of. 
        """
        
        src = fiona.open(shapefile_path)
        self._parse_to_state(src)
        self._calc_bounds()
        self._create_map()

    def _parse_to_state(self, src): 
        """Filter the USMap down to a state map now."""

        feats = [feature for feat in src for feature in \
                self._parse_feat(feat['geometry']['coordinates']) if \
                feat['properties']['STATEFP'] == self.state_fips]
        self.feats_arr = np.array(feats)

    def _parse_feat(self, feature): 
        """Parse a feature and grab the relevant parts. 

        For any feature that comes in, we need to consider it's 
        latitude and longitude points, and find the overall min/max. 
        latitude/longitude across all points. We'll use this to get the
        correct sizing of the end basemap that we want to plot. 

        Args: 
        ----
            feat: list
        """

        output_feats = []
        for feat in feature: 
            feat_arr = np.array(feat)
            output_feats.append(feat) 
            # Here is where we keep track of the min/max. of the lat/long. 
            # for this particular feature. 1 or two features have shape 
            # with only 1 element, and we can safely ignore those here. 
            if len(feat_arr.shape) > 1: 
                lng_pts_arr = feat_arr[np.where(feat_arr[:, 0] < 0)]
                lat_pts_arr = feat_arr[np.where(feat_arr[:, 1] > 0)]
                self.lng_pts.extend([lng_pts_arr[:, 0].max(), 
                    lng_pts_arr[:, 0].min()])
                self.lat_pts.extend([lat_pts_arr[:, 1].max(), 
                    lat_pts_arr[:, 1].min()])

        return output_feats

    def _calc_bounds(self): 
        """This will calculate the bounds/stipulations of our map. 
        
        Here, we'll calculate the lat/long of the corners of our map, 
        as well as the lat/long bounds of the map. We'll also calculate 
        where the center of the map needs to be. 
        """

        lng_pts_arr = np.array(self.lng_pts)
        lat_pts_arr = np.array(self.lat_pts)
        self._lat_min, self._lat_max = lat_pts_arr.min(), lat_pts_arr.max()
        self._lng_min, self._lng_max = lng_pts_arr.min(), lng_pts_arr.max()
        self._center_lng = (self._lng_max - self._lng_min) / 2 + self._lng_min
        self._center_lat = (self._lat_max - self._lat_min) / 2 + self._lat_min

    def _create_map(self): 
        """Build the map of the inputted state."""

        fig = plt.figure(figsize=(20, 10))
        # The first four arguments define the bounds of the box, with a 
        # padding of plus one. The next two are some standard specs., and 
        # the last give additional bounds to the box and where to center it. 
        self.geo_map = Basemap(llcrnrlon=self._lng_min - 1,
                llcrnrlat=self._lat_min - 1, urcrnrlon=self._lng_max + 1,
                urcrnrlat=self._lat_max + 1, resolution='l', projection='aea',
                lat_1=self._lat_min, lat_2=self._lat_max, 
                lon_0=self._center_lng, lat_0=self._center_lat)

        for feat in self.feats_arr: 
            if len(feat.shape) == 3:
                rows, cols = feat.shape[1], feat.shape[2]
                feat = feat.reshape(rows, cols)
            if len(feat.shape) > 1: 
                poly = self.geo_map(feat[:, 0], feat[:, 1])
                self.geo_map.plot(poly[0], poly[1])
