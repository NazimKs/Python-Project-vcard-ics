# -*- coding: utf-8 -*-
"""
This file contains the main procedure to execute the requested GUI part of the Python UE project.
@author KESKES Nazim
@version 1.0.0
@since 12 December 2022
"""

# initialization

from tkinter import *
from tkinter import filedialog
import os
from Convert_ICS import Convert_ICS
from Convert_VCF import Convert_VCF


# functions used

def openFile(entry_path, frame3, info_label, buttonCSV, buttonHTML):
    """
    Function to open a dialog window to list all the ics or vcf files in the Current directory,
    and select a file to display it
    """
    # open a dialog window
    filepath = filedialog.askopenfilename(initialdir=entry_path.get().replace("/", "\\"),
                                          title="Open file",
                                          filetypes=(("vcf files", "*.vcf"),
                                                     ("ics files", "*.ics"),
                                                     ("all files", ["*.vcf", "*.ics"])))
    # if a file is selected
    if filepath:
        # enable the button to generate a CSV file
        buttonCSV["state"] = "normal"
        # enable the button to generate an HTML fragment
        buttonHTML["state"] = "normal"
        info_label.set("Here is the information of your file: ")
        # update the path
        entry_path.set(filepath)
        if filepath.split('.')[1] == "vcf":
            # if the selected file is vCard, display it in formatted form
            display_vcf(filepath, frame3)
        elif filepath.split('.')[1] == "ics":
            # if the selected file is ICS, display it in formatted form
            display_ics(filepath,frame3)
    else:
        info_label.set("You need to select a file to display it, click on Open ")

def display_ics(file, frame):
    """
    Function to display an ICS file in formatted form after selecting it
    """

    # Create and initialize a Convert_ICS object
    convert = Convert_ICS()
    # read the file file.ics
    convert.read_ical(file)
    # generate the list of events
    convert.make_data()
    # remove all previous labels
    for label in frame.grid_slaves():
        label.grid_remove()
    # create labels where each label represents an attribute of an event
    labelSUMMURY = Label(frame, text="Summury : ", bg="ivory", pady=5, padx=5, anchor='w', font=("Poppins", 9, 'bold'))
    labelDTSTART = Label(frame, text="Start Date : ", bg="ivory", pady=5, padx=5, anchor='w',
                     font=("Poppins", 9, 'bold'))
    labelDTEND = Label(frame, text="End Date : ", bg="ivory", pady=5, padx=5, anchor='w',
                       font=("Poppins", 9, 'bold'))
    labelDTSTAMP = Label(frame, text="Modif Date : ", bg="ivory", pady=5, padx=5, anchor='w', font=("Poppins", 9, 'bold'))
    labelDESCRIPTION = Label(frame, text="Description : ", bg="ivory", pady=5, padx=5, anchor='w',
                         font=("Poppins", 9, 'bold'))
    labelLOCATION = Label(frame, text="Location : ", bg="ivory", pady=5, padx=5, anchor='w',
                         font=("Poppins", 9, 'bold'))
    labelSTATUS = Label(frame, text="Status : ", bg="ivory", pady=5, padx=5, anchor='w',
                         font=("Poppins", 9, 'bold'))
    # Fill labels with the value of each attribute of an event
    entrySUMMURY = Label(frame, bg="ivory", text=convert.data[0][0], anchor='w',justify=LEFT)
    entryDTSTART = Label(frame, bg="ivory", text=convert.data[0][1], anchor='w',justify=LEFT)
    entryDTEND = Label(frame, bg="ivory", text=convert.data[0][2], anchor='w',justify=LEFT)
    entryDTSTAMP = Label(frame, bg="ivory", text=convert.data[0][3], anchor='w',justify=LEFT)
    entryDESCRIPTION = Label(frame, bg="ivory", text=convert.data[0][4], anchor='w',justify=LEFT)
    entryLOCATION = Label(frame, bg="ivory", text=convert.data[0][5], anchor='w',justify=LEFT)
    entrySTATUS = Label(frame, bg="ivory", text=convert.data[0][7], anchor='w',justify=LEFT)
    # Place all labels in a global Grid
    labelSUMMURY.grid(row=0,sticky=NW)
    labelDTSTART.grid(row=1, sticky=NW)
    labelDTEND.grid(row=2,sticky=NW)
    labelDTSTAMP.grid(row=3,sticky=NW)
    labelDESCRIPTION.grid(row=4,sticky=NW)
    labelLOCATION.grid(row=5,sticky=NW)
    labelSTATUS.grid(row=6,sticky=NW)
    entrySUMMURY.grid(row=0, column=1,sticky=W)
    entryDTSTART.grid(row=1, column=1,sticky=W)
    entryDTEND.grid(row=2, column=1,sticky=W)
    entryDTSTAMP.grid(row=3, column=1,sticky=W)
    entryDESCRIPTION.grid(row=4, column=1,sticky=W)
    entryLOCATION.grid(row=5, column=1,sticky=W)
    entrySTATUS.grid(row=6, column=1,sticky=W)

def save_ics_csv(entry_path):
    """
    Function to convert an input iCalendar file to an output CSV file
    """
    # Create and initialize a Convert_ICS object
    convert = Convert_ICS()
    # Read the input file at entry_path
    file = entry_path.get()
    convert.read_ical(file)
    # Generate the list of events
    convert.make_data()
    save_file = file.split('.')[0] + '.csv'
    # Save the list as a CSV file
    convert.save_csv(save_file)

def save_ics_html(entry_path):
    """
    Function to convert an input iCalendar file to an output HTML fragment
    """
    # Create and initialize a Convert_ICS object
    convert = Convert_ICS()
    # Read the input file at entry_path
    file = entry_path.get()
    convert.read_ical(file)
    # Generate the list of events
    convert.make_data()
    save_file = file.split('.')[0] + '.html'
    # Save the list as an HTML file
    convert.save_html(save_file)


def display_vcf(file, frame):
    """
    Function to display a vcf file formatted after selecting it
    """

    # Create and initialize a Convert_VCF object
    convert = Convert_VCF()

    # Read the file file.vcf
    convert.read_vcf(file)

    # Remove all previous labels
    for label in frame.grid_slaves():
        label.grid_remove()

    # Create labels where each label represents an attribute of a vCard
    labelFN = Label(frame, text="Name: ", bg="ivory", pady=5, padx=5, anchor='w', font=("Poppins", 9, 'bold'))
    labelORG = Label(frame, text="Organization: ", bg="ivory", pady=5, padx=5, anchor='w',
                     font=("Poppins", 9, 'bold'))
    labelTITLE = Label(frame, text="Position: ", bg="ivory", pady=5, padx=5, anchor='w',
                       font=("Poppins", 9, 'bold'))
    labelEMAIL = Label(frame, text="Email: ", bg="ivory", pady=5, padx=5, anchor='w', font=("Poppins", 9, 'bold'))
    labelTELWORK = Label(frame, text="TEL WORK: ", bg="ivory", pady=5, padx=5, anchor='w',
                         font=("Poppins", 9, 'bold'))
    labelTELHOME = Label(frame, text="TEL HOME: ", bg="ivory", pady=5, padx=5, anchor='w',
                         font=("Poppins", 9, 'bold'))
    labelTELCELL = Label(frame, text="TEL CELL: ", bg="ivory", pady=5, padx=5, anchor='w',
                         font=("Poppins", 9, 'bold'))
    labelADRWORK = Label(frame, text="Address WORK: ", bg="ivory", pady=5, padx=5, anchor='w',
                         font=("Poppins", 9, 'bold'))
    labelADRHOME = Label(frame, text="Address HOME: ", bg="ivory", pady=5, padx=5, anchor='w',
                         font=("Poppins", 9, 'bold'))
    labelNOTE = Label(frame, text="Note: ", bg="ivory", pady=5, padx=5, anchor='w', font=("Poppins", 9, 'bold'))
    labelURL = Label(frame, text="URL: ", bg="ivory", pady=5, padx=5, anchor='w', font=("Poppins", 9, 'bold'))

    # Fill the labels with the value of each attribute of a vCard
    entryFN = Label(frame, bg="ivory", text=convert.data["FN"], anchor='w',justify=LEFT)
    entryORG = Label(frame, bg="ivory", text=convert.data["ORG"], anchor='w',justify=LEFT)
    entryTITRE = Label(frame, bg="ivory", text=convert.data["TITLE"], anchor='w',justify=LEFT)
    entryEMAIL = Label(frame, bg="ivory", text=convert.data["EMAIL"], anchor='w',justify=LEFT)
    entryTELWORK = Label(frame, bg="ivory", text=convert.data["TEL WORK"], anchor='w',justify=LEFT)
    entryTELHOME = Label(frame, bg="ivory", text=convert.data["TEL HOME"], anchor='w',justify=LEFT)
    entryTELCELL = Label(frame, bg="ivory", text=convert.data["TEL CELL"], anchor='w',justify=LEFT)
    entryADRWORK = Label(frame, bg="ivory", text=convert.data["ADR WORK"], anchor='w',justify=LEFT)
    entryADRHOME = Label(frame, bg="ivory", text=convert.data["ADR HOME"], anchor='w',justify=LEFT)
    entryNOTE = Label(frame, bg="ivory", text=convert.data["NOTE"], anchor='w', wraplength=600,justify=LEFT)
    entryURL = Label(frame, bg="ivory", text=convert.data["URL"], anchor='w')
    # Place all labels in a global grid
    labelFN.grid(row=0,sticky=NW)
    labelORG.grid(row=1, sticky=NW)
    labelTITLE.grid(row=2,sticky=NW)
    labelEMAIL.grid(row=3,sticky=NW)
    labelTELWORK.grid(row=4,sticky=NW)
    labelTELHOME.grid(row=5,sticky=NW)
    labelTELCELL.grid(row=6,sticky=NW)
    labelADRWORK.grid(row=7,sticky=NW)
    labelADRHOME.grid(row=8,sticky=NW)
    labelNOTE.grid(row=9,sticky=NW)
    labelURL.grid(row=10,sticky=NW)
    entryFN.grid(row=0, column=1,sticky=W)
    entryORG.grid(row=1, column=1,sticky=W)
    entryTITRE.grid(row=2, column=1,sticky=W)
    entryEMAIL.grid(row=3, column=1,sticky=W)
    entryTELWORK.grid(row=4, column=1,sticky=W)
    entryTELHOME.grid(row=5, column=1,sticky=W)
    entryTELCELL.grid(row=6, column=1,sticky=W)
    entryADRWORK.grid(row=7, column=1,sticky=W)
    entryADRHOME.grid(row=8, column=1,sticky=W)
    entryNOTE.grid(row=9, column=1,sticky=W)
    entryURL.grid(row=10, column=1,sticky=W)


def save_vcf_csv(entry_path):
    """
    Function that converts an input VCF file to an output CSV file
    """
    # Create and initialize a Convert_VCF object
    convert = Convert_VCF()
    # Read the file file.vcf
    file = entry_path.get()
    # Read the file file.vcf and generate a dictionary for each vCard information
    convert.read_vcf(entry_path.get())
    save_file = file.split('.')[0] + '.csv'
    # Save the dictionary as a CSV file
    convert.save_csv(save_file)

def save_vcf_html(entry_path):
    """
    Function that converts an input VCF file to an output HTML fragment
    """
    # Create and initialize a Convert_VCF object
    convert = Convert_VCF()
    # Read the file file.vcf and generate a dictionary for each vCard information
    file = entry_path.get()
    convert.read_vcf(file)
    save_file = file.split('.')[0] + '.html'
    # Save the dictionary as an HTML file
    convert.save_html(save_file)

def save_csv(entry_path):
    """
    Function that converts a selected VCF or ICS file in the dialog window to a CSV file
    """

    if entry_path.get() != os.getcwd().replace('\\', '/'):
        # If the selected file is a VCF file
        if entry_path.get().split('.')[1] == "vcf":
            save_vcf_csv(entry_path)
        # If the selected file is an ICS file
        elif entry_path.get().split('.')[1] == "ics":
            save_ics_csv(entry_path)

def save_html(entry_path):
    """
    Function that converts a selected VCF or ICS file in the dialog window to an HTML fragment
    """
    if entry_path.get() != os.getcwd().replace('\\', '/'):
        # If the selected file is a VCF file
        if entry_path.get().split('.')[1] == "vcf":
            save_vcf_html(entry_path)
        # If the selected file is an ICS file
        elif entry_path.get().split('.')[1] == "ics":
            save_ics_html(entry_path)




def gui() -> None:
    """Function allowing the execution of the process requested in the GUI part of the Python project.
    The objective of the project is to create an application for manipulating virtual business cards (vcf) and digital agenda events (ics)."""

    # Creating the main window
    root = Tk()
    root.title("GUI")

    # Creating the main canvas, specifying its height, width, and background color
    cnv = Canvas(root, width=700, height=700, bg="#FFFAE2")
    cnv.pack()

    # Creating a variable for the current path (or selected file)
    entry_path = StringVar()
    entry_path.set(os.getcwd().replace('\\','/'))

    # Creating a label for the main menu
    MenuLabel = Label(cnv, wraplength=680, pady=20, padx=20, text="Welcome to the GUI for manipulating your virtual business cards (vcf) and digital agenda events (ics).", font=("Poppins", 14, 'bold'), bg="#FFFAE2")
    MenuLabel.pack()

    # Creating a frame for manipulating vcf and ics files
    frame2 = LabelFrame(cnv, height=500, width=680, bg="ivory")
    frame2.pack(fill='both', expand=1, padx=5, pady=10)

    # Creating a label for the current path
    SelectLabel = Label(frame2, text="Select a path to your source directory:", bg="ivory", pady=5, padx=10, anchor='w')
    SelectLabel.pack(fill="both", expand=1)

    # Creating an entry for the current path
    EntryPath = Entry(frame2, bg="ivory", text=entry_path)
    EntryPath.pack(fill="both", expand=1, pady=5, padx=20)

    # Creating a button to open the file dialog
    buttonOpen = Button(frame2, text="Open", command=lambda:openFile(entry_path,frame3,info_label,buttonCSV,buttonHTML), pady=5, width=15)
    buttonOpen.pack()

    # Creating a label to provide usage instructions
    info_label = StringVar()
    info_label.set("You need to select a file to display it. Click Open.")
    InfoLabel = Label(frame2, textvariable=info_label, bg="ivory", pady=5, anchor='w')
    InfoLabel.pack(fill="both", expand=1, padx=10)

    # Creating a label frame to display data from an ics or vcf file
    frame3 = LabelFrame(frame2, height=250, width=680, bg="ivory")
    frame3.pack(fill="both", expand=1, pady=10, padx=10)

    # Creating a label to provide a note
    RemarqueLabel = Label(frame2, text="Note: For ics files, only the first event of the calendar will be displayed", bg="ivory", pady=5, padx=10, anchor='w')
    RemarqueLabel.pack(fill="both", expand=1)

    # Creating a frame for saving a file in CSV format
    CSVFrame = Frame(frame2, bg="ivory")
    CSVFrame.pack(pady=10, fill="both", expand=1)
    # Creating a label
    SauvgardeCSVLabel = Label(CSVFrame, text="To save the file in CSV format:", bg="ivory", pady=5, padx=10, anchor='w', justify=LEFT)
    # Create a button (by default it is disabled)
    buttonCSV = Button(CSVFrame, text="Save CSV", pady=5, width=10, command=lambda: save_csv(entry_path))
    buttonCSV["state"] = "disable"

    # Place a Grid envelope
    SauvgardeCSVLabel.grid(row=0, sticky=W)
    buttonCSV.grid(row=0, column=1, sticky=W)

    # Create a frame for saving a file in HTML format
    HTMLFrame = Frame(frame2, bg="ivory")
    HTMLFrame.pack(pady=10, fill="both", expand=1)

    # Create a label
    SauvgardeHTMLLabel = Label(HTMLFrame,
                              text="To save the file in HTML format: ",
                              bg="ivory", pady=5,
                              padx=10, anchor='w', justify=LEFT)

    # Create a button (by default it is disabled)
    buttonHTML = Button(HTMLFrame, text="Save HTML", pady=5, width=10, command=lambda: save_html(entry_path))
    buttonHTML["state"] = "disable"

    # Place a Grid envelope
    SauvgardeHTMLLabel.grid(row=0, sticky=W)
    buttonHTML.grid(row=0, column=1, sticky=W)

    # Launch the application
    root.mainloop()



if __name__ == "__main__":
    gui()
