
all: pdf docx
			

pdf:
	pandoc proposal.md -o proposal.pdf

docx:
	pandoc proposal.md -o proposal.docx
