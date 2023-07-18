import getpass, inspect
from datetime import datetime
import ntpath
from typing import Tuple, Any

from .type import *

RESET = '\x1b[0m'
CRITICAL: int = 50
ERROR: int = 40
WARNING: int = 30
INFO: int = 20
DEBUG: int = 10

class Logger():

    onColor: bool = False

    time: datetime
    user: str

    file_path: str
    writingFile: bool = False

    format: str
    datefmt: str

    levellog: int = 20
    space: int = 0
    #[0] = level number;
    #[1] = level Name;
    #[2] = level color;
    #[3] = level color background;
    levelStyle: dict[str, list[Any]] = {
        "CRITICAL" : (50, "CRITICAL", "#FEFEFE", "#A00000"),
        "ERROR" : (40, "ERROR", "#FF3030", None),
        "WARNING" : (30, "WARNING", "#FFBA01", None),
        "INFO" : (20, "INFO", "#00E111", None),
        "DEBUG" : (10, "DEBUG", "#00E1DA", None),
    }

    logstyle = Style_logger()

    def __init__(self, format: str = None, datefmt: str = None, file_path: str = None, levellog: int = None, levelCustom: dict = None) -> None:

        self.format = format
        if datefmt is None:
            self.datefmt = "%d/%m/%Y %H:%M:%S"
        else:
            self.datefmt = datefmt

        if file_path is not None:
            self.writingFile = True
            self.file_path = file_path
            self.__write(f"\n═════════════════════╣ {self.__time()} ╠═════════════════════")

        if levellog is not None:
            self.levellog = levellog

        if levelCustom is not None:
            self.levelStyle.update(levelCustom)

        for value in self.levelStyle:
            len_l = len(self.levelStyle[value][1])
            if len_l >= self.space:
                self.space = len_l

        self.user = getpass.getuser()

    def __time(self, datefmt: str = None) -> str:
        time = datetime.now()
        if datefmt is not None:
            return time.strftime(datefmt)
        else:
            return time.strftime(self.datefmt)

    def __hex_to_rgb(self, value) -> Tuple[int, int, int]:
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    def __color(self, rgb: Tuple[int, int, int] = None, hex: str = None , bg_rgb: Tuple[int, int, int] = None, bg_hex: str = None):
        background = False
        if rgb is not None:
            r, g, b = rgb
        elif hex is not None:
            r, g, b = self.__hex_to_rgb(hex)

        if bg_rgb is not None:
            bg_r, bg_g, bg_b = bg_rgb
            background = True
        elif bg_hex is not None:
            bg_r, bg_g, bg_b = self.__hex_to_rgb(bg_hex)
            background = True

        color = f'\x1b[38;2;{r};{g};{b}m'
        if background:
            color = color + f'\x1b[48;2;{bg_r};{bg_g};{bg_b}m'
        
        return color

    def __write(self, msg: str):
        with open(self.file_path, "a", encoding="utf8") as file:
            file.write(msg+"\n")

    def __space(self, level: Tuple) -> str:

        sp = ""
        len_l = len(level[1])

        if len_l <= self.space:
            len_l = self.space - len_l
            for _ in range(len_l):
                sp = sp + " "

        return sp
    
    def __stack(self, context: int = 10, sep: str = " > ", showMain=True) -> str:
        stacks = inspect.stack()

        l = []


        for stack in stacks:

            try:
                if stack[0].f_locals['__name__'] == "__main__" and showMain: l.append(ntpath.basename(stack[0].f_locals['__file__'])+"|Main")
            except:
                try:
                    _class = stack[0].f_locals["self"].__class__.__name__
                    _function = stack[0].f_code.co_name

                    if _class == "Logger":
                        continue

                    l.append(_class+'.'+_function)
                
                except:
                    _function = stack[3]
                    if _function in ["eval_python", "<module>"]:
                        continue

                    l.append(_function)

        l = l[::-1][:context]
        return sep.join(l)

    def activColor(self, color: bool = False):
        if color: self.onColor = color

    def getlevellog(self) -> int:
        return self.levellog
    
    def getlevellogName(self) -> str:
        for k, v in self.levelStyle.items():
            if self.levellog == v[0]:
                return k
            
    def isEnableFile(self) -> bool:
        return self.writingFile


    def customize(self, message: Message_s = None, level: Level_s = None, context: Context_s = None, stack: Stack_s = None, time: Time_s = None, user: User_s = None):
        '''
        {msg} : message
        {context} : context
        {stack} : stack class function
        {time} : date time
        {levelname} : level
        {user} : user
        '''

        if level is not None: self.logstyle.level = level
        if message is not None: self.logstyle.msg = message
        if context is not None: self.logstyle.ctx = context
        if stack is not None: self.logstyle.stack = stack
        if time is not None: self.logstyle.time = time
        if user is not None: self.logstyle.user = user

    def log(self, level: str, msg: str, context: str = ""):

        if self.levellog > self.levelStyle[level][0]:
            return

        msg = str(msg)
        context = str(context)
        level = str(level)

        levelT: Tuple = self.levelStyle[level]

        color = self.__color(hex=levelT[2], bg_hex=levelT[3])

        s = self.logstyle.level
        styled_level = s.colaps1+levelT[1]+s.colaps2
        styled_color_level = s.colaps1+color+levelT[1]+RESET+s.colaps2

        s = self.logstyle.msg
        styled_msg = s.colaps1+msg+s.colaps2

        s = self.logstyle.ctx
        styled_context = s.colaps1+context+s.colaps2 if context != "" else ""

        
        s = self.logstyle.stack
        t = self.__stack(context=s.context, sep=s.sep, showMain=s.showMain)
        styled_stack = s.colaps1+t+s.colaps2 if t != "" else ""

        s = self.logstyle.user
        styled_user = s.colaps1+self.user+s.colaps2

        s = self.logstyle.time
        styled_time = s.colaps1+self.__time()+s.colaps2
        styled_color_time = s.colaps1+self.__color(hex="#eeeeee")+self.__time()+RESET+s.colaps2

        

        log = self.format.format(msg=styled_msg,
                                context=styled_context,
                                stack=styled_stack,
                                time=styled_color_time if self.onColor else styled_time, 
                                levelname= styled_color_level+self.__space(levelT) if self.onColor else styled_level+self.__space(levelT),
                                user=styled_user)

        print(log)

        if self.writingFile:
            self.__write(self.format.format(msg=styled_msg,
                                            context=styled_context,
                                            stack=styled_stack,
                                            time=styled_time,
                                            levelname=styled_level+self.__space(levelT),
                                            user=styled_user))

    def critical(self, msg: str, context: str = ""):
        self.log("CRITICAL", msg, context)

    def error(self, msg: str, context: str = ""):
        self.log("ERROR", msg, context)

    def warning(self, msg: str, context: str = ""):
        self.log("WARNING", msg, context)

    def info(self, msg: str, context: str = ""):
        self.log("INFO", msg, context)

    def debug(self, msg: str, context: str = ""):
        self.log("DEBUG", msg, context)

