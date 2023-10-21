

class Button():
    '''location as (x,y), dimensions as (width, height). location will be the top left 
    corner of the button box rect'''
    def __init__(self, location:tuple, dimensions:tuple, func) -> None:
        self.location = location # (x, y)
        self.dimensions = dimensions
        self.func = func
    def click(self, location):
        if self.location[0] < location[0] < (self.location[0]+self.dimensions[0]):
            if self.location[1] < location[1] < (self.location[1]+self.dimensions[1]):
                return True
        return False
    def activate(self, *args):
        '''any positional arguments are passed as a tuple into the function'''
        self.func(args)

def button_func(*args):
    print('this function has worked!')

button = Button((500, 500), (200, 100), button_func)

if button.click((600,550)):
    button.activate()