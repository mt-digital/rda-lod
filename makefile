
all: pdf docx
			

pdf: proposal-pdf plan-pdf
		

proposal-pdf: 
	pandoc -V fontsize=12pt -V geometry:margin=1in proposal.md -o proposal.pdf
	
plan-pdf:
	pandoc -V fontsize=12pt -V geometry:margin=1in plan.md -o plan.pdf

docx: proposal-docx plan-docx

proposal-docx:
	pandoc proposal.md -o proposal.docx

plan-docx:
	pandoc plan.md -o plan.docx

