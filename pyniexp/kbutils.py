import time

try:
    import keyboard
except ImportError:
    print('module "keyboard" is not installed')
    raise(ImportError)

try:
    kbLayout = [k[0] for k in keyboard._os_keyboard.official_virtual_keys.values()]
except AttributeError:
    # a terrible hack to fix keybord portability    
    kbLayout = [
        'control-break processing', 'backspace', 'tab', 'clear', 'enter', 'shift', 
        'ctrl', 'alt', 'pause', 'caps lock', 'ime hangul mode', 'ime junja mode',
        'ime final mode', 'ime kanji mode', 'esc', 'ime convert', 'ime nonconvert',
        'ime accept', 'ime mode change request', 'spacebar', 'page up', 'page down',
        'end', 'home', 'left', 'up', 'right', 'down', 'select', 'print', 'execute',
        'print screen', 'insert', 'delete', 'help', '0', '1', '2', '3', '4', '5', '6',
        '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'left windows', 
        'right windows', 'applications', 'sleep', '0', '1', '2', '3', '4', '5', '6', '7',
        '8', '9', '*', '+', 'separator', '-', 'decimal', '/', 'f1', 'f2', 'f3', 'f4', 'f5',
        'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 
        'f18', 'f19', 'f20', 'f21', 'f22', 'f23', 'f24', 'num lock', 'scroll lock', 
        'left shift', 'right shift', 'left ctrl', 'right ctrl', 'left menu', 'right menu', 
        'browser back', 'browser forward', 'browser refresh', 'browser stop', 'browser search key', 
        'browser favorites', 'browser start and home', 'volume mute', 'volume down', 'volume up', 
        'next track', 'previous track', 'stop media', 'play/pause media', 'start mail', 'select media',
        'start application 1', 'start application 2', '+', ',', '-', '.', 'ime process', 'attn', 'crsel',
        'exsel', 'erase eof', 'play', 'zoom', 'reserved ', 'pa1', 'clear'
    ]


class Key:
    name = ''
    state = ''
    timeDown = 0
    timeUp = 0
    @property
    def time(self):
        return max(self.timeDown,self.timeUp)

    def __init__(self,name):
        self.name = name
        self.state = 'up'

    def eventTime(self,etype):
        if etype == 'down': return self.timeDown
        elif etype == 'up': return self.timeUp
        else: return -1
    
    def update(self,etype,val):
        self.state = etype
        if self.state == 'down': self.timeDown = val
        elif self.state == 'up': self.timeUp = val
        
class Kb:
    
    @property 
    def is_alive(self):
        return self.__is_alive

    def __init__(self):
        # Private property
        self.__keys = [Key(name) for name in kbLayout]
        self.__is_alive = False
    
        self.start()
        
    def start(self):
        if not(self.is_alive): keyboard.hook(self.__store_keys)
        self.__is_alive = True

    def stop(self):
        if self.is_alive: keyboard.unhook_all()
        self.__is_alive = False

    def kbCheck(self):
        return [(k.name, k.state, k.time) for k in self.__keys]

    def __store_keys(self,e):
            K = [k for k in self.__keys if k.name == e.name]
            if len(K):
                K[0].update(e.event_type,e.time)