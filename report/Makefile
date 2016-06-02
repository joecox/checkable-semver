
LATEX=pdflatex -file-line-error -interaction=nonstopmode 

.PHONY: all
all: report.tex graphics 
	latexmk -pdf -pdflatex="$(LATEX)" -use-make report.tex

.PHONY: auto
auto: report.tex
	latexmk -pdf -pdflatex="$(LATEX)" -use-make -pvc report.tex

plots := $(patsubst %.gnuplot,%-plt.pdf,$(wildcard graphics/*.gnuplot))

.PHONY: graphics
graphics: $(plots)
	@echo $(plots)

%-plt.pdf: %.gnuplot %.txt 
	gnuplot $< > $@

.PHONY: clean clean-aux
clean:
	rm -f report.pdf *.aux *.bbl *bcf *.blg *.log *.out *.tdo *.toc *.xdv *.synctex.gz *.fdb_latexmk *.fls *.run.xml *.lpc *.upa *.upb; \
	rm -f **/*.aux

clean-aux:
	rm -f *.aux *.bbl *bcf *.blg *.log *.out *.tdo *.toc *.xdv *.synctex.gz *.fdb_latexmk *.fls *.run.xml *.lpc *.upa *.upb; \
	rm -f **/*.aux

