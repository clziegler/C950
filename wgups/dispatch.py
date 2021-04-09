#!/usr/bin/env python -u
# encoding: utf-8

from hash_table import HashTable



def plan_packages(packages, no1, no2):
    """This takes the hashmap of packages, groups them by address,
    and sorts the groups and places them into a truck dictionary
    or the "Any" dictionary based on priority

    Args:
        packages (hashtable.HashTable): The HashTable containing the package objects .
        no1 (truck.Tuck): A truck object
        no2 (truck.Tuck): A truck object

    Space Complexity: O(n)

    Time Complexity: O(n*m)
        
    Returns:
        hash_table.HashTable: hashtable containing the priority dictionaries

       
    """
    
    #Truck1 prioritizes AM deliveries, as well as the packages that need to be delivered together.
    #Truck2 prioritizes packages that need to be on truck 2, packages that are delayed, 
    #and packages that have a wrong addres.
    #All other packages without any special needs are placed into "Any"
    
    truck1, truck2 = no1.get_name(), no2.get_name()
    truck_load = HashTable()
    truck_load[truck1] = []
    truck_load[truck2] = []
    truck_load["Any"] = []
    evaluated = []

    #Group the packages by address
    address_group = dupe_addresses(packages) 
    
    #Loop though all the address groups 
    for items in address_group:
        address = items[0]
        package_group = items[1]
        comment = []
        deadline = []
        
        #Loop though all the packages in the address groups.
        #Add the comments and deadlines of each package in the group
        #This is so we can evaluate each package by all the comments and
        #deadline in the package group
        for package in package_group:   
            
            comment.append(packages[package].comment)
            deadline.append(packages[package].deadline)
            
        #When a package in the group matches the criteria:
        #If the group is not in the evaluated list,
        #place the whole package group into priority groups truck1, truck2, or "Any",
        #then add that package group to the evaluated list so it is not added to another priority group 
        if "Wrong address listed" in comment: 
            if [address,package_group] not in evaluated:
                truck_load[truck2].append([address,package_group]) 
                evaluated.append([address,package_group]) 

        elif "Can only be on truck 2" in comment:
            if [address,package_group] not in evaluated:
                truck_load[truck2].append([address,package_group])
                evaluated.append([address,package_group])

        elif "Must be delivered with 15, 19" in comment or packages[package].id == "13":
            if [address,package_group] not in evaluated:
                truck_load[truck1].append([address,package_group])
                evaluated.append([address,package_group])    

        elif "Delayed on flight---will not arrive to depot until 9:05 am" in comment:
            if [address,package_group] not in evaluated:
                truck_load[truck2].append([address,package_group])  
                evaluated.append([address,package_group]) 

        elif "10:30 AM" in deadline and "" in comment:
            if [address,package_group] not in evaluated:
                truck_load[truck1].append([address,package_group])
                evaluated.append([address,package_group])  
        else:
            if [address,package_group] not in evaluated:
                truck_load["Any"].append([address,package_group])  
                evaluated.append([address,package_group])
                
    return truck_load


def plan_truckload(payload, packages):
    """This takes the truck payload, groups into  Priority, Other, or Hold lists

    Logic in the function follows a similar flow as plan_packages

    Args:
        payload (list): List of address/package groups
        packages (hashtable.HashTable): The HashTable containing the package objects .

    Space Complexity: O(n)

    Time Complexity: O(n*m)
        
    Returns:
       list: List containing the Priority, Other, Hold lists

       
    """
    
   
   
    priority = []
    other = []
    hold = []
    evaluated = []
  
  
    for items in payload:
        comment = []
        deadline = []
        address = items[0]
        package_group = items[1]
        
        #Loop though all the packages in the address groups.
        #Add the comments and deadlines of each package in the group
        #This is so we can evaluate each package by all the comments and
        #deadline in the package group
        for package in package_group:
            comment.append(packages[package].comment)
            deadline.append(packages[package].deadline)

        #When a package in the group matches the criteria:
        #If the group is not in the evaluated list,
        #place the whole package group into lists priority, other, or hold,
        #then add that package group to the evaluated list so it is not added to another priority group 
        if "Wrong address listed" in comment:
            if [address,package_group] not in evaluated:
                hold.append([address,package_group])
                evaluated.append([address,package_group])

        if "AM" in deadline and comment != "Wrong address listed":
            if [address,package_group] not in evaluated:
                priority.append([address,package_group])
                evaluated.append([address,package_group])

        else:
            if [address,package_group] not in evaluated:
                other.append([address,package_group])
                evaluated.append([address,package_group])

    return [priority, other, hold]

def dupe_addresses(packages):
    """ Creates a list of address package groups

    This function takes the package id as key and the package address as the value. 
    It then puts them into anthoer dictionary where the address is the key and a list of 
    package ids where the packages in that list share the same address. This allows for more 
    efficient delivery of packages as they are grouped by the address to which they will be delivered

    Args:
        packages (hashtable.HashTable): The HashTable containing the package objects .
        
        Space Complexity: O(n)

        Time Complexity: O(n)

        Returns: 
            list: List containing the address, package id key value pairs
        
        """
 
    address_group = {}
    
    for id, package in packages: 
        if package.address not in address_group: 
            address_group[package.address] = [id] 
        else: 
            address_group[package.address].append(id)
    
    return list(address_group.items())
