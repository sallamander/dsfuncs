import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon
import fiona
import numpy as np

class USMapBuilder(object): 
    """This docstring will describe how to interact with the USMapBuilder
    class.
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
        self.state_fips = set()
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
        """Build the Basemap that maps the inputted shapefile"""

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
        """Parse the basemap paths to use only what we want to plot."""
        
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

        lst_of_paths = np.array(lst_of_paths)
        if lst_of_paths.shape[0] > 1: 
            lst_of_paths= lst_of_paths.flatten()

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

        if lng_pts_arr.shape[0] != 0: 
            lng_min, lng_max = lng_pts_arr.min(), lng_pts_arr.max()
            self.lng_pts.extend([lng_min, lng_max])
        if lat_pts_arr.shape[0] != 0: 
            lat_min, lat_max = lat_pts_arr.min(), lat_pts_arr.max()
            self.lat_pts.extend([lat_min, lat_max])

    def _calc_bounds(self): 
        """This will calculate the min/max lat/long of our map. 
        
        Here, we'll calculate the lat/long of the corners of our map, 
        as well as the lat/long bounds of the map. We'll also calculate 
        where the center of the map needs to be. 
        """

        lng_pts_arr = np.array(self.lng_pts)
        lat_pts_arr = np.array(self.lat_pts)
        
        # In _parse_coord_path, we were looking for the local min/max of 
        # the lat/long. in a coordinate path. Here we're getting it globally
        # across all paths that are included in this map. 
        self.lat_min, self.lat_max = lat_pts_arr.min(), lat_pts_arr.max()
        self.lng_min, self.lng_max = lng_pts_arr.min(), lng_pts_arr.max()
        self._center_lng = (self.lng_max - self.lng_min) / 2 + self.lng_min
        self._center_lat = (self.lat_max - self.lat_min) / 2 + self.lat_min

    def _calc_corners(self): 
        """This will calculate the lat/long at the corners of our map."""

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

        # The first four arguments define the bounds of the box, with a 
        # padding of plus one. The next two are some standard specs., and 
        # the last give additional bounds to the box and where to center it. 
        if self.figsize and not self.ax: 
            fig = plt.figure(figsize=self.figsize)

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
            points: iterable of lat/long/color pairs 
                The input here should be an iterable, where each item contains
                the lat/long of a point to plot, along with the color of the
                marker that should be used to plot it. 
        """

        for point in points: 
            lon, lat, marker = point[0], point[1], point[2]
            x, y = self.geo_map(lon, lat)
            self.geo_map.plot(x, y, marker, markersize=markersize)

    def plot_boundary(self, filepath): 
        """Plot the inputted boundary on the initialized map."""

        self.geo_map.readshapefile(filepath, name='Filepath boundaries', color='blue')


