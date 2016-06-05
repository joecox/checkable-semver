set terminal pdfcairo size 5,2 font "Times,6"

set title title font "Time,10"

set output outputfile

plot data using 2 title "Actual" with lines, \
     "" using 3 title "Simulated" with lines