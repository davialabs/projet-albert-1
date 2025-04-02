from functools import partial
from geopy.geocoders import Nominatim
import pandas as pd

class FindClosestTown():

    adress : str
    
    def __init__(self, adress : str):
        self.adress = adress 
        self.geolocator = Nominatim(user_agent="ProjDavia")  
        self.geocode = partial(self.geolocator.geocode, language="fr")

    def find_closest_town_hall():
        town_hall_data = pd.read_csv("data_mairies.csv")
        print(town_hall_data.head())

if __name__ == "__main__":
    fct = FindClosestTown("93 bis Avenue Achille Peretti")
    fct.find_closest_town_hall()
    

    