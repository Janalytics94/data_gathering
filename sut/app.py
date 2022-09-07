#!/usr/bin/env python3

#Imports
import time 
import datetime
import json
import os
import psutil
import random 
from flask import Flask, render_template, request, g as app_ctx
from pathlib import Path



# Remember Exponential distribution describes the time between events in a Poisson process : https://en.wikipedia.org/wiki/Poisson_point_process
# Parameter Lambda beschreibt die durchschnittliche Wartezeit bis zum nächsten "Ereignis". Ein größeres Lambda steht dabei für eine kleinere durchschnittliche Wartezeit.

# ADDITIONAL DATA MIGHT BE USEFUL: NUMBER OF REQUESTS COMING IN, UNHANDELED ERRORS, REQUEST LATENCY, QUEUED TIME QUEUE SIZE, WOKRER PROCESSES,THREAD INFO
# DIFFERENT TEST SCENARIOS: NUMBER OF THREADS, ANZAHL DER EINGABEN, GRÖßER, KLEINER, SEEDS


# Test Scenario: If the len(string) > 500 a delay should happen. The time of the delay is drawn from an exponential dist. On average a delay should happen every x seconds. 
# We choose the rate parameter lambda = 1/x. Rate parameter lambda is a measure of frequency: the average rate of events (here: delays) per unit of time(seconds)
# check that the average time of this function is really x -> following expression calculates the average of 100 function calls: sum([random.expovariate(1/x) for i in range(100)])/100 

# create log files
log_file = 'logs.json'
Path(os.path.join(os.path.dirname(os.path.abspath(__name__)), 'logs', log_file)).touch(exist_ok=True)
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs', log_file)

#set seed
random.seed(1000)

def create_json(path: str, data_of_interest: dict):
    """
    Dumps our data of interest into a json file
    """
    with open(path,'a+') as f:
        json.dump(
            data_of_interest,f)
        f.write('\n')
    return

# Flask App
app = Flask(__name__)

@app.route("/")
def input():
    return render_template("input.html")


@app.route('/post', methods=['GET', 'POST'])
def enter_string():
    # Start time
    app_ctx.start = time.time()
    #create the necessary data
    timestamp =  datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    #Call CPU-Utilization in the form of percentage of 10 seconds
    cpu_usage = psutil.cpu_percent(10)

    lambda_ = 20
    intervals=[int(random.expovariate((lambda_))) for i in range(100)]
    delays_in_ms = [interval/1000 for interval in intervals]    
    delay = random.choice(delays_in_ms)

    if request.method == 'POST':    

        string = request.form.get("data")
        print(string)
        string_length = len(string)
        print(string_length)
        
        response_time = time.time() - app_ctx.start

        # create data of interest
        data_of_interest = {
                'timestamp': timestamp,
                'input_data': {
                    'time_delay_in_miliseconds': delay, 'string_length' : string_length,'lambda': lambda_, 'string': string
                },
                'response_time_in_seconds': response_time,
                'response_method': request.method,
                'cpu_usage': cpu_usage
            }
        # if string length is exceeded over 500:
        if string_length > 50:
            print('String is too long...')
            lambda_ = 1./20
            # create time intervall to create synthetic bug: delay in reponse time of application if the length of the string, that was submitted exceeds a specific length(50)
            intervals=[int(random.expovariate((lambda_))) for i in range(100)]
            delays_in_ms = [interval/1000 for interval in intervals]       
            delay = random.choice(delays_in_ms)
            time.sleep(delay)
            
            # create data of interest with new delay and new lambda
            data_of_interest = {
                'timestamp': timestamp,
                'input_data': {
                    'time_delay_in_miliseconds': delay, 'string_length' : string_length, 'lambda': lambda_, 'string': string
                },
                'response_time_in_seconds': response_time + delay,
                'response_method': request.method,
                'cpu_usage': cpu_usage
            }

        create_json(path=path, data_of_interest=data_of_interest)
        
        return string



if __name__ == '__main__':
    app.run(debug=True)#threaded=True)# use multiple threads(?)

