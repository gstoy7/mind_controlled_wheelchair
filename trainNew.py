from cortex import Cortex
import json
from collections import Counter
from statistics import mode
import socket
import time
i = 0
messages = []
UDP_IP = '128.153.171.170'
UDP_PORT = 12345
currentTime = 0
prevTime = 0
print("UDP target: ", UDP_IP)
print("UDP target port: ", UDP_PORT)
s = socket.socket()
s.connect((UDP_IP, UDP_PORT))
class Train():
"""
A class to use BCI API to control the training of the mental command detections.
Attributes
----------
c : Cortex
Cortex communicate with Emotiv Cortex Service
Methods
-------
do_prepare_steps():
Do prepare steps before training.
subscribe_data():
To subscribe to one or more data streams.
load_profile(profile_name):
To load an existed profile or create new profile for training
unload_profile(profile_name):
To unload an existed profile or create new profile for training
train_mc(profile_name, training_action, number_of_train):
To control the training of the mental command action.
live(profile_name):
Load a trained profiles then subscribe mental command data to enter live mode
on_new_data(*args, **kwargs):
To handle mental command data emitted from Cortex
"""
    def __init__(self):
    """
    Constructs cortex client and bind a function to handle subscribed data streams for the
    Train object
    If you do not want to log request and response message , set debug_mode = False. The
    default is True
    """
    self.c = Cortex(user, debug_mode=True)
    self.c.bind(new_com_data=self.on_new_data)
    The Mind-Controlled Wheelchair Page 16
    def do_prepare_steps(self):
    """
    Do prepare steps before training.
    Step 1: Connect a headset. For simplicity, the first headset in the list will be
    connected in the example.
    If you use EPOC Flex headset, you should connect the headset with a proper
    mappings via EMOTIV Launcher first
    Step 2: requestAccess: Request user approval for the current application for first
    time.
    You need to open EMOTIV Launcher to approve the access
    Step 3: authorize: to generate a Cortex access token which is required parameter of
    many APIs
    Step 4: Create a working session with the connected headset
    Returns
    -------
    None
    """
    self.c.do_prepare_steps()
    def subscribe_data(self, streams):
    """
    To subscribe to one or more data streams
    'com': Mental command
    'fac' : Facial expression
    Parameters
    ----------
    streams : list, required
    list of streams. For example, ['com']
    Returns
    -------
    None
    """
    self.c.sub_request(streams)
    def load_profile(self, profile_name):
    """
    To load an existed profile or create new profile for training
    Parameters
    ----------
    profile_name : str, required
    profile name
    Returns
    -------
    None
    """
    profiles = self.c.query_profile()
    if profile_name not in profiles:
    status = 'create'
    self.c.setup_profile(profile_name, status)
    status = 'load'
    self.c.setup_profile(profile_name, status)
    def unload_profile(self, profile_name):
    """
    To unload an existed profile or create new profile for training
    Parameters
    ----------
    profile_name : str, required
    profile name
    Returns
    -------
    None
    """
    profiles = self.c.query_profile()
    The Mind-Controlled Wheelchair Page 17
    if profile_name in profiles:
    status = 'unload'
    self.c.setup_profile(profile_name, status)
    else:
    print("The profile " + profile_name + " is not existed.")
    def train_mc(self, profile_name, training_action, number_of_train):
    """
    To control the training of the mental command action.
    Make sure the headset is at good contact quality. You need to focus during 8 seconds
    for training an action.
    For simplicity, the training will be called to accepted automatically and then the
    training will be saved.
    Parameters
    ----------
    profile_name : string, required
    name of training profile
    training_action : string, required
    mental command action, for example: neutral, push, pull, lift...
    number_of_train : int, required
    number of training for the action
    Returns
    -------
    None
    """
    print('begin train -----------------------------------')
    num_train = 0
    while num_train < number_of_train:
    num_train = num_train + 1
    print('start training {0} time {1} ---------------'.format(training_action,
    num_train))
    print('\n')
    status='start'
    self.c.train_request(detection='mentalCommand',
    action=training_action,
    status=status)
    print('accept {0} time {1} ---------------'.format(training_action, num_train))
    print('\n')
    status='accept'
    self.c.train_request(detection='mentalCommand',
    action=training_action,
    status=status)
    print('save trained action')
    status = "save"
    self.c.setup_profile(profile_name, status)
    def live(self, profile_name):
    """
    Load a trained profiles then subscribe mental command data to enter live mode
    Returns
    -------
    None
    """
    print('begin live mode ----------------------------------')
    # load profile
    status = 'load'
    self.c.setup_profile(profile_name, status)
    # sub 'com' stream and view live mode
    stream = ['com']
    The Mind-Controlled Wheelchair Page 18
    self.c.sub_request(stream)
    def on_new_data(self, *args, **kwargs):
    """
    To handle mental command data emitted from Cortex
    Returns
    -------
    data: dictionary
    the format such as {'action': 'neutral', 'power': 0.0, 'time': 1590736942.8479}
    """
    global i
    global messages
    global s
    global currentTime
    global prevTime
    data = kwargs.get('data')
    if(i == 0):
    prevTime = time.time()
    # print('mc data: {}'.format(data))
    #eeg_dict = json.loads(data)
    #messages[i] = eeg_dict['action']
    messages.append(data['action'])
    print(messages[i])
    i = i + 1
    currentTime = time.time()
    if (currentTime >= prevTime + 0.5):
    i = 0
    print(mode(messages))
    s.send(mode(messages).encode())
    messages.clear()
    print(s.recv(1024))
# -----------------------------------------------------------
'''
SETTING
- replace your license, client_id, client_secret to user dic
- naming your profile
- connect your headset with dongle or bluetooth, you should saw headset on EmotivApp.
make sure the headset at good contact quality.
TRAIN
you need to folow steps:
1) do_prepare_steps: for authorization, connect headset and create working session.
2) subscribe 'sys' data for Training Event
3) load a profile with the connected headset
4) do training actions one by one. Begin with neutral action
LIVE
you can run live mode with the trained profile. the data as below:
{'action': 'neutral', 'power': 0.0, 'time': 1590736942.8479}
{'action': 'neutral', 'power': 0.0, 'time': 1590736942.9729}
{'action': 'push', 'power': 0.345774, 'time': 1590736943.0979}
{'action': 'push', 'power': 0.294056, 'time': 1590736943.2229}
{'action': 'push', 'power': 0.112473, 'time': 1590736943.3479}
'''
"""
client_id, client_secret:
To get a client id and a client secret, you must connect to your Emotiv account on
emotiv.com and create a Cortex app
For training purpose, you should set empty string for license
The Mind-Controlled Wheelchair Page 19
"""
user = {
"license" : "LICENSE ID",
"client_id" : "nqfvFPCklM6UQyjl6nxKXC7BAJQ7erxFTuTaSSm3",
"client_secret" :
"w2dfJcfJ95qOhsweAAAqaMMgiDg3ypK5x7uV69BpV6MCJ0cQj7AtJ7n3W4a58WFi9wzqUdrdtoJeTTt7sQUEjPAUIlwc7
S1zDX3KHmRvJ5migHNA0s2KnGkArOYIkyp0",
"debit" : 100
}
# name of training profile
profile_name = 'NAME'
# number of training time for one action
number_of_train = 1
# Init Train
t=Train()
# Do prepare steps
t.do_prepare_steps()
# subscribe sys stream to receive Training Event
t.subscribe_data(['sys'])
# load existed profile or create a new profile
t.load_profile(profile_name)
training_action = 'disappear'
t.train_mc(profile_name, training_action, number_of_train)
# Training neutral action
training_action = 'neutral'
t.train_mc(profile_name, training_action, number_of_train)
# # add active action
# Training left action
training_action = 'push'
t.train_mc(profile_name, training_action, number_of_train)
# Training right action
training_action = 'pull'
t.train_mc(profile_name, training_action, number_of_train)
# Training right action
training_action = 'left'
t.train_mc(profile_name, training_action, number_of_train)
# Training right action
training_action = 'right'
t.train_mc(profile_name, training_action, number_of_train)
# unload profile
t.unload_profile(profile_name)
# start live mode with profile
t.live(profile_name)
