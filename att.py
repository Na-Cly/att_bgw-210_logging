"""
Extract loggin info from att bgw210
"""
import requests
from bs4 import BeautifulSoup
import json
class att_logs:
    
    def __init__(self, url):
        self.url = url
        self.dhcp_url = '/cgi-bin/devices.ha'
        self.software_url = '/cgi-bin/sysinfo.ha'
        self.broadband_url = '/cgi-bin/broadbandstatistics.ha'
        self.lan_url = '/cgi-bin/lanstatistics.ha'

    def get_dhcp(self):
        """grabs dhcp info from gateway"""
        #get html data, requires no login.
        table_data = {}
        data = requests.get(self.url + self.dhcp_url)
        html = BeautifulSoup(data.text, 'html.parser') 
        #get the elements from the html
        items = html.find_all('tr')
        #counter used to separate data in the dictionary
        counter = -1
        for item in items:
            split = item.get_text().split('\n')
            if split[0] == 'MAC Address':
                counter += 1
                table_data[counter]={}
            if split[0] != '':
                table_data[counter].update({split[0]:split[1]})
        #conver the dictionary with keys of 1 - x to dictionaries in a list
        table_data = [val for key, val in table_data.items()]
        return json.dumps(table_data)

    def get_software(self):
        """Gets software info from gateway"""
        table_data = {}
        data = requests.get(self.url + self.software_url)
        html = BeautifulSoup(data.text, 'html.parser')
        #get the elements from the html
        items = html.find_all('tr')
        
        #counter used to separate data in the dictionary
        for item in items:
            split = item.get_text().strip().split('\n')
            try:
                split.remove('')
            except:
                pass
            table_data[split[0]] = split[1]
        #return the json
        return json.dumps(table_data)

    def get_broadband(self):
        """Gets broadband information"""
        table_data = {}
        data = requests.get(self.url + self.broadband_url)
        html = BeautifulSoup(data.text, 'html.parser')
        #get the elements from the html 
        items = html.find_all('tr')
        for item in items:
            split = item.get_text().strip().split('\n')
            try:
                split.remove('')
            except:
                pass
            if len(split) > 1:
                table_data[split[0]] = split[1]
            elif len(split) == 1:
                table_data[split[0]] = ''
        #return the json
        return json.dumps(table_data)

    """def get_lan(self):
        """Gets lan information"""
        table_data = {}
        data = requests.get(self.url + self.lan_url)
        html = BeautifulSoup(data.text, 'html.parser')
        #get the elements from the html 
        items = html.find_all('tr')
        for item in items:
            split = item.get_text().split('\n')
            if len(split) > 3:
                
            try:
                split.remove('')
            except:
                pass"""
            print(split)
            """if len(split) > 1:
                table_data[split[0]] = split[1]
            elif len(split) == 1:
                table_data[split[0]] = ''
        #return the json
        return json.dumps(table_data)"""
