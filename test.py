import sched
import time

schedule = sched.scheduler(time.time, time.sleep)

def func(s, f):
	print("[{}]".format(time.time()), "output: ", s, f)

print(time.time())
schedule.enter(10, 0, func, ("1", time.time()))
schedule.enter(20, 0, func, ("2", time.time()))
schedule.enter(30, 0, func, ("3", time.time()))
schedule.enter(40, 0, func, ("4", time.time()))
schedule.run()
print(time.time())