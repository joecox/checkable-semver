set terminal pdfcairo size 5,2 font "Times,6"

set title title font "Time,10"

set output outputfile

set xtics ("2.0.0" 9, "3.0.0" 32, "4.0.0" 33, "5.0.0" 34, "6.0.0" 35, "7.0.0" 36,\
           "8.0.0" 37, "9.0.0" 38\
          )
set ytics ("2.0.0" 9, "3.0.0" 32, "4.0.0" 33, "5.0.0" 34, "6.0.0" 35, "7.0.0" 36,\
           "8.0.0" 37, "9.0.0" 38\
          )

plot data using 1:2 title "Actual" with lines, \
     "" using 1:3 title "Simulated" with lines