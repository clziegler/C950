#!/usr/bin/env python -u
# encoding: utf-8

import hash_table
import package
import parse_csv

PACKAGE_FILE = "./files/WGUPS_Package_File_CSV.csv"
DISTANCE_NAME_FILE = "./files/WGUDistanceNameData.csv"
DISTANCE_DATA_FILE = './files/WGUDistanceData.csv'

def parse_packages():
    """This returns the list of package data from WGUPS_Package_File_CSV.csv

    Space Complexity: O(n)

    Time Complexity: O(n)
        
    Returns:
       list: List containing csv data
       
    """
    packages = parse_csv.parse_csv(PACKAGE_FILE)
    return packages

def parse_distance_name_data():
    """This returns the list of package data from WGUDistanceNameData.csv

    Space Complexity: O(n)

    Time Complexity: O(n)
        
    Returns:
       list: List containing csv data
       
    """
    distance_names = parse_csv.parse_csv(DISTANCE_NAME_FILE)
    return distance_names

def parse_distances():
    """This returns the list of package data from WGUDistanceData.csv

    Space Complexity: O(n)

    Time Complexity: O(n)
        
    Returns:
       list: List containing csv data
       
    """
    distance_data = parse_csv.parse_csv(DISTANCE_DATA_FILE)
    return distance_data


def package_hashmap():
    """This returns the package hashmap

    Space Complexity: O(n)

    Time Complexity: O(n)
        
    Returns:
       hash_table.HashTable: packages hashtable
       
    """
    package_hash = hash_table.HashTable()
    packages = parse_packages()
    for i in packages:
        
        package_hash[i[0]] = package.Package(*i)

    return package_hash

def location_hashmap():
    """This returns the location and address hashmap

    Space Complexity: O(n)

    Time Complexity: O(n)
        
    Returns:
       hash_table.HashTable: location hashtable, address hashtable
       
    """
    name_hash = hash_table.HashTable()
    address_hash = hash_table.HashTable()
    full_address = parse_distance_name_data()
    
    for i, j in enumerate(full_address):
        name_hash.add(j[1], i)
        address_hash.add(j[2], i)

    return name_hash, address_hash


def get_distance_names(location1, location2, distance_table, names):
    """This takes 2 location names, and returns the distance between them
    Args:
        location1 (str): Location name
        
        location2 (str): Location name
        
        distance_table (distance_graph.DistanceGraph): Graph of the distances between every location
        
        names (hash_table.HashTable): HashTable containing location names

    Space Complexity: O(1)

    Time Complexity: O(1)
        
    Returns:
       float: the distance between the 2 locations
       
    """

    distance = distance_table[names.get(location1)][names.get(location2)]

    return distance


def get_distance_addresses(location1, location2, distance_table, addresses):
    """This takes 2 location names, and returns the distance between them
    Args:
        location1 (str): Address
        
        location2 (str): Address
       
        distance_table (distance_graph.DistanceGraph): Graph of the distances between every location
        
        addresses (hash_table.HashTable): HashTable containing addresses

    Space Complexity: O(1)

    Time Complexity: O(1)
        
    Returns:
       float: the distance between the 2 locations
       
    """

    distance = distance_table[addresses.get(location1)][addresses.get(location2)]

    return distance
