class hotel:
    name = ''
    country_name = ''
    city_name = ''
    price_per_night = ''
    adult_count = ''
    child_count = ''

    def __init__(self, name, country_name, city_name, price_per_night, adult_count, child_count):
        self.name = name
        self.country_name = country_name
        self.city_name = city_name
        self.price_per_night = price_per_night
        self.adult_count = adult_count
        self.child_count = child_count

    def to_dict(self):
        return {
            'name': self.name,
            'country_name': self.country_name,
            'city_name': self.city_name,
            'price_per_night': self.price_per_night,
            'adult_count': self.adult_count,
            'child_count': self.child_count
        }
