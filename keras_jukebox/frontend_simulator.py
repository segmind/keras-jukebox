import paho.mqtt.client as mqtt
import json, threading, time


class Mqttc(object):
    """docstring for Mqttc"""
    def __init__(self, host='localhost', port=1883):
        super(Mqttc, self).__init__()
        self.host = host
        self.port = port
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.topic = None
        self.msg = None
        self.client.connect(host=self.host, port=self.port, keepalive=60, bind_address="")
        self.start = False

    def on_connect(self, client, userdata, flags, rc):
        print("Connected to {} with result code {}".format(self.host,rc))
        #self.client.subscribe('test')

    def read_message(self):
        return self.topic, self.msg

    def on_message(self,client, userdata, msg):
        self.topic = msg.topic
        self.msg = json.loads(msg.payload.decode('utf-8'))
        #print("got a message")
        print(self.topic+" "+str(self.msg))

    def subscribe_to(self, topic):
        self.client.subscribe(topic)
        #print("subscribed to {}".format(topic))

    def start_listening(self):
        """
        Start listening to broker for messages
        """
        if self.start:
            print("Loop started Already")
        else:
            self.start = True
            while self.start:
                self.client.loop(timeout=1.0, max_packets=1)

    def stop_listening(self):
        self.start = False

    def publish_data(self, topic, payload, qos=0, retain=False):
        assert isinstance(payload, dict)
        payload = json.dumps(payload, indent=2)
        self.client.publish(topic, payload=payload, qos=qos, retain=retain)
        #print(payload)

    def disconnect(self):
        self.client.disconnect()


class SpawnAndInterrupt(Mqttc):
    """docstring for SpawnAndInterrupt"""
    def __init__(self, PID, **kwargs):
        super(SpawnAndInterrupt, self).__init__(**kwargs)
        self.interrupt = False
        self.PID = PID

    def on_message(self,client, userdata, msg):
        message = json.loads(msg.payload.decode('utf-8'))
        print(message)
        #if message['cmd'] == 'stop' : #and message['PID']==self.PID:
        #    self.interrupt = True
        #    print("process interrupted")
        #    self.stop_listening()

    def listen(self):
        thr = threading.Thread(target=self.start_listening)
        thr.daemon = True
        thr.start()


def main():
    #['play','pause','stop']
    sim = SpawnAndInterrupt(9988)
    sim.subscribe_to(topic='keras_JukeBox/frontend/199')
    sim.listen()


    payload = {'PID':199,'status':'acknowledged'}
    # acknowledge
    sim.publish_data('keras_JukeBox/backend/199', payload=payload)
    print('sent ack')

    time.sleep(2)

    #play
    payload = {
    'tab1':{'play_status':'play'},
    'tab2':{'learning_rate':0.001}}

    sim.publish_data('keras_JukeBox/backend/199', payload=payload)
    print('sent play command')

    time.sleep(2)


    #pause
    payload = {
    'tab1':{'play_status':'pause'},
    'tab2':{'learning_rate':0.001}}

    sim.publish_data('keras_JukeBox/backend/199', payload=payload)
    print('sent play command')

    time.sleep(2)


    #play
    payload = {
    'tab1':{'play_status':'play'},
    'tab2':{'learning_rate':0.0001}}

    sim.publish_data('keras_JukeBox/backend/199', payload=payload)
    print('sent play command')

    time.sleep(5)

    #pause

    payload = {
    'tab1':{'play_status':'pause'},
    'tab2':{'learning_rate':0.001}}

    sim.publish_data('keras_JukeBox/backend/199', payload=payload)
    print('sent play command')

    time.sleep(6)

    # play
    payload = {
    'tab1':{'play_status':'play'},
    'tab2':{'learning_rate':0.0009}}

    sim.publish_data('keras_JukeBox/backend/199', payload=payload)
    print('sent play command')

    time.sleep(5)

    # test illegal play command
    payload = {
    'tab1':{'play_status':'fake'},
    'tab2':{'learning_rate':0.0009}}

    sim.publish_data('keras_JukeBox/backend/199', payload=payload)
    print('sent play command')

    time.sleep(5)
    #stop

    payload = {
    'tab1':{'play_status':'stop'},
    'tab2':{'learning_rate':0.0009}}

    sim.publish_data('keras_JukeBox/backend/199', payload=payload)
    print('sent play command')

if __name__ == '__main__':
    main()