from enum import Enum

class Game(Enum):
    GNAME = 'gname'
    DESCRIPTION = 'description'
    GENRE = 'genre'
    DATE = 'date'
    PRICE = 'price'

class Developer(Enum):
    DNAME = 'dname'
    LOCATION = 'location'
    STARTED = 'started'

class Producer(Enum):
    PNAME = 'pname'
    NATION = 'nation'
    AGE = 'age'

class Composer(Enum):
    CNAME = 'cname'
    INAME = 'iname'
    MUSIC_GENRE = 'mgenre'
