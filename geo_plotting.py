"""A module for geographical plotting. 

This module contains classes for building geographical maps. At this 
point in time, it only contains the USMapBuilder class, which allows for 
the plotting of a US Map based of an inputted geography - country, 
region, state(s), and/or county (or counties).

"""
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import fiona
import numpy as np

class USMapBuilder(object): 
    """Builder for a US Map of an inputted geography. 

    USMapBuilder builds a US Map of a user inputted geography. It 
    allows for a map of the entire country, or a specified 
    region(s), state(s), and/or county(ies). It expects that a 
    shapefile of the state/county boundaries be passed in. It will 
    then parse the boundary to grab the specfied geographies to plot. 
    This allows allow for rather quick, easy geographical plotting of 
    the US, without the need to create separate shapefiles for 
    different boundaries. 

    While any shapefile of US state/county boundaries can be 
    passed in, the class has been tested with the boundaries found
    at census.gov: 

    https://www.census.gov/geo/maps-data/data/tiger-cart-boundary.html

    Note that the shapefile needs to be in 2D format when passed in. A 
    version of the following command was used to transfer the downloaded
    shapefiles from 3D to 2D: 

    ogr2ogr -f "ESRI Shapefile" -dim 2 output_2D.shp input_3D.shp

    Args: 
    ----
        shapefile_path: str
            Filepath pointing to the shapefile to read in and parse. 
        geo_level (optional): str
            Holds the geographical level to use for plotting 
            ('Country', 'State', 'County'). 
        region_names (optional): set (or other iterable) of strings 
            Holds the regions to use in our map. 
        state_names (optional): set (or other iterable) of strings
            Holds the state names to use in our map. 
        county_names (optional): set (or other iterable) of strings
            Holds the county names to use in our map. Only relevant
            and accessed if the `geo_level` is 'County' and  
            `state_names` is not empty. 
        figsize (optional): tuple of ints 
            Holds the size of the figure to create. 
        border_padding (optional): int 
            Holds the amount of padding to build around the map. 
        ax (optional): matplotlib.pyplot.Axes object 
            Holds an axis to plot the boundaries on. 
    """

    fips_dict = {'Alabama': '01', 'Alaska': '02', 'Arizona': '04', 
            'Arkansas': '05', 'California': '06', 'Colorado': '08', 
            'Connecticut': '09', 'Deleware': '10', 
            'District of Columbia': '11', 'Florida': '12', 'Georgia': '13', 
            'Hawaii': '15', 'Idaho': '16', 'Illinois': '17', 'Indiana': '18', 
            'Iowa': '19' , 'Kansas': '20', 'Kentucky': '21', 'Louisiana': '22',
            'Maine': '23', 'Maryland': '24', 'Massachusetts': '25', 
            'Michigan': '26', 'Minnesota': '27', 'Mississippi': '28', 
            'Missouri': '29', 'Montana': '30', 'Nebraska': '31', 
            'Nevada': '32', 'New Hampshire': '33', 'New Jersey': '34', 
            'New Mexico': '35', 'New York': '36', 'North Carolina': '37', 
            'North Dakota': '38', 'Ohio': '39', 'Oklahoma': '40', 
            'Oregon': '41', 'Pennsylvania': '42', 'Rhode Island': '44', 
            'South Carolina': '45', 'South Dakota': '46', 'Tennessee': '47', 
            'Texas': '48', 'Utah': '49', 'Vermont': '50', 'Virgina': '51', 
            'Washington': '53', 'West Virgina': '54', 'Wisconsin': '55', 
            'Wyoming': '56'}

    regions_dict = {'West': {'Washington', 'Montana', 'Idaho', 'Wyoming', 
                            'Colorado', 'Utah', 'Nevada', 'California', 
                            'Oregon'}, 
                    'Southwest': {'Arizona', 'New Mexico', 'Texas', 
                            'Oklahoma'}, 
                    'Midwest': {'North Dakota', 'South Dakota', 'Nebraska', 
                                'Kansas', 'Missouri', 'Iowa', 'Minnesota', 
                                'Wisconsin', 'Illinois', 'Indiana', 
                                'Ohio', 'Michigan'}, 
                    'Southeast': {'Arkansas', 'Louisiana', 'Alabama', 
                                  'West Virgina', 'Virgina', 'Kentucky', 
                                  'Tennessee', 'North Carolina', 
                                  'South Carolina', 'Georgia', 'Mississippi', 
                                  'Florida'}, 
                    'Northeast': {'Maine', 'Massachusetts', 'Rhode Island', 
                                  'Connecticut', 'New Hampshire', 'Vermont', 
                                  'New York', 'Pennsylvania', 'New Jersey', 
                                  'Deleware', 'Maryland'}
                    }  

    def __init__(self, shapefile_path, geo_level=None, region_names=None, 
                 state_names=None, county_names=None, figsize=None, 
                 border_padding=1, ax=None): 
        self.geo_level = 'Country' if not geo_level else geo_level
        self.figsize = figsize
        self.lat_pts = []
        self.lng_pts = []
        self.coord_paths_lst = []
        self.border_padding = border_padding 
        self.ax = ax 

        if region_names: 
            state_names = set(state_name for region_name in region_names \
                    for state_name in self.regions_dict[region_name])
        if self.geo_level == 'State' and state_names is None \
                and region_names is None: 
            raise Exception ('Must input state names for plotting.') 
        elif self.geo_level == 'County' and ((state_names is None 
                and region_names is None) or county_names is None): 
            raise Exception ('Must input state and county names for plotting.') 
        
        if self.geo_level == 'State': 
            self.state_names = set(state_names)
            self.state_fips = set(self.fips_dict[state_name] for state_name \
                in self.state_names)
        elif self.geo_level == 'County': 
            self.state_names = set(state_names)
            self.state_fips = set(self.fips_dict[state_name] for state_name \
                in self.state_names)
            self.county_names = set(county_names) 

        self._build_map(shapefile_path)

    def _build_map(self, shapefile_path): 
        """Build the Basemap that maps the inputted shapefile. 
        
        Implement all of the steps necessary for building the 
        map of the specified geography: 
            * Read in the shapefile
            * Parse the boundaries in the shapefile 
            * Calculate the boundaries/borders necessary to pass
              to Basemap
            * Initalize the Basemap
            * Plot the Basemap

        Args: 
        -----
            shapefile_path: str
                Holds the filepath of the shapefile to read in and 
                use for building of the Basemap. 
        """

        src = fiona.open(shapefile_path)  
        self._parse_paths(src)
        try: 
            self._calc_bounds()
        except ValueError as e: 
            raise Exception('Double check that you put in the appropriate state/county level shapefile that corresponds to the self.geo_level.')
        self._calc_corners()
        self._create_map()
        self._plot_map()
        src.close()

    def _parse_paths(self, src): 
        """Parse the basemap paths to use only what we want to plot.

        Run through each of the boundaries given in the opened 
        shapefile passed in and grab only those that correspond 
        to the specified geography (region, state, county). While
        parsing, keep track of the min/max lat/long coordinates to 
        later calculate the boundaries/borders of the Basemap with. 
        Store these in `self.lng_pts` and `self.lat_pts`, and store
        the parsed boundaries in `self.coord_paths_list`. 

        Args: 
        ----
            src: fiona.collection.Collection
                Inputted collection of boundaries that have been 
                grabbed from the shapefile (using fiona) inputted 
                to the class. 
        """
        
        noncontiguous = {'02', '15', '14', '66', '60', '69' ,'72', '78'}
 
        for feature in src: 
            country_mask = self.geo_level == 'Country' and \
                    feature['properties']['STATEFP'] not in noncontiguous
            state_mask = self.geo_level == 'State' and \
                    feature['properties']['STATEFP'] in self.state_fips
            county_mask = self.geo_level == 'County' and \
                    feature['properties']['STATEFP'] in self.state_fips and \
                    feature['properties']['NAME'] in self.county_names 
            
            if country_mask or state_mask or county_mask:  
                # This will return the coordinate paths that make
                # up a geometry. 
                lst_of_paths = feature['geometry']['coordinates']
                for coord_path in self._parse_lst_of_paths(lst_of_paths): 
                    self.coord_paths_lst.append(coord_path)

    def _parse_lst_of_paths(self, lst_of_paths): 
        """Parse a list of coordinate paths. 

        For any lst_of_paths that comes in, do the following: 
            * parse the coordinate path - this involves making 
              that the odd shapes that some of the paths are read
              in as are transformed in such a way that Basemap can 
              plot them; it also involves grabbing the max/min 
              lat/long and storing them in `self.lat_pts` and 
              `self.lng_pts`
            * yield the parsed coordinate path

        Args: 
        ----
            lst_of_paths: list of lat/long coordinates 
        """

        lst_of_paths = np.array(lst_of_paths)
        # Occasionally we get a list that has multiple 
        # lists of paths (unclear why), and the easiest 
        # way to handle this was to cast it to an 
        # np.ndarray and flatten it.  
        if lst_of_paths.shape[0] > 1: 
            lst_of_paths= lst_of_paths.flatten()

        for coord_path in lst_of_paths: 
            coord_path_arr = np.array(coord_path)
            # We don't want to parse the path if it's only 
            # one dimensional. 
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

        # The if statements are basically extra checking to make
        # sure there are no issues/errors. Occasionally with the 
        # filtering directly above we end up with no lat/long points
        # in the array. 
        if lng_pts_arr.shape[0] != 0: 
            lng_min, lng_max = lng_pts_arr.min(), lng_pts_arr.max()
            self.lng_pts.extend([lng_min, lng_max])
        if lat_pts_arr.shape[0] != 0: 
            lat_min, lat_max = lat_pts_arr.min(), lat_pts_arr.max()
            self.lat_pts.extend([lat_min, lat_max])

    def _calc_bounds(self): 
        """This will calculate the min/max lat/long of our map. 
        
        Use the `self.lng_pts` and `self.lat_pts` lists to calculate 
        the boundaries for our map. These lists hold the min/max
        lat/long of each path that was parsed (e.g. a kind of local
        min/max). Taking the min/max of these lists will give the 
        overall min/max of the lat/long (e.g. a kind of global min/max). 
        """

        lng_pts_arr = np.array(self.lng_pts)
        lat_pts_arr = np.array(self.lat_pts)
        
        self.lat_min, self.lat_max = lat_pts_arr.min(), lat_pts_arr.max()
        self.lng_min, self.lng_max = lng_pts_arr.min(), lng_pts_arr.max()
        self._center_lng = (self.lng_max - self.lng_min) / 2 + self.lng_min
        self._center_lat = (self.lat_max - self.lat_min) / 2 + self.lat_min

    def _calc_corners(self): 
        """This will calculate the lat/long at the corners of our map. 

        The lat/long at the corners will just be the lat/long min/max, 
        plus any padding to add. 
        """

        self._llcrnrlat = self.lat_min
        self._llcrnrlon = self.lng_min
        self._urcrnrlon = self.lng_max
        self._urcrnrlat = self.lat_max

        if self.geo_level == 'Country': 
            self._llcrnrlat -= 6
            self._urcrnrlon += 12 
        else: 
            self._llcrnrlat -= self.border_padding
            self._llcrnrlon -= self.border_padding
            self._urcrnrlon += self.border_padding
            self._urcrnrlat += self.border_padding

    def _create_map(self): 
        """Initialize the map of the inputted state."""

        if self.figsize and not self.ax: 
            fig = plt.figure(figsize=self.figsize)

        # The first four arguments define the bounds of the box, 
        # The next two are some standard specs., and the last give 
        # additional bounds to the box, where to center it, and 
        # an optional axis to plot on. 
        self.geo_map = Basemap(llcrnrlon=self._llcrnrlon,
                llcrnrlat=self._llcrnrlat, 
                urcrnrlon=self._urcrnrlon,
                urcrnrlat=self._urcrnrlat, 
                resolution='l', projection='aea',
                lat_1=self.lat_min, lat_2=self.lat_max, 
                lon_1=self.lng_min, lon_2=self.lng_max, 
                lon_0=self._center_lng, lat_0=self._center_lat, 
                ax=self.ax)
    
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
                self.geo_map.plot(poly[0], poly[1], color='black')

    def plot_points(self, points, markersize=8): 
        """Plot the inputted points on the self.geo_map stored on the class

        Args: 
        ----
            points: iterable of lat/long/color pairs 
                The input here should be an iterable, where each item contains
                the lat/long of a point to plot, along with the color of the
                marker that should be used to plot it. 
        """

        for point in points: 
            lon, lat, marker = point[0], point[1], point[2]
            # This line translates it to the x, y space of the 
            # self.geo_map. 
            x, y = self.geo_map(lon, lat)
            self.geo_map.plot(x, y, marker, markersize=markersize)

    def plot_boundary(self, filepath): 
        """Plot the inputted boundary on the initialized map.

        Use the `readshapefile` method available on a Basemap object
        to plot any boundaries given in the filepath. 
        
        Args: 
        ----
            filepath: str
                Holds a filepath of a shapefile that contains additional 
                boundaries to plot on the map. 
        """

        self.geo_map.readshapefile(filepath, name='Filepath boundaries', 
                color='blue')


