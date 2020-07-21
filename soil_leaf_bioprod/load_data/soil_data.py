import sys
from datetime import datetime
import time
import scylla_db
import csv


def layer_to_int(layer):
    if layer == "top":
        return 1
    elif layer =="middle" :
        return 2
    elif layer == "bottom":
        return 3

infer_type = True
def datestr(year, month, day):
    return year + "-" + month + "-" + day

def infer_type(col):
    try:
        val = float(col)
        return "float"
    except Exception as e:
        try:
            val = int(col)
            return "int"
        except Exception as e:
            val = str(col)
            return "text"
    return None

print(infer_type('1.0'))
print(infer_type('1'))
print(type(infer_type('A1.0')))
print(infer_type('A10A'))
print(infer_type('ABA'))



def convert_density_soil(soil_type, percent, depth):
    return (lambda area: area *soil_densities[soil_type] * percent / 100 * depth)
def get_mapping_array(headers, measurements, vals, mapping):
    for v in vals:
        row =
        dict(DATE_TS = row[1] + "-" + row[2] + "-" + row[3],REGION = str(row[4]),SUBREGION = str(row[5]),
    column_mapping = []
    i = 0
    while i < len(headers):
        irow_val = vals[i]
        irow_col = headers[i]
        imeasurement = measurements[i]
        irow_type = infer_type(irow_val)
        i += 1
        column_mapping.append([i, irow_col, irow_type, imeasurement])
    print(column_mapping)
    return column_mapping

soil_densities = {"SAND" : 0.0, "SILT" : 0.0, "CLAY" : 0.0}
soil_layer = [20,30,50]

class SOIL_ROW:
    def __init__(self, row):
        self.PLOT_ID = int(row[6])
        self.LATITUDE = float(row[9])
        self.LONGITUDE = float(row[10])
        self.ELEVATION = float(row[11])
        self.MAT = float(row[12])
        self.MAP = float(row[13])
        self.SOIL_DEPTH = float(row[14])
        self.layers = {1 : None, 2: None, 3 :None}
        self.add_layer(row)
    def add_layer(self, row):
        layer = layer_to_int(row[15])
        self.layers[layer] = dict(
        UPPER_DEPTH= float(row[16]) * self.SOIL_DEPTH / 100, 
        LOWER_DEPTH= float(row[17]) * self.SOIL_DEPTH / 100 ,
        BULK_DENSITY = float(row[18]),
        CARBON_CONTENT = float(row[19]),
        NITROGEN_CONTENT = float(row[20]),
        PH_OF_SOIL_LAYER = float(row[21]), 
        FRACTION_SAND = float(row[22]) / 100,
        FRACTION_SILT = float(row[23]) / 100, 
        FRACTION_CLAY = float(row[24]) / 100)

    def return_insert(self):
        retns = []
        for (val, layer) in self.layers.items():
            if layer is not None:
                retns.append([self.DATE_TS,self.ECOREGION, self.CLUSTER, self.PLOT_ID, self.LATITUDE,self.LONGITUDE,self.ELEVATION,self.MAT,self.MAP,self.SOIL_DEPTH, layer["UPPER_DEPTH"],layer["LOWER_DEPTH"],layer["BULK_DENSITY"],layer["CARBON_CONTENT"] ,layer["NITROGEN_CONTENT"] ,layer["PH_OF_SOIL_LAYER"],layer["FRACTION_SAND"],layer["FRACTION_SILT"],layer["FRACTION_CLAY"]])

        return retns
    '''
    def approx_densities(self):
        components = []
        layer_density = []
        for (layer,vals_layer) in self.layers.items():
            cm = vals_layer["LOWER_DEPTH"] - vals_layer["UPPER_DEPTH"]
            print(cm)
            sand_per_cm = -vals_layer["FRACTION_SAND"]
            silt_per_cm = vals_layer["FRACTION_SILT"]
            clay_per_cm = vals_layer["FRACTION_CLAY"]
            components.append([sand_per_cm, silt_per_cm, clay_per_cm])
            layer_density.append(vals_layer["BULK_DENSITY"] *cm / 10000)
        print(self.PLOT_ID)
        print(components)
        print(layer_density)
            
        x = np.linalg.solve(components, layer_density)
        return {"sand" : x[0], "silt" : x[1], "clay" : x[2]}
    '''
    def print_self(self):
        self_cols = "PROJECT YEAR MONTH DAY ECOREGION CLUSTER PLOT_ID LATITUDE LONGITUDE ELEVATION MAT MAP SOIL_DEPTH"
        print(len(self_cols.split(" ")))
        print(len(["%-10s |" for s in self_cols.split(" ")]))
        strr = "".join(["%-10s |" for s in self_cols.split(" ")])
        print(strr)
        print(strr % tuple(self_cols.split(" ")))
        print(strr % (self.PROJECT, self.YEAR ,self.MONTH ,self.DAY ,self.ECOREGION ,self.CLUSTER ,self.PLOT_ID ,self.LATITUDE,self.LONGITUDE ,self.ELEVATION,self.MAT ,self.MAP ,self.SOIL_DEPTH ))



def main(args):
    nodes = ["mms_scylla-node2_1", "mms_scylla-node3_1","mms_scylla-node1_1"]#, "mms_scylla-node2_1", "mms_scylla-node3_1", "mms_scylla-node4_1", "mms_scylla-node5_1", "mms_scylla-node6_1"]
    scylla_manager = scylla_db.scylla_db_manager(nodes, "nacp")

    f1 = open("data_csvs/NACP_TERRA_PNW_soil.csv", "r")
    f1_csv = csv.reader(f1)

    headers_soil = next(f1_csv)
    row = headers_soil
    measurements_soil = next(f1_csv)
    print(headers_soil)
    row0 = next(f1_csv)
    print(row0)
    columns = "CREATE TABLE SOIL_TRAIT (DATE_TS timestamp, REGION text,SUBREGION text,PLOT_ID int,LATITUDE float,LONGITUDE float,ELEVATION float,MAT float,MAP float,SOIL_DEPTH int,UPPER_DEPTH float,LOWER_DEPTH float,BULK_DENSITY float,CARBON_CONTENT int,NITROGEN_CONTENT int,PH_OF_SOIL_LAYER float,FRACTION_SAND float,FRACTION_SILT float,FRACTION_CLAY float, primary key (REGION, SUBREGION,LATITUDE, LONGITUDE))"

    rows_soil = get_mapping_array(headers_soil, measurements_soil,f1_csv, mapping)


main(sys.argv[1:])



    #scylla_manager.createTable("SOIL_TRAIT", columns_soil, types_soil,("LATITUDE", "LONGITUDE"))



main(sys.argv[1:])
