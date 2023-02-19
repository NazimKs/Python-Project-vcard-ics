# initialization
from pathlib import Path
import pandas as pd
from typing import Any, Union

# Class dedicated to the ICS file
class Convert_VCF():
    """
    Class dedicated to reading and processing data from a VCF file.
    """
    def __init__(self) -> None:
        """
        Constructor of the class dedicated to the VCF file.
        """
        # A dictionary that contains each information with its necessary field
        self.data: dict[Any, Any] = {}

    def read_vcf(self, vcf_file_location: str) -> dict[Any, Any]:
        """
        Method to read a VCF (Virtual Card) file and return a dictionary that contains the necessary information.
        """
        with open(vcf_file_location, 'r') as f:
            # Filter out "http:" and split all lines of the file into 2 parts (one for the attribute and the other for the information field of the attribute)
            ls = [l.replace('http://', '') for l in f]
            ls = [l.replace('http\\://', '') for l in ls]
            lines = [l.split(':') for l in ls]
            # Create a tuple for each vcard information
            tup_lin = [tuple(li) for li in lines]
            dt = {}
            for d in tup_lin:
                # If the length of the tuple is 2, it is valid.
                if len(d) == 2:
                    # Filter the file to return only the attribute field with its information field
                    dt.update({self.clean_entry(d[0]): self.clean_entry(d[1])})
            # If our dictionary doesn't have information in one of these fields, insert an empty string
            for elt in ['N', 'FN', 'ORG', 'TITLE', 'EMAIL', 'TEL WORK', 'TEL HOME', 'TEL CELL', 'ADR WORK', 'ADR HOME', 'NOTE', 'URL']:
                if elt not in dt.keys():
                    dt[elt] = ''
        # Save the obtained dictionary from the VCF file
        self.data = dt
        return self.data

    def clean_entry(self, field):
        """
        Method to filter the VCF (Virtual Card) file for only the attribute field with its information field and insert it into the data dictionary of the class.
        """
        # Filter the file to return only the attribute field with its information field
        g = field.replace('\n', '')
        g = g.replace(';;', ';')
        g = g.replace(';', ' ')
        g = g.replace('=0D=0A=', ' ')
        g = g.replace('=0D=0A', ' ')
        g = g.replace('http', '')
        g = g.replace('type=', '')
        g = g.replace(' VOICE', '')
        g = g.replace('item1.', '')
        g = g.replace('item2.', '')
        g = g.replace('item3.', '')
        g = g.replace('item4.', '')
        g = g.replace('item5.', '')
        g = g.replace('EMAIL INTERNET WORK pref', 'EMAIL PREF INTERNET')
        g = g.replace('EMAIL PREF INTERNET', 'EMAIL')
        g = g.replace('ADR HOME pref', 'ADR HOME')
        g = g.replace('TEL WORK pref', 'TEL WORK')
        g = g.replace('URL pref', 'URL')
        g = g.replace('\\n', '')
        # Return the filtered file
        return g


    def save_csv(self, vcf_save_location: Union[str, Path]):
        """
        Method to create and save our vCard dictionary in a CSV file
        """
        # Create a pandas series from the vCard dictionary
        db = pd.Series(self.data)
        db = db[['N', 'FN', 'ORG', 'TITLE', 'EMAIL', 'TEL WORK', 'TEL HOME', 'TEL CELL', 'ADR WORK', 'ADR HOME', 'NOTE', 'URL']]
        # Generate a CSV file
        db.to_csv(vcf_save_location, index_label="vCard")

    def save_html(self, vcf_save_location: Union[str, Path]):
        """
        Method to create and save our vCard dictionary in an HTML fragment
        """
        file_html = open(vcf_save_location, "w")

        # Generate and launch an HTML file
        file_html.write(f'''
                <html>
                <head>
                <title>{vcf_save_location.split('/')[-1].split('.')[0]}</title>
                </head> 
                <body>
                <h1 class="p-name">{vcf_save_location.split('/')[-1].split('.')[0]} HTML Fragment</h1>
                <hr>

                ''')
        # Fill the h-card microformat in the HTML fragment with vCard information
        atts = ['N', 'FN', 'ORG', 'TITLE', 'EMAIL', 'TEL WORK', 'TEL HOME', 'TEL CELL', 'ADR WORK', 'ADR HOME', 'NOTE', 'URL']
        file_html.write(f'''
                    <div class="h-card">
                    <p> <span class="p-name" STYLE="font-weight:bold">{self.data['FN']}</span> , <span class="p-title">{self.data['TITLE']}</span> </p>
                    <p class="p-org">Organisation : {self.data['ORG']}</p>
                    <p class="p-email">Email : {self.data['EMAIL']}</p>
                    <p class="p-tel-work">Business Tel : {self.data['TEL WORK']}</p>
                    <p class="p-tel-home">Home Tel : {self.data['TEL HOME']}</p>
                    <p class="p-tel-cell">Cell Tel : {self.data['TEL CELL']}</p>
                    <p class="p-adr-work">Business Address : {self.data['ADR WORK']}</p>
                    <p class="p-adr-home">Home Address : {self.data['ADR HOME']}</p>
                    <p class="p-note">Note : {self.data['NOTE']}</p>
                    <p class="p-url">URL :<a href="{self.data['URL']}"> {self.data['URL']}</a></p>
                    <hr>
                    </div>
                    ''')
        # Close the HTML file
        file_html.write(f'''
                </body>
                </html>
                ''')
