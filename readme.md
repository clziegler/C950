

## Problem overview

The Western Governors University Parcel Service (WGUPS) is having a issue with packages not being delivered by their promised deadlines. To alleviate the issue, WGUPS needs to determine the best route and delivery distribution system for their Daily Local Deliveries (DLD). The DLD has 3 trucks, 2 drivers, and average of 40 packages to deliver each day, and each package has specific delivery conditions.

##### Assumptions:

* Each truck can carry a maximum of 16 packages.
* Trucks travel at an average speed of 18 miles per hour.
* Trucks have a “infinite amount of gas” with no need to stop.
* Each driver stays with the same truck as long as that truck is in service.
* Drivers leave the hub at 8:00 a.m., with the truck loaded, and can return to the hub for packages if needed. The day ends when all 40 packages
have been delivered.
* Delivery time is instantaneous, i.e., no time passes while at a delivery (that time is factored into the average speed of the trucks).
* There is up to one special note for each package.
* The wrong delivery address for package #9, Third District Juvenile Court, will be corrected at 10:20 a.m. The correct address is 410 S State St., Salt Lake City, UT 84111.
* The package ID is unique; there are no collisions.
* No further assumptions exist or are allowed.


## WGUPS Main Application
#### INTERFACE

The WGUPS Application utilizes a simple __command-line interface__. To run the program, in a terminal window navigate to the folder `c_ziegler_c950` and type `python wgups`.

This will print the help menu of the program, which for convenience is also included here:
    
    usage: wgups [-h] [-f] [-t time] [-p id]

    ===========================================================================================================
    Charles Ziegler's Final Project for Western Governors University C950 -Data Structures and Algorithms II-
    ===========================================================================================================

    optional arguments:
    -h, --help            show this help message and exit
    -f, --final           Print the Final Report Showing the Final Result of All Packages, and the Total Milage Traveled
    -t time, --time time  Print the Status of All Packages at a Given Time (24 hour time in this format= HH:MM)
    -p id, --package id   Enter the Package ID after entering the time to see the status of that particular package at the givien time


            Examples:
                To see final report: wgups -f
                To see the status of all packages at  10:00: wgups -t 10:00
                To see the status of Package ID 1 at 8:30: wgups -t 8:30 -p 1



---

#### Screen Shots of Package Status at Certain Times, and Final Status of the Packages and Total Miles Traveled. 
##### Screen shots also show the program execution
__Final Status of all packages, Total Miles Traveled, and Total Packages Delivered__
![Final Report](files/images/final.png)
__Status of All Packages at 8:45__
![Packages at 8:45](files/images/845.png)
__Status of All Packages at 9:45__
![Packages at 9:45](files/images/945.png)
__Status of All Packages at 12:45__
![Packages at 12:45](files/images/1245.png)

---
