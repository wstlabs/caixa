"""Demonstrates usage of @timed decorator in `caixa.decorators`""" 
import time
import random 
from caixa.decorators import timed


@timed(bare=False)
def boofar(string: str) -> int:
    delay = random.random() * .4
    time.sleep(delay)
    return len(string)

(delta, length) = boofar("bwah!")
print(f"bare=False: got {length} in {delta} sec")


@timed(bare=True)
def doowoop(string: str) -> None: 
    delay = random.random() * .4
    time.sleep(delay)
    return None

delta = doowoop("bwah!")
print(f"bare=True: got nothing in {delta} sec")


@timed() # defaults to bare=False
def woohoo(string: str) -> int:
    delay = random.random() * .4
    time.sleep(delay)
    return len(string)

(delta, length) = woohoo("bwah!")

print(f"Argless case: got {length} in {delta} sec")

