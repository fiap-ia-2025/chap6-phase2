class Farm:

    def __init__(self, name, city, state, agriculture_types):
        self.name = name
        self.city = city
        self.state = state
        self.agriculture_types = agriculture_types

    def get_city_state_full(self):
        return self.city + ", " + self.state + ", " + "BRASIL"
