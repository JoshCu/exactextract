from ._exactextract import Feature


class GDALFeature(Feature):
    def __init__(self, f):
        Feature.__init__(self)
        self.feature = f

    def set(self, name, value):
        idx = self.feature.GetDefnRef().GetFieldIndex(name)

        if type(value) in (int, float, str):
            self.feature.SetField(idx, value)
            return

        import numpy as np

        if value.dtype == np.int64:
            self.feature.SetFieldInteger64List(idx, value)
        elif value.dtype == np.int32:
            self.feature.SetFieldIntegerList(idx, value)
        elif value.dtype == np.float64:
            self.feature.SetFieldDoubleList(idx, value)
        else:
            raise Exception("Unexpected type in GDALFeature::set")

    def get(self, name):
        return self.feature.GetField(name)

    def geometry(self):
        return bytes(self.feature.GetGeometryRef().ExportToWkb())

    def set_geometry(self, wkb):
        if wkb:
            from osgeo import ogr

            geom = ogr.CreateGeometryFromWkb(wkb)
            self.feature.SetGeometryDirectly(geom)
        elif self.feature.GetGeometryRef():
            self.feature.SetGeometry(None)

    def set_geometry_format(self):
        return "wkb"

    def fields(self):
        defn = self.feature.GetDefnRef()
        return [defn.GetFieldDefn(i).GetName() for i in range(defn.GetFieldCount())]


class JSONFeature(Feature):
    def __init__(self, f=None):
        Feature.__init__(self)
        if f is None:
            self.feature = {"type": "Feature"}
        elif hasattr(f, "__geo_interface__"):
            self.feature = f.__geo_interface__
        else:
            self.feature = f

    def set(self, name, value):
        if name == "id":
            self.feature["id"] = value
        else:
            if "properties" not in self.feature:
                self.feature["properties"] = {}
            self.feature["properties"][name] = value

    def get(self, name):
        if name == "id":
            return self.feature["id"]
        else:
            return self.feature["properties"][name]

    def geometry(self):
        if "geometry" in self.feature:
            import json

            return json.dumps(self.feature["geometry"])

    def set_geometry(self, geojson):
        if geojson:
            import json

            self.feature["geometry"] = json.loads(geojson)
        elif "geometry" in self.feature:
            del self.feature["geometry"]

    def set_geometry_format(self):
        return "geojson"

    def fields(self):
        fields = []
        if "id" in self.feature:
            fields.append("id")
        if "properties" in self.feature:
            fields += self.feature["properties"].keys()
        return fields
