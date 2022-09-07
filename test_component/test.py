#!/usr/bin/env python3
#Imports
from clize import run
import string
import random
import requests
import random


def client(data_points: int):
    """
    Function that sends continous strings to an existing flask application.
    
    data_points : int, number of request that shall be made

    """
    url = "http://127.0.0.1:5000/post" 
    i = 0
    while i < data_points:
        print('Current data_point will be created: {0}'.format(i))
        # create random String length
        n = random.randint(0,100)
        print('Length of String: {0}'.format(n))
        # Create Strings
        string_= "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))
        data = {"data": string_}
        r = requests.post(url, data=data)
        print('Length of actual data postet to the API: {0}'.format(len(r.text)))
        i +=1
        print('###########################################')
    
if __name__ == "__main__":
   run(client)