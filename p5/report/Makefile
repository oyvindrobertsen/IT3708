.PHONY: all

TITLE = oyvinrob_p5

all:
	pdflatex ${TITLE}.tex
	bibtex ${TITLE}
	pdflatex ${TITLE}.tex
	pdflatex ${TITLE}.tex

.PHONY: clean
clean:
	rm -f *.aux *.bbl *.blg *.xml *.log *blx.bib *blg *blg
