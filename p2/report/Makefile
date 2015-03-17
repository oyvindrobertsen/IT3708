.PHONY: all
all:
	pdflatex oyvinrob_p2.tex
	bibtex oyvinrob_p2
	pdflatex oyvinrob_p2.tex
	pdflatex oyvinrob_p2.tex

.PHONY: clean
clean:
	rm -f *.aux *.bbl *.blg *.xml *.log *blx.bib *blg *blg
