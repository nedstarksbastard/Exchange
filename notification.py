__author__ = 'fizi'

class Observable(object):
    """ maintains a list of its dependents, called observers, and notifies them automatically of any state changes"""

    def __init__(self):
        self.__observers = []
        super(Observable, self).__init__()

    def register_observer(self, observer):
        """function to add an observer to the list
        :param observer: observer class to be notified upon an event
        :type observer: class object
        """
        self.__observers.append(observer)

    def notify_observers(self, *args, **kwargs):
        """function to notify observers upon an event"""
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)


class Observer(object):
    """Base class to register as an observer. Needs a subject class/classes upon instantiation that will observed for any events"""

    def __init__(self, *args):
        for arg in args:
            arg.register_observer(self)
        super(Observer, self).__init__()

    def notify(self, observable, *args, **kwargs):
        """The subject class will call this function to notify of any changes. This in turn calls action
        :param observable: observed class
        :type observable: class object
        :param *args: arguments specified. In this case, order
        :type *args: Ordernamed tuple

        """
        #print('Got', args, kwargs, 'From', observable)
        self.action(observable, *args)

    def action(self,observable, *args):
        """function to implement specific action to be taken by the child class upon notification"""
        raise NotImplementedError("Subclasses should implement this!")
