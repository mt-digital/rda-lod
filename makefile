
all: pdf docx
			

pdf:
	pandoc -V geometry:margin=1in proposal.md -o proposal.pdf

docx:
	pandoc proposal.md -o proposal.docx
