set terminal pdfcairo size 5,2 font "Times,6"

set style line 11 lc rgb '#808080' lt 1
set border 3 back ls 11

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid ytics back ls 12

set tics nomirror

set boxwidth 0.5
set style fill solid

set xtics rotate by -50 font "Times,6"

set style line 1 lc rgb '#8b1a0e' pt 0 ps 1 lt 1 lw 2 # --- red
set style line 2 lc rgb '#5e9c36' pt 6 ps 1 lt 1 lw 2 # --- green

set ylabel 'Violations' font "Times,10"
set xlabel 'Version'  font "Times,10"

plot "graphics/violations.txt" using 4:xtic(1) with boxes ls 1 title "Breaking Changes", \
     "" u 2:xtic(1) with boxes ls 2 title "Added Features"
