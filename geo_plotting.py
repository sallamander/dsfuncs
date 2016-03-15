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

    def _parse_to_state(self, src): 
        """Filter the USMap down to a state map now."""
        pass



