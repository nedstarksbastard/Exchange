import collections
import time
import random
from notification import Observable

#named tuple for an order
Order = collections.namedtuple('Order', 'action tickr qty price time')

class OrderStream(Observable,object):
    """class to instantiate a stream of buy or sell orders
    It can be substituted with some other order input but the format of the order will need to stay the same
    """
    def __init__(self):
        super(OrderStream, self).__init__()

    def sendorder(self):
        """function to create and notify observer classes of the buy or sell orders
        """
        self.notify_observers(Order('BUY',random.choice(['GOOGL','IBM']),\
                                    12,23,time.time()))
        self.notify_observers(Order('SELL',random.choice(['GOOGL','IBM']),\
                                    4,23,time.time()))