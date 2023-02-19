#initialisation

from pathlib import Path
from typing import Any, List, Union
from icalendar import Calendar
import csv

# Class dedicated to the ICS file

class Convert_ICS:
    """
    Class dedicated to reading and processing data from an ICS file.
    """

    def __init__(self) -> None:
        """
        Constructor of the class dedicated to the ICS file.
        """
        # A list of events where each event is also a list
        self.data: List[List[Any]] = []
        # ICS file in the Calendar format
        self.cal: Calendar = None


    def read_ical(self, ical_file_location: Union[str, Path]) -> Calendar:
        """
        Method for reading the ICS file.
        """
        # Read the ICS file
        with open(ical_file_location, 'r', encoding='utf-8') as ical_file:
            data = ical_file.read()
        # Save the Calendar format of the ICS file
        self.cal = Calendar.from_ical(data)
        return self.cal


    def make_data(self) -> None:
        """
        Method for creating a list of events from a file in the Calendar format.
        """
        # For each event, return the necessary information in a list
        for event in self.cal.subcomponents:
            if event.name != 'VEVENT':
                continue
            dtstart = ''
            if event.get('DTSTART'):
                dtstart = event.get('DTSTART').dt
            dtend = ''
            if event.get('DTEND'):
                dtend = event.get('DTEND').dt
            dtstamp = ''
            if event.get('DTSTAMP'):
                dtstamp = event.get('DTSTAMP').dt
            row = [
                event.get('SUMMARY'),
                dtstart,
                dtend,
                dtstamp,
                event.get('DESCRIPTION'),
                event.get('LOCATION'),
                event.get('UID'),
                event.get('STATUS'),
                event.get('TRANSP')
            ]
            row = [str(x) for x in row]
            # Insert the event into a list of events
            self.data.append(row)


    def save_csv(self, csv_location: str) -> None:
        """
        Method for creating and saving our list of events in a CSV file.
        """
        self.data.insert(0, ['SUMMURY', 'DTSTART', 'DTEND', 'DTSTAMP', 'DESCRIPTION', 'LOCATION', 'UID', 'STATUS', 'TRANSP'])
        with open(csv_location, 'w', encoding='utf-8', newline='') as csv_handle:
            writer = csv.writer(csv_handle)
            # For each event, insert it into a line of CSV file
            for row in self.data:
                writer.writerow([r.strip() for r in row])

    # Method for creating and saving our list of events in an HTML fragment
    def save_html(self, vcf_save_location: Union[str, Path]):
        """
        Method for creating and saving our list of events in an HTML fragment
        """
        file_html = open(vcf_save_location, "w")

        # Generate and launch an html file
        file_html.write(f'''
                <html>
                <head>
                <title>{vcf_save_location.split('/')[-1].split('.')[0]}</title>
                </head> 
                <body>
                <h1 class="p-name">{vcf_save_location.split('/')[-1].split('.')[0]} HTML Fragment</h1>
                <hr>
                ''')

        # For each event, fill in the microformat of an event (h-event) in the HTML fragment
        for element in self.data:
            file_html.write(f'''
                    <div class="h-event">
                    <h3 class="p-summary">{element[0]}</h3>
                    <p> From 
                        <time class="dt-start" datetime="2013-06-30T12:00">{element[1].split('+')[0]}</time>
                        to <time class="dt-end" datetime="2013-06-30T18:00">{element[2].split('+')[0]}</time>
                        at <span class="p-location">{element[5]}</span></p>
                    <p class="p-description">DESCRIPTION : {element[4]}</p>
                    <p class="p-location">STATUS : {element[7]}</p>
                    <hr>
                    </div>
                    ''')

        # Close the HTML file
        file_html.write(f'''
                </body>
                </html>
                ''')

    # Method for saving the modified ics file
    def save_cal(self):
        """
        Method for saving the modified ICS file
        """
        res_data = self.cal.to_ical()
        with open("result.ics", 'wb') as ical_file:
            ical_file.write(res_data)
