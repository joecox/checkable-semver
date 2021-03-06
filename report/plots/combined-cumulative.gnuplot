set terminal pdfcairo size 5,2 font "Times,6"

set output outputfile

set style line 11 lc rgb '#808080' lt 1
set border 3 back ls 11

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid ytics front ls 12

set tics nomirror

set key left

set boxwidth 0.5
set style fill solid

set xtics rotate by -50 font "Times,5"

set style line 1 lc rgb '#8b1a0e' pt 0 ps 1 lt 1 lw 2 # --- red
set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2 # --- green

set style fill solid 0.2

set ylabel 'Cumulative Violations' font "Times,7"
set xlabel 'Version'  font "Times,7"

plot data using 3:xtic(1) with filledcurves above x1 linestyle 1 title "all", \
    "" using 2:xtic(1) with filledcurves above x1 ls 2 title "jsapi"

