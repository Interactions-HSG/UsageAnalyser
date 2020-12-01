'''check internet connection'''
import urllib.request


def connect(host='http://google.com'):
    '''check internet connection, return true if the request is successful else false'''
    try:
        urllib.request.urlopen(host) 
        return True
    except:
        return False