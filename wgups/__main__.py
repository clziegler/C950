#!/usr/bin/env python -u
# encoding: utf-8
"Charles Ziegler Student ID: 000622857"

import wgups
import parser

def main():
    "main"
  
    main_program = wgups.Wgups()
    args = parser.argparser()
   
    if args.final:
        main_program.final_report()
    elif args.time and args.package:
        main_program.get_time_package(args.time, args.package)
    elif args.time:
        main_program.get_time_all(args.time)
    

if __name__ == '__main__':
    main()
