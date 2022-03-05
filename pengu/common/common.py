import enum

class Cell(enum.Enum):
    """Encapsulates the elements in the game to human readable format.
    """
    wall = '#'
    ice = ' '
    ice_with_fish = '*' 
    snow = '0'
    pengu = 'P'
    bear = 'U'
    shark = 'S'
    death = 'X'
    empty = ''