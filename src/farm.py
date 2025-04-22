class Farm:

    def __init__(self, name, city, state, agriculture_types):
        self.name = name
        self.city = city
        self.state = state
        self.agriculture_types = agriculture_types

    def get_city_state_full(self):
        return self.city + ", " + self.state + ", " + "BRASIL"

    def get_name(self):
        return self.name

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_agriculture_types(self):
        return self.agriculture_types
