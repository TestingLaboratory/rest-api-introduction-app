import os
import sys
from time import sleep
__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

with open(f"{__location__}/sleeper_messages.txt") as file:
    announcements = (message for message in file.readlines())

sleep(15)  # initial sleep for cunning purposes ;)
sys.stdin.write('printf "\033c"')
while True:
    try:
        sys.stdout.write(next(announcements))
        sys.stdout.flush()
    except StopIteration:
        pass
    sleep(60 * 10)
