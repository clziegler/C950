#!/usr/bin/env python -u
# encoding: utf-8
import data_table
import truck
import dispatch
import distance_graph
from collections import deque
import datetime
import re
import sys
 


class Wgups:
    """The main WGUPS program. It takes the users input and creates a report on the status of the 
    packages

    Parameters
    ----------
        truck1 :str 
            The name of the truck (default 'Truck 1)
        truck2 : str 
            The name of the truck (default 'Truck 2)

    Methods
    -------
        final_report():
            Prints the final report showing the final result of all packages, and the total milage traveled by
                both trucks
        get_time_package(time, package):
            Prints the status of a particular package at a given time
        get_time_all(time):
            Prints the status of all packages at a given time
          
    """

    def __init__(self, truck1 = "Truck 1", truck2 = "Truck 2"):
        #Ingest all the data from the CSV files, create the optimized adjacency matrix
        self._packages = data_table.package_hashmap()
        _, self._addresses = data_table.location_hashmap()
        self._distances = distance_graph.DistanceGraph(data_table.parse_distances())
        self._distance_optimized = self._distances.shortest_adj_matrix()

        #Instantiate the 2 delivery trucks
        self._no1 = truck.Truck(truck1, self._distance_optimized, self._addresses, start_time=[8, 0])
        self._no2 = truck.Truck(truck2, self._distance_optimized, self._addresses, start_time=[9, 5])

        #Group the packages by address, and plan how the trucks will be loaded by priority of the packages
        self._planned_packages = dispatch.plan_packages(self._packages, self._no1, self._no2) 
        self._title = [
            "\tPackage ID:",
            "Weight:",
            "Address:",
            "Delivery Truck:",
            "Due:",
            "Status:"
            ]
        self._truck_title = [
            "\n\tTruck Name:",
            "Miles Traveled:",
            "Time of Final Delivery:", 
            "Packages delivered:"
            ]
        self._evaluated = deque()


    def _deliver_packages(self):
        """The main program that delivers all the packages to 
        their destinations
        
        Space Complexity: O(n)

        Time Complexity: O(n^2*m*j)
        """

        while self._planned_packages:
            if len(self._planned_packages[self._no1.name]) == 0 and len(self._planned_packages[self._no2.name]) == 0 and len(self._planned_packages["Any"]) == 0:
                break
            
            self._no1.load_and_deliver_packages(self._planned_packages, self._packages)
            self._no2.load_and_deliver_packages(self._planned_packages, self._packages)
    
        
       
    def final_report(self):
        """Prints a report giving the status of all packages, 
        the status of the delivery trucks, the total number of delivered packages
        and the total combined truck milage 
        
        Space Complexity: O(n)

        Time Complexity: O(n^2*m*j)
        
        """
        self._deliver_packages()
        print(
            ("\n\t=============================="
            "==================================="
            "WGUPS Final Report:"
            " ==================================="
            "======================"))
        
        for i in sorted(self._packages, key=lambda x : int(x[0])):
            package, _ = i[0], i[1]
            self._evaluated.append(
                [
                    f"\t{self._packages[package].id}",
                    f'{self._packages[package].weight} lb. ',
                    self._packages[package].full_address(),
                    self._packages[package].truck,
                    self._packages[package].deadline,
                    f'Delivered {self._packages[package].on_time} at {self._packages[package].formatted_delivered_time()}'
                    ])
        self._evaluated.appendleft(self._title)
        print_list(self._evaluated)
        print_list([self._truck_title, self._no1.final_report_list(), self._no2.final_report_list()])

        print(
            "\t========================================================="
            f" Total miles traveled: {self._no1 + self._no2} "
            "==========================================================")
        print(
            "\t============================================================="
            f" Total packages: {self._no1.packages_delivered + self._no2.packages_delivered} "
            "===============================================================\n")  


    def get_time_package(self, time, package):
        """Prints a report giving the status of a package at a certain time

        Args:
            time (str): time of when to evaluate the package status
            package (str):  id of package 
        
        Space Complexity: O(1)

        Time Complexity: O(n^2*m*j)
        
        """

        try:
            self._packages[package]
        except KeyError:
            print(f"Could not find a package with id of {package}")
            sys.exit(2)
       
        self._deliver_packages()
        asked_time = parse_time(time)
       
        print(
            ("\n\t=================================================="
            f" WGUPS Status of Package {self._packages[package].id} at {time} "
            "====================================================="))
        
        self._evaluate_package_time(asked_time, package)
        self._evaluated.appendleft(self._title)
        print_list(self._evaluated)
    
    def get_time_all(self, time):
        """Prints a report giving the status of all package at a certain time

        Args:
            time (str): time of when to evaluate the package status
            package (str):  id of package 
        
        Space Complexity: O(n)

        Time Complexity: O(n^2*m*j)
        
        """
        
       
        self._deliver_packages()
        asked_time = parse_time(time)
        
        print(
            ("\n\t================================================="
            f" WGUPS Status of All Packages at {time} "
            "======================================================"))
        
        for i in sorted(self._packages, key=lambda x : int(x[0])):
            package, v = i[0], i[1]
            self._evaluate_package_time(asked_time, package)
        self._evaluated.appendleft(self._title)
        print_list(self._evaluated)
       

    def _evaluate_package_time(self, asked_time, package):
        """Takes the asked time and gives the status of the package at that time
        and appends the the package status to the evaluated list.

        Args:
            asked_time (str): time of when to evaluate the package status
            package (str):  id of package 
        
        Space Complexity: O(1)

        Time Complexity: O(1)
        
        """
        
        
        if asked_time >= self._packages[package].delivered_time:
            self._evaluated.append(
                [
                    f"\t{self._packages[package].id}",
                    f'{self._packages[package].weight} lb. ',
                    self._packages[package].full_address(),
                    self._packages[package].truck,
                    self._packages[package].deadline,
                    f'Delivered {self._packages[package].on_time} at {self._packages[package].formatted_delivered_time()}'
                    ])
        elif self._packages[package].on_truck_time < asked_time < self._packages[package].delivered_time:
            self._evaluated.append(
                [
                    f"\t{self._packages[package].id}",
                    f'{self._packages[package].weight} lb. ',
                    self._packages[package].full_address(),
                    self._packages[package].truck, self._packages[package].deadline,
                    f'Out for Delivery on {self._packages[package].truck}'
                    ])
       
        elif asked_time < self._packages[package].on_truck_time:
            if self._packages[package].comment == 'Delayed on flight---will not arrive to depot until 9:05 am':
                self._evaluated.append(
                    [
                        f"\t{self._packages[package].id}",
                        f'{self._packages[package].weight} lb. ',
                        self._packages[package].full_address(),
                        self._packages[package].truck,
                        self._packages[package].deadline,
                        'En route to WGUPS Hub'])
            else:
                self._evaluated.append(
                    [
                        f"\t{self._packages[package].id}",
                        f'{self._packages[package].weight} lb. ',
                        self._packages[package].full_address(),
                        self._packages[package].truck,
                        self._packages[package].deadline,
                        'At WGUPS Hub'])
        


def print_list(sorted_list):
    """Prints a report giving the status of all package at a certain time

    Args:
        sorted_list (deque): List of elements to create the final report
        
    
    Space Complexity: O(n)

    Time Complexity: O(n^2)
    
    """

    formatter = []
    for col in zip(*sorted_list):
        formatter.append(max([len(v) for v in col]))
    format = "  ".join(["{:<" + str(l) + "}" for l in formatter])
    for row in sorted_list:
        print(format.format(*row))
        
def parse_time(time):
    """Evalutes the time given by the user

    Args:
        time (str): time given by user
       
    
    Space Complexity: O(1)

    Time Complexity: O(1)

    Returns:
        DateTime: DateTime of user entered time
    
    """

    if not re.match("(\d\d|\d):\d\d", time):
        print("Time was not formatted correctly! Please enter the time in 24 hour format. ex. 1:00 PM = 13:00")
        sys.exit(2)
    
    split_time = time.split(":")
    
    h, m = int(split_time[0]), int(split_time[1])
    if not 0 <= h <= 23  or not 0 <= m <= 59:
        print("The time entered is not valid, please enter a valid time in 24 hour time format. ex. 1:00 PM = 13:00")
        sys.exit(2)

    asked_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=h, minute=m, second=0))

    return asked_time

