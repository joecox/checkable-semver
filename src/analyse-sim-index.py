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

    pat = re.compile("^A(?P<actual>.*),S(?P<sim>.*)$", re.M)
    with open(args.input_file, 'r') as fin:
        for line in fin:
            m = re.match(pat, line)
            actual = m.group("actual")
            sim = m.group("sim")

            actual_data.append(actual)
            sim_data.append(sim)

    all_data = semver.sort(list(set(actual_data + sim_data)))
    
    with open(args.output_file, 'w') as fo:
        for i in range(len(sim_data)):
            # fo.write("{} {} {}\n".format(i, all_data.index(actual_data[i]), all_data.index(sim_data[i])))
            fo.write("{} {} {} {} {}\n".format(all_data.index(actual_data[i]), all_data.index(actual_data[i]), all_data.index(sim_data[i]), all_data[i], sim_data[i]))

if __name__ == "__main__":
    main()
