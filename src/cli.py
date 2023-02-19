# -*- coding: utf-8 -*-
"""
This file contains the main procedure to execute the requested CLI flow in the Python UE project.
@author KESKES Nazim
@version 1.0.0
@since December 12th, 2022
"""

# Initialization

from Convert_ICS import Convert_ICS
from Convert_VCF import Convert_VCF
from pathlib import Path
import sys

# Used functions

def list_my_files(path):
    """
    Function to display the list of all vcf or ics files in the directory (path).
    """
    exts = ['.vcf', '.ics']
    for file in Path(path).glob('**/*'):
        if file.suffix in exts:
            print(file)


def convert_ics_csv(file, save_file):
    """
    Function to convert an input ics file to an output csv file.
    """
    # Create and initialize a Convert_ICS object
    if save_file == '':
        save_file = file.split('.')[0] + '.csv'
    convert = Convert_ICS()

    # Read the file file.ics
    convert.read_ical(file)

    # Generate the list of events
    convert.make_data()
    # Save the list as a csv file
    convert.save_csv(save_file)


def afficher_ics(file):
    """
    Function to display the formatted content of an ics file.
    """
    # Create and initialize a Convert_ICS object
    convert = Convert_ICS()

    # Read the file file.ics
    convert.read_ical(file)
    # Generate the list of events
    convert.make_data()
    # For each event in the list, display its necessary fields
    for i, elt in enumerate(convert.data):
        print(f"\n*************** Event {i + 1}  ***************")
        print('SUMMURY : ' + elt[0])
        print('DTSTART : ' + elt[1])
        print('DTEND: ' + elt[2])
        print('DTSTAMP: ' + elt[3])
        print('DESCRIPTION : ' + elt[4])
        print('LOCATION : ' + elt[5])
        print('UID : ' + elt[6])
        print('STATUS : ' + elt[7])
        print('TRANSP : ' + elt[8])

    convert.save_cal()



def convert_ics_html(file, save_file):
    """
    Function that converts an input .ics file into an HTML fragment
    """
    # Create and initialize a Convert_ICS object
    if save_file == '':
        save_file = file.split('.')[0] + '.html'
    convert = Convert_ICS()

    # Read the file file.ics
    convert.read_ical(file)
    # Generate a list of events
    convert.make_data()
    # Save the list as an HTML file
    convert.save_html(save_file)


def convert_vcf_csv(file, save_file):
    """
    Function that converts an input .vcf file into a CSV file
    """
    # Create and initialize a Convert_VCF object
    convert = Convert_VCF()
    # Read the file file.vcf and generate a dictionary for each vCard information
    convert.read_vcf(file)
    if save_file == '':
        save_file = file.split('.')[0] + '.csv'
    # Save the dictionary as a CSV file
    convert.save_csv(save_file)


def afficher_vcf(file):
    """
    Function that displays the contents of a .vcf file in a formatted way
    """
    # Create and initialize a Convert_VCF object
    convert = Convert_VCF()
    # Read the file file.vcf and generate a dictionary for each vCard information
    convert.read_vcf(file)
    # Display the necessary fields of a vCard
    print("\n************** VCard ****************")
    for element in ['N', 'FN', 'ORG', 'TITLE', 'EMAIL', 'TEL WORK', 'TEL HOME', 'TEL CELL', 'ADR WORK', 'ADR HOME',
                    'NOTE', 'URL']:
        print(f'{element} : {convert.data[element]}')


def convert_vcf_html(file, save_file):
    """
    Function that converts an input .vcf file into an HTML fragment
    """
    # Create and initialize a Convert_VCF object
    if save_file == '':
        save_file = file.split('.')[0] + '.html'
    convert = Convert_VCF()

    # Read the file file.vcf and generate a dictionary for each vCard information
    convert.read_vcf(file)
    # Save the dictionary as an HTML fragment
    convert.save_html(save_file)


def cli() -> None:
    """
    Function that allows the execution of the requested process in the CLI part of the Python project.
    The objective of the project is to create an application to manipulate virtual business cards and calendar events.
    """

    # read the command line arguments into a list
    command_line = sys.argv[1:]
    # if no argument is displayed, ask to get help
    if len(command_line) == 0:
        print("Type '-h' (or '--help') to get help.")
    # if the argument is '-h', display the possible modes of use
    elif command_line[0] == "-h":
        print("\nHere are the possible modes of use (or options) you can use: \n")
        print("'-h': Display the modes of use")
        print("'-d directory_path': Display the list of all vcf or ics files starting from the specified directory (directory_path)")
        print("'-i file': Display the formatted content of the ics or vcf file")
        print("'-i file -h save_file.html': Generate the 'save_file.html' file that represents the HTML fragment of the input vcf or ics file")
        print("'-i file -c save_file.csv': Generate the 'save_file.csv' file that represents the CSV workbook of the input vcf or ics file")
    # if the argument is '-d', display the vcf or ics files in the given directory
    elif command_line[0] == "-d":
        # if directory is not specified
        if len(command_line) == 1:
            print("\nError, directory not specified. You must provide a valid directory as a parameter.\nThe correct syntax of the command is: '-d directory_path'")
        else:
            list_my_files(command_line[1])
    # if the argument is '-i'
    elif command_line[0] == "-i":
        # if the input file is an ics file
        if command_line[1].split('.')[1] == "ics":
            # if no other argument is specified, we display the formatted ics file
            if len(command_line) == 2:
                display_ics(command_line[1])
            # if the argument is '-h'
            elif command_line[2] == '-h':
                # if the save file name is not specified, we take the input file name
                if len(command_line) == 3:
                    convert_ics_html(command_line[1],'')
                else:
                    convert_ics_html(command_line[1], command_line[3])
            # if the argument is '-c'
            elif command_line[2] == '-c':
                # if the save file name is not specified, we take the input file name
                if len(command_line) == 3:
                    convert_ics_csv(command_line[1], '')
                else:
                    convert_ics_csv(command_line[1], command_line[3])
            else:
                # if the command is invalid
                print("\nError, the command is invalid.\nType '-h' (or '--help') to get help.")
        # if the input file is a vcf file
        elif command_line[1].split('.')[1] == "vcf":
            # if no other argument is specified, we display the formatted vcf file
            if len(command_line) == 2:
                display_vcf(command_line[1])
            # if the argument is '-h'
            elif command_line[2] == '-h':
                # if the save file name is not specified, we take the input file name
                if len(command_line) == 3:
                    convert_vcf_html(command_line[1],'')
                else:
                    convert_vcf_html(command_line[1], command_line[3])
            # if the argument is '-c'
            elif command_line[2] == '-c':
                # if the save file name is not specified, we take the input file name
                if len(command_line) == 3:
                    convert_vcf_csv(command_line[1], '')
                else:
                    convert_vcf_csv(command_line[1], command_line[3])
            else:
                # if the command is invalid
                print("\nError, the command is invalid.\nType '-h' (or '--help') to get help.")
    else:
        # if the command is invalid
        print("\nError, the command is invalid.\nType '-h' (or '--help') to get help.")




if __name__ == "__main__":
    cli()
