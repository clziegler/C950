#!/usr/bin/env python -u
# encoding: utf-8
"""Parses User Input"""

import argparse
import sys
import textwrap

class Parser(argparse.ArgumentParser):
    """"Subclass of the ArgumentParser error method to print the argparse help
    
    """
    def error(self, message):
        sys.stderr.write(f'error: {message}\n' )
        self.print_help()
        sys.exit(2)

def argparser():
    """"argparser for the WGUPS program"""
    
    parser = Parser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''
        ===========================================================================================================
        Charles Ziegler\'s Final Project for Western Governors University C950 -Data Structures and Algorithms II-
        ===========================================================================================================
        '''),
        epilog=""" 
        Examples:
            To see final repport: wgups -f
            To see the status of all packages at 10:00: wgups -t 10:00
            To see the status of Package ID 1 at 8:30: wgups -t 8:30 -p 1
            """)

    parser.add_argument(
        "-f", "--final", 
    help="Print the Final Report Showing the Final Result of All Packages, and the Total Milage Traveled",
                    action="store_true")
    parser.add_argument(
        "-t", "--time", 
        help="Print the Status of All Packages at a Given Time  (24 hour time in this format= HH:MM)",
                    action="store", type=str, metavar=('time'))
    parser.add_argument(
        "-p", "--package", 
        help="Enter the Package ID after entering the time to see the status of that particular package at the given time",
                    action="store", type=str, metavar=('id'))

    if len(sys.argv)==1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    return parser.parse_args()

