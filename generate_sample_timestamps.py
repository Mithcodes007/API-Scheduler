#!/usr/bin/env python3
import argparse, datetime

def gen(n=5, start=5, step=3):
    now = datetime.datetime.now()
    items = []
    for i in range(n):
        t = (now + datetime.timedelta(seconds=start + i*step)).time()
        items.append(t.strftime("%H:%M:%S"))
    print(",".join(items))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--start", type=int, default=5)
    p.add_argument("--step", type=int, default=3)
    a = p.parse_args()
    gen(a.n, a.start, a.step)
