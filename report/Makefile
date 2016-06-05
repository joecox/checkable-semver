
LATEX=pdflatex -file-line-error -interaction=nonstopmode 

.PHONY: all
all: report.tex graphics 
	latexmk -pdf -pdflatex="$(LATEX)" -use-make report.tex

.PHONY: auto
auto: report.tex
	latexmk -pdf -pdflatex="$(LATEX)" -use-make -pvc report.tex

plots := $(patsubst data/%.txt,graphics/%-plt.pdf,$(wildcard data/*.txt))

.PHONY: graphics
graphics: $(plots)
	@echo $(plots)


graphics/combined-violations-plt.pdf: data/combined-violations.txt plots/combined-violations.gnuplot
	gnuplot -e "data='$<'; outputfile='$@'; title='Combined Violations'" plots/combined-violations.gnuplot

graphics/violations-%-plt.pdf: data/violations-%.txt plots/violations.gnuplot
	gnuplot -e "data='$<'; outputfile='$@'; title='test-$*'" plots/violations.gnuplot

graphics/cumulative-%-plt.pdf: data/cumulative-%.txt plots/cumulative.gnuplot
	gnuplot -e "data='$<'; outputfile='$@'; title='test-$*'" plots/cumulative.gnuplot

graphics/simulation-plt.pdf: data/simulation.txt plots/simulation.gnuplot
	gnuplot -e "data='$<'; outputfile='$@'; title='Simulation'" plots/simulation.gnuplot

.PHONY: clean clean-aux
clean:
	rm -f report.pdf *.aux *.bbl *bcf *.blg *.log *.out *.tdo *.toc *.xdv *.synctex.gz *.fdb_latexmk *.fls *.run.xml *.lpc *.upa *.upb; \
	rm -f **/*.aux
	rm -f $(plots)

clean-aux:
	rm -f *.aux *.bbl *bcf *.blg *.log *.out *.tdo *.toc *.xdv *.synctex.gz *.fdb_latexmk *.fls *.run.xml *.lpc *.upa *.upb; \
	rm -f **/*.aux

