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

class StateMap(object): 
    """This docstring will describe how to interact with the Statemap class. 

    this class will take the instantiated usmap from the usmap class, and then 
    take it down to the state level by restricting it to the inputted state. 

    parameters: 
    -----------
        shapefile_path: str
            holds a path to the shapefile that the map will be built on 
            top of. 
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

    def __init__(self, shapefile_path, state_name): 
        self.state_name = state_name
        self.state_fips = self.fips_dict[self.state_name]
        self.lat_pts = []
        self.lng_pts = []
        self.coord_paths_lst = []
        self._initialize_map(shapefile_path)

    def _initialize_map(self, shapefile_path): 
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
        self._plot_map()

    def _parse_to_state(self, src): 
        """Filter the USMap down to a state map now."""

        for feature in src: 
            if feature['properties']['STATEFP'] == self.state_fips:  
                # This will return the coordinate paths that make
                # up a geometry (county here). 
                lst_of_paths = feature['geometry']['coordinates']
                for coord_path in self._parse_lst_of_paths(lst_of_paths): 
                    self.coord_paths_lst.append(coord_path)

    def _parse_lst_of_paths(self, lst_of_paths): 
        """Parse a list of coordinate paths. 

        For any lst_of_paths that comes in, there will be a bunch of 
        coordinate paths that we want to look at and do a couple of 
        things with. First off is that we'll want to actually store
        that coordinate path to map it later. We'll also want to 
        store the maximum/minimum longitude and latitude so that we 
        can get the correct sizing of our plot (although this will 
        occur in the _parse_coord_path) method. 

        Args: 
        ----
            lst_of_paths: list 
        """

        for coord_path in lst_of_paths: 
            coord_path_arr = np.array(coord_path)
            if len(coord_path_arr.shape) > 1: 
                self._parse_coord_path(coord_path_arr)
            yield np.array(coord_path)

    def _parse_coord_path(self, coord_path_arr): 
        """Parse a coordinate path. 

        Here we'll actually grab the maximum and minimum latitudes
        and longitudes that we can find in this particular coordinate
        path. 

        Args: 
        ----
            coord_path_arr: numpy.ndarray
        """
        # For a couple of points, the long is switched with the
        # lat., and so we have to filter those out first. Since
        # we're in the US, we know that this will be restricted 
        # to negative longitudes, and positive latitudes. 
        lng_pts_mask = np.where(coord_path_arr[:, 0] < 0)
        lat_pts_mask = np.where(coord_path_arr[:, 1] > 0)

        lng_pts_arr = coord_path_arr[lng_pts_mask][:, 0]
        lat_pts_arr = coord_path_arr[lat_pts_mask][:, 1]

        lng_min, lng_max = lng_pts_arr.min(), lng_pts_arr.max()
        lat_min, lat_max = lat_pts_arr.min(), lat_pts_arr.max()
        self.lng_pts.extend([lng_min, lng_max])
        self.lat_pts.extend([lat_min, lat_max])

    def _calc_bounds(self): 
        """This will calculate the bounds/stipulations of our map. 
        
        Here, we'll calculate the lat/long of the corners of our map, 
        as well as the lat/long bounds of the map. We'll also calculate 
        where the center of the map needs to be. 
        """

        lng_pts_arr = np.array(self.lng_pts)
        lat_pts_arr = np.array(self.lat_pts)
        
        # In _parse_coord_path, we were looking for the local min/max of 
        # the lat/long. in a coordinate path. Here we're getting it globally
        # across all paths that are included in this map. 
        self._lat_min, self._lat_max = lat_pts_arr.min(), lat_pts_arr.max()
        self._lng_min, self._lng_max = lng_pts_arr.min(), lng_pts_arr.max()
        self._center_lng = (self._lng_max - self._lng_min) / 2 + self._lng_min
        self._center_lat = (self._lat_max - self._lat_min) / 2 + self._lat_min

    def _create_map(self): 
        """Initialize the map of the inputted state."""

        fig = plt.figure(figsize=(20, 10))
        # The first four arguments define the bounds of the box, with a 
        # padding of plus one. The next two are some standard specs., and 
        # the last give additional bounds to the box and where to center it. 
        self.geo_map = Basemap(llcrnrlon=self._lng_min - 1,
                llcrnrlat=self._lat_min - 1, urcrnrlon=self._lng_max + 1,
                urcrnrlat=self._lat_max + 1, resolution='h', projection='aea',
                lat_1=self._lat_min, lat_2=self._lat_max, 
                lon_1=self._lng_min, lon_2=self._lng_max, 
                lon_0=self._center_lng, lat_0=self._center_lat)
    
    def _plot_map(self): 
        """Plot the paths on the initialized map."""

        for feat in self.coord_paths_lst: 
            # Even though I put the data into 2D format before using it,
            # there were still a couple of 3D data points that lead to issues.
            # Ignoring them didn't seem to cause any problems. 
            if len(feat.shape) == 3:
                rows, cols = feat.shape[1], feat.shape[2]
                feat = feat.reshape(rows, cols)
            if len(feat.shape) > 1: 
                poly = self.geo_map(feat[:, 0], feat[:, 1])
                self.geo_map.plot(poly[0], poly[1])

class CountyMap(StateMap):
    """This docstring will describe how to interact with the CountyMap class

    This CountyMap class will filter out the inputted GIS data down to 
    the inputted state and county, and then build a Basemap using the 
    GIS boundary for that county. It will obtain almost all of it's 
    functionality from the StateMap class that it inherits from, but 
    will override _initalize_map method and replace the _parse_to_state
    with _parse_to_county. 

    parameters: 
    -----------
        shapefile_path: str
            holds a path to the shapefile that the map will be built on 
            top of. 
        state_name: str
        county_name: str
    """

    def __init__(self, shapefile_path, state_name, county_name): 
        self.state_name = state_name
        self.county_name = county_name
        self.state_fips = self.fips_dict[self.state_name]
        self.lat_pts = []
        self.lng_pts = []
        self.coord_paths_lst = []
        self._initialize_map(shapefile_path)

    def _initialize_map(self, shapefile_path): 
        """Initalize the Basemap that holds the state map of counties.

        Args: 
        ----
            shapefile_path: str
                Holds a path to the shapefile that the map will be built
                on top of. 
        """
        
        src = fiona.open(shapefile_path)
        self._parse_to_county(src)
        self._calc_bounds()
        self._create_map()
        self._plot_map()

    def _parse_to_county(self, src): 
        """Filter the USMap down to a state map now."""

        for feature in src: 
            if feature['properties']['STATEFP'] == self.state_fips and \
                feature['properties']['NAME'] == self.county_name: 
                # This will return the coordinate paths that make
                # up a geometry (county here). 
                lst_of_paths = feature['geometry']['coordinates']
                for coord_path in self._parse_lst_of_paths(lst_of_paths): 
                    self.coord_paths_lst.append(coord_path)
