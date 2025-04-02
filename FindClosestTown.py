from functools import partial
from geopy.geocoders import Nominatim
import pandas as pd
import folium

class FindClosestTown():

    adress : str
    
    def __init__(self, adress : str):
        self.adress = adress 
        self.geolocator = Nominatim(user_agent="ProjDavia")  
        self.geocode = partial(self.geolocator.geocode, language="fr")
        self.location = self.geocode(self.adress)
        self.reverse = partial(self.geolocator.reverse, language="fr")

    def find_closest_town_hall(self):
        town_hall_data = pd.read_csv("data_mairies.csv")
        min_dist2 = 1000
        for latitude, longitude in zip(town_hall_data['latitude'],town_hall_data['longitude']):
            if (latitude-self.location.latitude)**2 + (longitude-self.location.longitude)**2 < min_dist2:
                min_dist2 = (latitude-self.location.latitude)**2 + (longitude-self.location.longitude)**2
                minlat = latitude
                minlong = longitude
        return self.reverse(str(minlat) + "," + str(minlong))

if __name__ == "__main__":
    fct = FindClosestTown("Hardelot Neufchatel")
    cth = fct.find_closest_town_hall()
    print(cth)
    m = folium.Map((fct.location.latitude,fct.location.longitude), tiles="cartodb positron")
    folium.Marker(
        location=[cth.latitude, cth.longitude],
        tooltip="Click me!",
        popup="Town Hall",
        icon=folium.Icon(color="green"),
    ).add_to(m)
    folium.Marker(
        location=[fct.location.latitude, fct.location.longitude],
        tooltip="Click me!",
        popup="Adresse",
        icon=folium.Icon(color="red"),
    ).add_to(m)
    folium.Marker(
        location=[50.619594, 1.643270],
        tooltip="Click me!",
        popup="Adresse",
        icon=folium.Icon(color="blue"),
    ).add_to(m)
    m.save("map.html")

    