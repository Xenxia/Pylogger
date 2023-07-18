class Level_s:

    colaps1: str
    colaps2: str

    def __init__(self, colaps1: str = "", colops2: str = "") -> None:
        self.colaps1 = colaps1
        self.colaps2 = colops2

class Message_s:

    colaps1: str
    colaps2: str

    def __init__(self, colaps1: str = "", colops2: str = "") -> None:
        self.colaps1 = colaps1
        self.colaps2 = colops2

class Context_s:

    colaps1: str
    colaps2: str

    def __init__(self, colaps1: str = "", colops2: str = "") -> None:
        self.colaps1 = colaps1
        self.colaps2 = colops2

class Stack_s:

    colaps1: str
    colaps2: str
    context: int
    sep: str
    showMain: bool


    def __init__(self, colaps1: str = "", colops2: str = "", context: int = 10, sep: str = " > ", showMain: bool = True) -> None:
        self.colaps1 = colaps1
        self.colaps2 = colops2
        self.context = context
        self.sep = sep
        self.showMain = showMain

class User_s:

    colaps1: str
    colaps2: str

    def __init__(self, colaps1: str = "", colops2: str = "") -> None:
        self.colaps1 = colaps1
        self.colaps2 = colops2

class Time_s:

    colaps1: str
    colaps2: str

    def __init__(self, colaps1: str = "", colops2: str = "") -> None:
        self.colaps1 = colaps1
        self.colaps2 = colops2

class Style_logger:

    level: Level_s
    msg: Message_s
    ctx: Context_s
    stack: Stack_s
    user: User_s
    time: Time_s

    def __init__(self) -> None:
        self.level = Level_s()
        self.msg = Message_s()
        self.ctx = Context_s()
        self.stack = Stack_s()
        self.user = User_s()
        self.time = Time_s()