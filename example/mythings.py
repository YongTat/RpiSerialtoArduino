from __future__ import division, print_function
from webthing import (Action, Event, MultipleThings, Property, Thing, Value,
                      WebThingServer)
import logging
import random
import time
import tornado.ioloop
import uuid
import sqlite3

class FakeTempSensor(Thing):
    """A Temperature sensor which updates its measurement every few seconds."""

    def __init__(self, deviceid):
        self.deviceid = deviceid
        Thing.__init__(
            self,
            'mytempsensor:{}'.format(self.deviceid),
            'My {} Temp Sensor'.format(self.deviceid),
            ['MultiLevelSensor'],
            'A web connected Temp sensor'
        )

        self.level = Value(0.0)
        self.add_property(
            Property(self,
                     'level',
                     self.level,
                     metadata={
                         '@type': 'LevelProperty',
                         'title': 'Temperature',
                         'type': 'number',
                         'description': 'The current temperature in C',
                         'minimum': 0,
                         'maximum': 100,
                         'unit': 'celsius',
                         'readOnly': True,
                     }))

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update_level,
            10000
        )
        self.timer.start()

    def update_level(self):
        new_level = self.read_from_gpio(self.deviceid)
        logging.debug('setting new temperature level: %s', new_level)
        self.level.notify_of_external_update(new_level)

    def cancel_update_level_task(self):
        self.timer.stop()

    @staticmethod
    def read_from_gpio(deviceid):
        """Mimic an actual sensor updating its reading every couple seconds."""
        data = c.execute("SELECT * FROM {}".format(deviceid))
        final = list(data)
        return final[-1]
        # return random.randint(20,40)

class FakeHumidSensor(Thing):
    """A humidity sensor which updates its measurement every few seconds."""

    def __init__(self, deviceid):
        self.deviceid = deviceid
        Thing.__init__(
            self,
            'myhumidsensor:{}'.format(self.deviceid),
            'My {} Humidity Sensor'.format(self.deviceid),
            ['MultiLevelSensor'],
            'A web connected Humid sensor'
        )

        self.level = Value(0.0)
        self.add_property(
            Property(self,
                     'level',
                     self.level,
                     metadata={
                         '@type': 'LevelProperty',
                         'title': 'Humidity',
                         'type': 'number',
                         'description': 'The current humidity in %',
                         'minimum': 0,
                         'maximum': 100,
                         'unit': 'percent',
                         'readOnly': True,
                     }))

        logging.debug('starting the sensor update looping task')
        self.timer = tornado.ioloop.PeriodicCallback(
            self.update_level,
            10000
        )
        self.timer.start()

    def update_level(self):
        new_level = self.read_from_gpio(self.deviceid)
        logging.debug('setting new humidity level: %s', new_level)
        self.level.notify_of_external_update(new_level)

    def cancel_update_level_task(self):
        self.timer.stop()

    @staticmethod
    def read_from_gpio(deviceid):
        """Mimic an actual sensor updating its reading every couple seconds."""
        data = c.execute("SELECT * FROM {}".format(deviceid))
        final = list(data)
        return final[-1]
        # return random.randint(0,100)

def run_server():
    # Create a thing that represents a humidity sensor
    tempsensor1 = FakeTempSensor("A1")
    humidsensor1 = FakeHumidSensor("A1")
    tempsensor2 = FakeTempSensor("A2")
    humidsensor2 = FakeHumidSensor("A2")

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([tempsensor1, humidsensor1, tempsensor2, humidsensor2],
                                           'TempandHumidDevice'),
                            port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        tempsensor1.cancel_update_level_task()
        humidsensor1.cancel_update_level_task()
        tempsensor2.cancel_update_level_task()
        humidsensor2.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')

if __name__ == '__main__':
    conn = sqlite3.connect("sensor.db")
    c = conn.cursor()
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()