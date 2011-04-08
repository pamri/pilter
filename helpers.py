import re
import datetime

def contains(s1, s2 ):
    """Check if s2 is present in s1"""
    if s1.lower().__contains__(s2.lower()):
        return True
    else:
        return False

def line_match(body_s, strings):
    """If the strings are in any line of the body, then print the matching
    line. Function can take  a single string or a list of strings.
    Use strings if you are using any of the string functions to process further.
    Use list if you want to match multiple lines without further processing. 

        """

    temp_l = []
    if contains(str(type(strings)), 'list'):
        for each_line in body_s.splitlines():
            for each_string in strings:
                if contains(each_line, each_string):
                    temp_l.append(each_line)
        return temp_l
    elif contains(str(type(strings)), 'str'):
        for each_line in body_s.splitlines():
            if contains(each_line, strings):
                return each_line

def alert(instance,text):
    """Print subject with timestamp from the mail"""
    print "%s on" % text, instance.date_d

def c_date(date_s):
    return datetime.datetime.strptime(date_s.split('-')[0].split('+')[0],
    "%a, %d %b %Y %H:%M:%S ")

def c_date_ssl(date_s):
    return datetime.datetime.strptime(date_s,"%b %d %Y %H:%M%p")

def html_to_text(body_s):
    """Simple regex to strip html tags."""
    body_c = ""
    for each_line in body_s.splitlines():
        l = re.sub("<[^<]*?>", "", each_line)
        if l != "" and l != "\n":
            l = l + "\n"
        body_c = body_c + l
    return body_c
