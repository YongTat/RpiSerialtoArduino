from __future__ import division, print_function
from webthing import (Action, Event, MultipleThings, Property, Thing, Value,
                      WebThingServer)
import logging
import random
import time
import tornado.ioloop
import uuid

class FakeTempSensor(Thing):
    """A humidity sensor which updates its measurement every few seconds."""

    def __init__(self, deviceid):
        self.deviceid = deviceid
        Thing.__init__(
            self,
            'mytempsensor:{}'.format(self.deviceid),
            'My {} Sensor'.format(self.deviceid),
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
            3000
        )
        self.timer.start()

    def update_level(self):
        new_level = self.read_from_gpio()
        logging.debug('setting new temperature level: %s', new_level)
        self.level.notify_of_external_update(new_level)

    def cancel_update_level_task(self):
        self.timer.stop()

    @staticmethod
    def read_from_gpio():
        """Mimic an actual sensor updating its reading every couple seconds."""
        return random.randint(20,40)

def run_server():
    # Create a thing that represents a humidity sensor
    sensor1 = FakeTempSensor("A1")
    sensor2 = FakeTempSensor("A2")

    # If adding more than one thing, use MultipleThings() with a name.
    # In the single thing case, the thing's name will be broadcast.
    server = WebThingServer(MultipleThings([sensor1, sensor2],
                                           'LightAndTempDevice'),
                            port=8888)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.debug('canceling the sensor update looping task')
        sensor1.cancel_update_level_task()
        sensor2.cancel_update_level_task()
        logging.info('stopping the server')
        server.stop()
        logging.info('done')

if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()