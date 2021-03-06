from six import PY2

from procmon_parser.configuration import *
from procmon_parser.configuration_format import load_configuration, loads_configuration, dump_configuration, \
    dumps_configuration
from procmon_parser.logs import *
from procmon_parser.stream_logs_format import PMLStreamReader

__all__ = [
    'load_configuration', 'loads_configuration', 'dump_configuration', 'dumps_configuration', 'ProcmonLogsReader',
]


class ProcmonLogsReader(object):
    """Reads procmon logs from a stream which in the PML format
    """

    def __init__(self, f):
        """Build a ProcmonLogsReader object from ``f`` (a `.read()``-supporting file-like object).
        :param f: ``read`` supporting file-like object
        """
        self._struct_readear = PMLStreamReader(f)
        self._current_event_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current_event_index >= self.__len__():
            raise StopIteration
        current_index = self._current_event_index
        self._current_event_index += 1
        return self[current_index]

    if PY2:
        next = __next__

    def __getitem__(self, index):
        return self._struct_readear[index]

    def __len__(self):
        return self._struct_readear.number_of_events

    def processes(self):
        """Return a list of all the known processes in the log file
        """
        return self._struct_readear.processes()

    def system_details(self):
        """Return the system details of the computer which captured the logs (like Tools -> System Details in Procmon)
        """
        return self._struct_readear.system_details()
