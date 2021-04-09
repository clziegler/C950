#!/usr/bin/env python -u
# encoding: utf-8

import datetime
import data_table
import dispatch

class Truck:
    """The representation of a delivery truck

    Parameters
    ----------
        name :str 
            name of the truck
        distances : hashmap 
            hashmap of the parsed distance csv table
        addressses: hashmap 
            hashmap of the parsed address csv table
        packages : hashmap 
            hashmap of the packaged csv table
        start_time : list
            list with 2 integers, hour and minutes

    Attributes
    ----------
        trip_count : int
            The times the truck has left the hub
        packages_delivered ; int
            THe total amount of packages delivered by the truck
        payload : list
            The data structure that holds the packages on the truck
        hub : str
            the address of the WGUPS Hub
        current_loc : str
            The address of where the truck is at a given delivery (default 'Hub')
        distance_to_hub : float
            the distance between the trucks current location and the WGUPS Hub
    Methods
    -------
        final_report_list():
            returns the list to generate the final report
        formatted_delivered_time():
            returns the formated time sting from a datetime object
        get_current_location():
            returns the current address of the truck
        get_time():
            returns the current datetime of truck
        get_miles():
            return the current milage of the truck
        drive(destination):
            drives from the current location to the destinattion
        return_to_hub():
            drives from the current location to the WGUPS Hub
        get_distance_to_hub():
            returns the distance to the WGUPS Hub
        load_and_deliver_packages(planned_packages, packages):
            loads the truck and delivers the packages
          
    """

    def __init__(self, name, distances, addresses, start_time=[8,0]):
        self.name = name
        self.distances = distances
        self.addresses = addresses
        self._max = 16
        self._mph = 18.0
        self._odm = 0.0
        self.packages_delivered = 0
        self.payload = []
        self.start_hour, self.start_minute = start_time 
        self._time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=self.start_hour, minute=self.start_minute, second=0))
        self.hub = "4001 South 700 East"
        self.current_loc = self.hub
        self.distance_to_hub = None
    
    def __add__(self, other):
        """Adds the truck objects milage with another truck's milage
        
        Space Complexity: O(1)

        Time Complexity: O(1)
        
        """
        total_miles = round(self.get_miles() , 1) + round(other.get_miles(), 1)

        return total_miles
    
    def __repr__(self):
        """Returns a string representation of the truck"""
        return f"{self.name} Milage: {round(self._odm, 2)}\t Time of Last Delivery: {self._time}  \tPackages delivered: {self.packages_delivered}"

    def final_report_list(self):
        """ Create the list needed for the program final report

        Returns: 
            list: List containing the parameters needed to generate the program final report
        
        """
        return [f"\t{self.name}", str(round(self.get_miles(),2)), self.formatted_delivered_time(), str(self.packages_delivered)]
    
    def formatted_delivered_time(self):
        """ Takes the DateTIme truck time object and formats them to HH:DD


        Returns: 
            str: HH:DD representation of the truck DateTime 
        
        """
        
        formatted = datetime.datetime.strftime(self._time, "%H:%M")
        return formatted


    def get_current_location(self):
        """Returns the truck's current address"""
        return self.current_loc

    def get_time(self):
        """Returns the truck's current time"""
        return self._time
    
    def get_name(self):
        """Returns the truck's name"""
        return self.name

    
    def get_miles(self):
        """Returns the truck's current milage"""
        return self._odm
        

    def drive(self, destination):
        """Moves truck object from current location to new destination, updates milage, truck time
         and location

        Args:
            destination (str): address of the next destination
        
        Space Complexity: O(1)

        Time Complexity: O(1)
        
        """
        new_distance = data_table.get_distance_addresses(self.current_loc, destination, self.distances, self.addresses)
        self._odm += float(new_distance)
        self.current_loc = destination

        def _travel_time(new_distance):
            """Calculates the time needed to travel to a new location

            Args:
                 new_distance (float): the distance in miles 
            
            Space Complexity: O(1)

            Time Complexity: O(1)
            """
        
            hour = int(new_distance / self._mph)
            minute = (((new_distance / self._mph)*60) % 60)
            self._time +=  datetime.timedelta(hours=hour, minutes=minute)

        _travel_time(new_distance)

    
    def return_to_hub(self):
        """Moves truck from current location to the WGUPS Hub
            
            Space Complexity: O(1)

            Time Complexity: O(1)
            
            """
        self.drive(self.hub)
    
    def get_distance_to_hub(self):
        """Calculates the distance from the trucks current location and the WGUPS Hub
            
        Space Complexity: O(1)

        Time Complexity: O(1)
        
        """
        new_distance =  data_table.get_distance_addresses(self.current_loc, self.hub, self.distances, self.addresses)
        self.distance_to_hub = new_distance
        return self.distance_to_hub


    def load_and_deliver_packages(self, planned_packages, packages):
        """Loads the truck and delivers the packages

        Args:
            planned_packages (hashtable.Hashmap): Hashmap of planned_packages of each truck, as well as the 
                "Any" group
            packages (hashtable.Hashmap): Hashmap containing package objects
        
        Space Complexity: O(1)

        Time Complexity: O(n*m*j)
        
        returns:
            callable: _deliver_package(packages, planned_packages)
        
        """ 
        
        packages_count = 0
        
        #Keep filling the truck until the truck can no longer hold anymore packages
        while packages_count < self._max:
            
            #If the truck priority hashmap is empty fill the truck hashmap with packages from the "Any" Hashmap
            if planned_packages["Any"] and len(planned_packages[self.name]) == 0 :
                    popped = planned_packages["Any"].pop(0)
                    planned_packages[self.name].append(popped)
            
            #Loop through the package list of the trucks hashmap, and add a list containing the address and list of package ids       
            for package_bundle in planned_packages[self.name]:
                address, package_id_list = package_bundle[0], package_bundle[1]
                self.payload.append([address, package_id_list])
                
                #Change the package on truck time to the trucks current time, and increment the package count
                for package in package_id_list:
                    packages[package].on_truck_time = self.get_time()
                    packages_count += 1
                #Remove the package group from the truck hashmap
                planned_packages[self.name].remove(package_bundle)
                
                #If the payload is full, deliver the packages
                if len(self.payload) == self._max:
                    return self._deliver_package(packages)
                
                #If the payload + the current package count would go over the payload, deliver the packages
                if len(package_id_list) + packages_count >= self._max:
                    return self._deliver_package(packages)
            
            #If there are no more packages in the planned packages hashmap, deliver the packages
            if len(planned_packages[self.name]) == 0 and len(planned_packages["Any"]) == 0: 
                return self._deliver_package(packages)
        
        self._deliver_package(packages)
            
    
    def _find_nearest(self, payload):
        """Finds the nearest address of the packages group in the truck payload 
        
        Space Complexity: O(n)

        Time Complexity: O(n)

        Returns: 
            tuple: package group tuple
        """
        
        
        short_list= {}
        #Loop through the package groups in the payload, add the distance from the current location as the 
        #dictionary key amd the package group as the value
        for i in payload:
            address = i[0]
            distance = data_table.get_distance_addresses(self.current_loc, address, self.distances, self.addresses)
            short_list[distance] =  i

        #Find the smallest key in the short_list dictionary, which indicates closest package group to the truck's 
        # current location 
        smallest = min(short_list)
        #Return the package list that is closest to the trucks current location
        return short_list.get(smallest)

    
    def _deliver_package(self, packages):
        """This delivers the packages

        Args:
            packages (hashtable.HashTable): The HashTable containing the package objects .
        

        Space Complexity: O(n)

        Time Complexity: O(n^2)
            

        Returns:
            hash_table.HashTable: hashtable containing the priority dictionaries
        """  
        
        priority, other, hold = dispatch.plan_truckload(self.payload, packages)
        truck_payload = [priority, other]
        wrong_address_time = datetime.datetime.combine(datetime.date.today(), datetime.time(hour=10, minute=20, second=0))
        
        #Reset the gerneral truck payload to 0 so we can refill if needed          
        self.payload = []
        
        #Loop through the priority and other lists
        for group in truck_payload: 
            while len(group) > 0:
                #Find the packages that are closest to the trucks current location
                nearest = self._find_nearest(group)
                
                #move truck to the location
                self.drive(nearest[0])
                
                #Deliver all the packages that should be delivered to the address of the truck's location
                for id in nearest[1]:
                    package = packages[id]
                    if self._check_on_time(package):
                        package.on_time = "On Time"
                    else:
                        package.on_time = "Late"
                    package.delivered_time = self.get_time()
                    package.truck = self.get_name()
                    self.packages_delivered += 1
                
                group.remove(nearest)
                #Check to see if the if it is passed 10:20, if so add the held package to the current group that
                #is being delivered
                if self.get_time() >= wrong_address_time:
                    if len(hold) > 0:
                        group.append(hold.pop(0))
                if len(group) == 0:
                    break
           
        
           
        self.return_to_hub()
        

    def _check_on_time(self, package):
        """Determines if the package was delivered on time 
        
        Space Complexity: O(1)

        Time Complexity: O(1)

        Returns: 
            Bool: True if the package was on time, false if it was not
        """
        
        
        time = package.deadline
        
        if time == "EOD":
            return True

        #The package deadline is in HH:MM p format, the following transforms that to a datetime object so 
        #it can be comapaired with the truck's current time at time of delivery
        given_time = datetime.datetime.strptime(package.deadline, "%H:%M %p")
        formatted_time = given_time.time().strftime("%H:%M:%S")
        time_list = formatted_time.split(':')
        final_time =  datetime.time(hour=int(time_list[0]), minute=int(time_list[1]), second=int(time_list[2]))
        due_time = datetime.datetime.combine(datetime.date.today(), final_time)
        
        if due_time < self._time:
            return False

        return True




    
    
