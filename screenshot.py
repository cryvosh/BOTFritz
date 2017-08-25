from mss import mss

def grab(region):
    sct = mss()
    return sct.grab(region)