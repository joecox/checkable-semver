set terminal pdfcairo size 5,2 font "Times,6"

set output outputfile

set style line 11 lc rgb '#808080' lt 1
set border 3 back ls 11

set style line 12 lc rgb '#808080' lt 0 lw 1
set grid ytics back ls 12

set tics nomirror

set boxwidth 0.5
set style fill solid

set xtics rotate by -50 font "Times,5"

set style line 1 lc rgb '#FF6E00' pt 0 ps 1 lt 1 lw 2 # --- red
set style line 2 lc rgb '#FFB612' pt 6 ps 1 lt 1 lw 2 # --- green
set style line 3 lc rgb '#4c5cc5' pt 0 ps 1 lt 1 lw 2 # --- red
set style line 4 lc rgb '#7AB800' pt 6 ps 1 lt 1 lw 2 # --- green

set ylabel '# Violations' font "Times,7"
set xlabel 'Version'  font "Times,7"

plot data u 7:xtic(1) with boxes ls 2 title "Added Features (all)", \
       "" u 5:xtic(1) with boxes ls 1 title "Breaking Changes (all)", \
       "" u 4:xtic(1) with boxes ls 4 title "Added Features (jsapi)", \
       "" u 2:xtic(1) with boxes ls 3 title "Breaking Changes (jsapi)"

