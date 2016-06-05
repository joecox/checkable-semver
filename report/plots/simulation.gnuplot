set terminal pdfcairo size 5,2 font "Times,6"

set style line 11 lc rgb '#808080' lt 1
set border 3 back ls 11

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid ytics back ls 12

set tics nomirror

set boxwidth 0.5
set style fill solid

set xtics rotate by -50 font "Times,5"

set style line 1 lc rgb '#FF6E00' pt 0 ps 0.2 lt 1 lw 2 # --- red
set style line 2 lc rgb '#FFB612' pt 0 ps 0.2 lt 1 lw 2 # --- green
set style line 3 lc rgb '#4c5cc5' pt 0 ps 0.2 lt 1 lw 2 # --- red
set style line 4 lc rgb '#7AB800' pt 0 ps 0.2 lt 1 lw 2 # --- green


set ylabel 'Version Number' font "Times,7"
set xlabel 'Release Number'  font "Times,7"

set key left

set output outputfile
#set xtics rotate by -50 font "Times,5"

# set xrange [0.01:0.021]
# set yrange [0.01:0.055]

# set xtics ("1.0.0" 1, "2.0.0" 1) #, "3.0.0" 0.03, "4.0.0" 0.04, "5.0.0" 0.05, "6.0.0" 0.06)
set ytics ("1.0.0" 1, "2.0.0" 2, "3.0.0" 3, "4.0.0" 4, "5.0.0" 5, "6.0.0" 6)

plot data using 1 title "Actual" with linespoints pointtype 5 pointsize 0.2, \
     "" using 2 title "Simulated" with linespoints pointtype 6 pointsize 0.2 # , \
#     "" using 3 title "Simulated Ignore" with linespoints pointtype 6 pointsize 0.2     