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

            # Parse into decimal
            m_actual = semver.parse(actual)
            m_sim = semver.parse(sim)

            f_actual = float(".{0:02d}{1:02d}{2:02d}".format(*m_actual))
            f_sim = float(".{0:02d}{1:02d}{2:02d}".format(*m_sim))

            actual_data.append(f_actual)
            sim_data.append(f_sim)
            
    with open(args.output_file, 'w') as fo:
        for i in range(len(sim_data)):
            fo.write("{} {} {}\n".format(i, actual_data[i], sim_data[i]))

if __name__ == "__main__":
    main()
