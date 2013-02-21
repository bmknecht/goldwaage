'''manages events'''


class Event(object):
    '''parent class for all events'''


class EventDispatcher(object):
    '''contains methods and calls them on events '''
    def __init__(self):
        self._events_and_listeners = {}

    def register_listener(self, eventtype, listener):
        '''add listener to list of an event'''
        if eventtype not in self._events_and_listeners:
            self._events_and_listeners[eventtype] = set()
        self._events_and_listeners[eventtype].add(listener)

    def fire_event(self, event):
        '''event was dispatched, call listeners'''
        for listener in self._events_and_listeners[event.__class__]:
            listener.handle_event(event)
