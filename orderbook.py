__author__ = 'fizi'

import collections
from bintrees import RBTree
from notification import Observer, Observable

class SellBook(Observer,Observable):
    """Class that adds and maintains all the sell orders
    Drawbacks: All price-points have to be different for a particular ticker
            Cannot offer two different quantities at same price-point

        :param _action: internal var to store the type of action
        :type _action: str
        :param tickrDict: dictionary to store RBTree of price:qty nodes for each ticker symbol
        :type tickrDict: dict

    """

    def __init__(self,*args, **kwargs):
        self._action = 'SELL'
        SellBook.tickrDict = {}
        super(SellBook, self).__init__(*args)

    def addOrder(self,order):
        """function to add a sell order to the SellOrder book and notify the matcher
        :param order: buy order
        :type: Order named tuple
        """
        if order.action == self._action:
            if not order.tickr in self.tickrDict:
                SellBook.tickrDict[order.tickr]=RBTree()
                SellBook.tickrDict[order.tickr].insert(order.price,order.qty)
            else:
                SellBook.tickrDict[order.tickr].insert(order.price,order.qty)
            self.notify_observers(order)

    @staticmethod
    def printBook():
        """static method to print the book"""
        print 'SellBook: ', SellBook.tickrDict

    def action(self,module, *args):
        """function to receive sell orders from OrderStream.
        Any other order stream can be added here

        :param module: the observed class object
        :type: OrderStream class object
        """
        if module.__class__.__name__ == 'OrderStream':
            self.addOrder(args[0])


class BuyBook(Observer,Observable):
    """Class that adds and maintains all the buy orders

        :param _action: internal var to store the type of action
        :type _action: str
        :param tickrDict: dictionary to store list of price:qty tuple for each ticker symbol
        :type tickrDict: dict

    """

    def __init__(self,*args, **kwargs):
        self._action = 'BUY'
        BuyBook.tickrDict = {}
        super(BuyBook, self).__init__(*args)

    def addOrder(self,order):
        """function to add a buy order to the BuyOrder book and notify the matcher
        :param order: buy order
        :type: Order named tuple
        """
        if order.action == self._action:
            if order.tickr not in self.tickrDict:
                BuyBook.tickrDict[order.tickr]=[(order.price,order.qty)]
            else:
                BuyBook.tickrDict[order.tickr].append((order.price,order.qty))
            self.notify_observers(order)

    @staticmethod
    def printBook():
        """static method to print the book"""
        print 'BuyBook: ', BuyBook.tickrDict

    def action(self,module, *args):
        """function to receive buy orders from OrderStream.
        Any other order stream can be added here

        :param module: the observed class object
        :type: OrderStream class object
        """
        if module.__class__.__name__ == 'OrderStream':
            self.addOrder(args[0])



