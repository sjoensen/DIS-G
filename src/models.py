
class Location(dict):
    def __init__(self, data: dict):
        super(Location, self).__init__(data)
        self.id = data.get('id')
        self.name = data.get('name')
        self.address = data.get('address')
        self.station = data.get('station')
        self.minutes_to_walk = data.get('minutes_to_walk')


class Station(dict):
    def __init__(self, data: dict):
        super(Station, self).__init__(data)
        self.name = data.get('name')
        self.area = data.get('area')


class Tag(dict):
    def __init__(self, data: dict):
        super(Tag, self).__init__(data)
        self.type = data.get('type')


class Amenity(dict):
    def __init__(self, data: dict):
        super(Amenity, self).__init__(data)
        self.id = data.get('id')
        self.name = data.get('name')


class Line(dict):
    def __init__(self, data: dict):
        super(Line, self).__init__(data)
        self.name = data.get('name')
        self.length = data.get('length')
