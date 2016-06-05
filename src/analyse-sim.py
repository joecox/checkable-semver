import argparse
import re
import itertools
import semver

def main():
    p = argparse.ArgumentParser()
    p.add_argument("input_file")
    p.add_argument("output_file")

    args = p.parse_args()

    actual_data = []
    sim_data = []
    ult_data = []

    pat = re.compile("^A(?P<actual>.*),S(?P<sim>.*),S(?P<ult>.*)$", re.M)
    with open(args.input_file, 'r') as fin:
        for line in fin:
            m = re.match(pat, line)
            actual = m.group("actual")
            sim = m.group("sim")
            ult = m.group("ult")

            # Parse into decimal
            m_actual = semver.parse(actual)
            m_sim = semver.parse(sim)
            m_ult = semver.parse(ult)

            actual_data.append(m_actual)
            sim_data.append(m_sim)
            ult_data.append(m_ult)

    max_minor = {}
    for v in (sim_data + actual_data + ult_data):
        old_max = max_minor.get(v[0], 0)
        max_minor[v[0]] = max(v[1],old_max)
            
    with open(args.output_file, 'w') as fo:
        for i in range(len(sim_data)):
            simV = sim_data[i]
            ultV = ult_data[i]
            actV = actual_data[i]

            simMinor = int(100 * float(simV[1])/(max_minor[simV[0]] + 1))
            ultMinor = int(100 * float(ultV[1])/(max_minor[ultV[0]] + 1))
            actMinor = int(100 * float(actV[1])/(max_minor[actV[0]] + 1))

            f_actual = float("%02d.%02d" % (actV[0], actMinor))
            f_sim = float("%02d.%02d" % (simV[0], simMinor))
            f_ult = float("%02d.%02d" % (ultV[0], ultMinor))

            print "SimVersion = %s, f_sim = %s, ActVersion = %s, f_actual = %s" % (simV, f_sim, actV, f_actual)
            
            fo.write("{} {} {}\n".format(f_actual, f_sim, f_ult))

if __name__ == "__main__":
    main()
