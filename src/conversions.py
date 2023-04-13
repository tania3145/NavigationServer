import utm


# class UVTConvertor:
#     def __init__(self):
#         (self.easting, self.northing, self.zone_number, self.zone_letter) = utm.from_latlon(45.74666101971023, 21.230468210382533)
#
#     def three_d_space_to_lat_lng(self, point):
#         (lat, lng) = utm.to_latlon(self.easting + point[0], self.northing - point[2], self.zone_number, self.zone_letter)
#         return lat, lng, point[1]
#
#     def lat_lng_to_three_d_space(self, lat, lng, level=0):
#         easting2, northing2, zone_number2, zone_letter2 = utm.from_latlon(lat, lng)
#         return easting2 - self.easting, level, -(northing2 - self.northing)


class LatLng:
    def __init__(self, lat, lng, level=0):
        self.lat = lat
        self.lng = lng
        self.level = level

    def to_utm(self):
        return UTM(*utm.from_latlon(self.lat, self.lng), self.level)

    def to_tuple(self):
        return self.lat, self.lng, self.level

    def to_blender_point(self, ):
        return self.to_utm().to_blender_point()


class UTM:
    def __init__(self, easting, northing, zone_number, zone_letter, level=0):
        self.easting = easting
        self.northing = northing
        self.zone_number = zone_number
        self.zone_letter = zone_letter
        self.level = level

    def to_lat_lng(self):
        return LatLng(*utm.to_latlon(self.easting, self.northing, self.zone_number, self.zone_letter), self.level)

    def to_blender_point(self):
        return BlenderPoint.from_utm(self)

    def to_tuple(self):
        return self.easting, self.northing, self.zone_number, self.zone_letter, self.level


UVT_ZERO_POINT_LAT_LNG = LatLng(45.74666101971023, 21.230468210382533)
UVT_ZERO_POINT_UTM = UVT_ZERO_POINT_LAT_LNG.to_utm()


class RecastNavMeshPoint:
    def __init__(self, vec3):
        self.position = vec3

    def to_blender_point(self):
        return BlenderPoint((self.position[0], -self.position[2], self.position[1]))

    def to_tuple(self):
        return self.position[0], self.position[1], self.position[2]


class BlenderPoint:
    def __init__(self, vec3, utm_zero_reference=UVT_ZERO_POINT_UTM):
        self.position = vec3
        self.utm_zero_reference = utm_zero_reference

    def to_recast_nav_mesh_point(self):
        return RecastNavMeshPoint((self.position[0], self.position[2], -self.position[1]))

    def to_utm(self):
        return UTM(self.utm_zero_reference.easting + self.position[0],
                   self.utm_zero_reference.northing + self.position[1],
                   self.utm_zero_reference.zone_number, self.utm_zero_reference.zone_letter, self.position[2])

    def to_lat_lng(self):
        return self.to_utm().to_lat_lng()

    @staticmethod
    def from_utm(utm_pos, utm_zero_reference=UVT_ZERO_POINT_UTM):
        return BlenderPoint((utm_pos.easting - utm_zero_reference.easting,
                             utm_pos.northing - utm_zero_reference.northing, utm_pos.level), utm_zero_reference)

    def to_tuple(self):
        return self.position[0], self.position[1], self.position[2]
