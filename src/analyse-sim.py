import argparse
import re

import semver

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input_file")
    p.add_argument("output_file")

    args = p.parse_args()

    actual_data = []
    sim_data = []

    actual_sum = 0
    sim_sum = 0
    
    last_actual = "1.0.0"
    last_sim = "1.0.0"

    pat = re.compile("^A(?P<actual>.*),S(?P<sim>.*)$", re.M)
    with open(args.input_file, 'r') as fin:
        for line in fin:
            m = re.match(pat, line)
            actual = m.group("actual")
            sim = m.group("sim")

            actual_sum += add_diff(actual, last_actual)
            sim_sum += add_diff(sim, last_sim)

            actual_data.append(actual_sum)
            sim_data.append(sim_sum)
            
            last_actual = actual
            last_sim = sim

    with open(args.output_file, 'w') as fo:
        for i in range(len(sim_data)):
            fo.write("{} {} {}\n".format(i, actual_data[i], sim_data[i]))

def add_diff(v1, v2):
    diff = semver.diff(v1, v2)
    if diff == 3:
        return 20
    elif diff == 2:
        return 4
    else:
        return 1
            
if __name__ == "__main__":
    main()
