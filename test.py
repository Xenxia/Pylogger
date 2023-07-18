from Pylogger import *


log = Logger(
    format="{time} | {levelname} : {stack}{context}{msg}",
    levellog=DEBUG
)

log.customize(level=Level_s("[", "]"), context=Context_s("{ ", " } "), stack=Stack_s("( ", " ) ", 10, " > ", False))

log.info("test", "oui")


def f1():
    log.debug("test", "oui")

f1()

def f2():
    f1()

def f3():
    f2()

f3()