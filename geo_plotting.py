import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


class USMap(): 
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
        """Initalize the Basemap that holds the US map of counties."""

        fig = plt.figure(figsize=(20, 10))
        self.geo_map = Basemap(projection='aea', width=4750000, height=3500000, 
                    lat_1=24.,lat_2=55.,lat_0=38.5,lon_1=-125., 
                    lon_2 = -65., lon_0 = -97.5)
        self.geo_map.readshapefile(shapefile_path, self.geo_level)

