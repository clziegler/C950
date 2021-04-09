import datetime

class Package:
    """A class representing a package
    
    Parameters:
    
        id (int): The package identifier
        address (str):
            The destination street for the package destination
        city (str):
            The city for the package destination
        state (str):
            The state for the package destination
        zip (str)
            :The zip code for the package destination
        deadline (str):
            The package delivery deadline
        weight (int):
            The package weight
        comment(str):
            The package delivery notes
        status (str)
            The starting position of the package, (default 'Hub')
        truck (str):
            The name of the delivery truck that delivered the package
        on_truck_time (DateTime):
            The time that the package is loaded onto a delivery truck
        delivered_time (DateTime):
            The time that the package was delivered to the destination
        on_time (str):
            the status of the package delivery 
        
    """

    def __init__(self, id, address, city, state, zip, deadline, weight, comment="", status="Hub"):
      
       
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        self.comment = comment
        self.status = status
        self.truck = None
        self.on_truck_time = None
        self.delivered_time = None
        self.on_time = None


    def full_address(self):
        """ Returns the address, city, state, and zipcode to a full address"""

        return f'{self.address} {self.city} {self.state}, {self.zip}'

    
    def formatted_delivered_time(self):
        """ Returns a full DateTime object and formats it to HH:MM format"""
  
        formatted = datetime.datetime.strftime(self.delivered_time, "%H:%M")
        return formatted
