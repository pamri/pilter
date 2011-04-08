#!/usr/bin/python

r"""
This module helps in filtering incoming mail. It uses the FeedParser module
from email to parse each incoming message and puts the data into easily 
accessible data types.

Note on writing filters :
* Filters should be written in filters.py under the run_filter function.
* Filters are written in python
* Use () to enclose the "if" statements for readability
* For readability, do not go beyond the width of 79 columns
* The "contains" function converts both strings to lower case before comparing. 
* Use "line_match" to print out a list of lines that match the string:
** Use list type if you want to match multiple lines without further processing.
** Use str type if you want to process a single line with additional processing.

"""

import sys
from email.feedparser import FeedParser
#import datetime

# import helper functions
import helpers as h
# import and execute filters from filters.py
import filters

class mail:
    """Class to filter mail."""
    def __init__(self):
        """Initialise class"""
        # initiate class for feedparser
        self.raw_stream = FeedParser()

        # variables for parsed mail data
        self.raw_data   = ''
        self.raw_msg    = ''
        self.headers    = {}
        self.body    = ''
        self.sender  = ''
        self.to      = ''
        self.subject = ''
        self.date_s  = ''
        self.date_d  = ''

    def feed(self, r1):
        """Read data before parsing."""
        self.raw_data = ''.join(r1) 

    def parse(self):
        """Parse raw data using FeedParser to extract body and headers."""

        # pass raw data to feedparser instance
        self.raw_stream.feed(self.raw_data)

        # close and create a feedparser instance 
        self.raw_msg = self.raw_stream.close()
        # Mail processing
        # sort raw messages to extract variables
        for each_key in self.raw_msg.keys():
            self.headers[each_key] = self.raw_msg.get(each_key)

        # mail related variables
        # Get payload without parsing if it is not multipart
        if self.raw_msg.is_multipart() == False:
            self.body    = h.html_to_text(self.raw_msg.get_payload())
        # If message is multi-part and has both html/text parts,
        # get only the text message
        elif self.raw_msg.get_content_type() == 'multipart/alternative':
            for part in self.raw_msg.walk():
                if h.contains(part.get_content_type(),'text/plain'):
                    self.body =  part.get_payload(decode=True)
            self.body = h.html_to_text(self.body)
        else:
            # If message is multi-part and encoded with base-64, combine plain 
            # text and html text and strip all html tags
            for part in self.raw_msg.walk():
                if h.contains(part.get_content_type(), 'text'):
                    self.body = self.body + part.get_payload(decode=True)
            self.body = h.html_to_text(self.body)

        # Store data into essential variables
        self.sender  = self.headers['From'].lower()
        self.to      = self.headers['To'].lower()
        self.date_s  = self.headers['Date']
        self.date_d = h.c_date(self.date_s)
        self.subject = self.headers['Subject'].lower()


if __name__ == '__main__':

    # read from file/stdin and pipe to feedparser
    m_instance = mail()
    m_instance.feed(sys.stdin.readlines())
    m_instance.parse()
    filters.run_filter(m_instance)
