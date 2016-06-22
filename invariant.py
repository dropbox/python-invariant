import inspect

class Invariant(object):
    __invariants = {}

    class InvariantException(Exception):
        pass

    @staticmethod
    def get(invariant):
        return invariant.raw_invariant()

    @staticmethod
    def ensure(invariant, levels_up=0):
        ''' This function (in conjunction with the rest of the code in the class) takes in
            a value (the invariant parameter), and looks n=level_up stack frames up the stack
            for the location the value was passed in.  It then stores the location -> hash(value)
            in a global mapping, and if the same location has been seen before with a different
            value passed for the invariant, it raises an exception.  This means that the first
            value passed in from a location will never raise an exception, even if it isn't an
            invariant.

        '''

        if hasattr(invariant, 'raw_invariant'):
            return Invariant.get(invariant)
        else:
            Invariant(invariant, levels_up + 1)
            return invariant

    def __init__(self, invariant, levels_up=0):
        location = Invariant._get_caller_location(levels_up + 1)

        self.__invariant = invariant
        self.__location = location

        old_invariant = Invariant.__invariants.get(location)
        if old_invariant and old_invariant != hash(invariant):
            raise Invariant.InvariantException("The value at %s is not invariant!" % location)

        Invariant.__invariants[location] = hash(invariant)

    def raw_invariant(self):
        return self.__invariant


    # This may not be completely robust, so make sure to test it in your environment.
    # See:
    # - http://docs.python.org/2/library/inspect.html
    # - http://hg.python.org/cpython/file/2.7/Lib/inspect.py
    @staticmethod
    def _get_caller_location(levels_up=0):
        frame = inspect.currentframe()

        try:
            for i in range(levels_up + 1):
                frame = frame.f_back # Go up one level

            filename = frame.f_code.co_filename
            lineno = frame.f_lineno

        finally:
            # Get around the circular reference, just in case.
            # http://docs.python.org/2/library/inspect.html#the-interpreter-stack
            del frame

        return "%s:%i" % (filename, lineno)
