# project: p5
# submitter: mhashemineja
# partner: none
# hours: 12

import netaddr
import time
import sys
import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper
import re
import json
import numpy as np
import pyproj
import geopandas as gpd
from shapely.geometry import Polygon, box, Point


ip2location = pd.read_csv ('ip2location.csv')
index_in_ip2location = 0

def main():
    if len(sys.argv) < 2:
        print("usage: main.py <command> args...")
    elif sys.argv[1] == "ip_check":
        ips = sys.argv[2:]
        print(json.dumps(ip_check(ips)))
    elif sys.argv[1] == "region":
        zip_create(sys.argv[2],sys.argv[3])
    elif sys.argv[1] == "zipcode":
        zipcode_create(sys.argv[2])
    elif sys.argv[1] == "geo":
        graph_create(sys.argv[2],sys.argv[3])
    else:
        print("unknown command: "+sys.argv[1])
        
def ip_check(ips):
    ip_region = []
    for ip in ips:
        temp_dict = {}
        temp_dict["ip"]=str(ip)
        temp_dict["int_ip"]=int(netaddr.IPAddress(temp_dict["ip"]))
        s_time = time.time()
        temp_dict["region"]=region_check(temp_dict["int_ip"])
        temp_dict["ms"]= time.time() - s_time
        ip_region.append(temp_dict)
    return ip_region
def ip_check_2(ip):
    ip_region = str(ip)
    ans = int(netaddr.IPAddress(ip_region))
    return ans
def ip_check_3(ip):
    ip_region["region"]=region_check(ip_region["int_ip"])
    return ip_region["region"]
                                
def region_check(int_ip):
    global index_in_ip2location
    while True:
        if int_ip > ip2location["high"][index_in_ip2location]:
            index_in_ip2location += 1
        elif int_ip < ip2location["low"][index_in_ip2location]:
            index_in_ip2location -= 1
        else:
            return ip2location["region"][index_in_ip2location]


def zip_create(csv_file,name):
    with ZipFile(csv_file) as zf:
        with zf.open("rows.csv", "r") as f:
            tio = TextIOWrapper(f)
            rows = pd.read_csv(tio)

    rows["ip"] = letter_to_zero(rows["ip"])
    rows["ip"] = rows["ip"].apply(ip_check_2)
    rows = rows.sort_values("ip")
    rows["region"] = rows["ip"].apply(region_check)
    
    with ZipFile(name, "w", compression=ZIP_DEFLATED) as zf:
        with zf.open("rows.csv", "w") as f:
            rows.to_csv(f, index=False)
            
def letter_to_zero(nums):
    nums_to_return = []
    for j in range(len(nums)):
        word = ""
        for i in range(len(nums[j])):
            if re.match(r"[a-z]", nums[j][i]):
                word += "0"
            else:
                word += nums[j][i]
        nums_to_return.append(word)
    return nums_to_return

def zipcode_create(docs):
    string = ""
    with ZipFile(docs) as zf:
        for name in zf.namelist():
            with zf.open(name, "r") as f:
                tio = TextIOWrapper(f)
                string += str(tio.read()) + " \n"
    matches = []
    for match in re.findall(r"(CA|NY|WI|IL)\s(\d{5}-\d{4}|\d{5})?", string):
        if match[1] != "" and match[1] not in matches:
            matches.append(match[1])
            print(match[1])
    
def graph_create(proj, name = None):
    path = gpd.datasets.get_path("naturalearth_lowres")
    df = gpd.read_file(path).set_index("name")
    with ZipFile("server_log2.zip") as zf:
        with zf.open("rows.csv", "r") as f:
            tio = TextIOWrapper(f)
            rows = pd.read_csv(tio)
    print("step 1")
    df["colorname"] = "gray"
    df["occurances"] = 0
    for index in rows.index:
        if rows["region"][index] in df.index:
            df["occurances"][rows["region"][index]] += 1
    print("step 2")
    for index in df.index:
        if df["occurances"][index] > 1000:
            df["colorname"][index] = "red"
        elif df["occurances"][index] > 0:
            df["colorname"][index] = "orange"
    print("step 3")
    crs = pyproj.CRS.from_epsg(proj)
    our_window = box(crs.area_of_use.west, crs.area_of_use.south, crs.area_of_use.east, crs.area_of_use.north)
    europe = df.intersection(our_window)
    europe = europe[~europe.is_empty]
    europe = europe.to_crs("EPSG:"+str(proj))
    fig = europe.plot(color=df["colorname"], edgecolor="white",figsize=(5,5))
    
    fig.get_figure().savefig(name, format="svg")
    print("step 4")
def occurance_counter(rows_regions):
    for rows_region in rows_regions:
        if rows_region in 
# python3 main.py geo 3035 out.svg
if __name__ == '__main__':
    main()
