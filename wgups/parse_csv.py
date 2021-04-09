#!/usr/bin/env python -u
# encoding: utf-8

import csv



def parse_csv(filename):
    """This parses a csv file into a list

    Args:
        filename (str): Relative path to the csv file

    Space Complexity: O(n)

    Time Complexity: O(n)
        
    Returns:
       list: List containing csv data
       
    """
    
    csv_list = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            csv_list.append(row)

    return csv_list



