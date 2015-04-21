.PHONY: all

TITLE = mathiabo_oyvinrob_p4

all:
	pdflatex ${TITLE}.tex
	bibtex ${TITLE}
	pdflatex ${TITLE}.tex
	pdflatex ${TITLE}.tex

.PHONY: clean
clean:
	rm -f *.aux *.bbl *.blg *.xml *.log *blx.bib *blg *blg
