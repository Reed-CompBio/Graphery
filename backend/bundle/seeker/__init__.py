"""
Seeker - seek the changes and store them input pocket

Usage::

        import seeker

        @seeker.tracer('x')  # watch list goes here
        def your_function(x):
            # implementations here
            ...

Credit: modified from PySnooper U{https://github.com/cool-RR/PySnooper/}
"""

from .sight import Tracer as tracer
from .variables import Attrs, Exploding, Indices, Keys
from collections import namedtuple

__VersionInfo = namedtuple('VersionInfo', ('major', 'minor', 'micro'))

__version__ = '0.1.0'
__version_info__ = __VersionInfo(*(map(int, __version__.split('.'))))

del namedtuple, __VersionInfo  # Avoid polluting the namespace
