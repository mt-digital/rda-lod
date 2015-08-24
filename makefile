
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

p6_final:
	pandoc -o final_p6_plan.pdf final_p6_plan.md && open final_p6_plan.pdf

p6_final_draft:
	pandoc -H draft.sty -o final_p6_plan.pdf final_p6_plan.md && open final_p6_plan.pdf

p6_final_html:
	pandoc final_p6_plan.md -c writeups.css -s --highlight-style pygments -o final_p6_plan.html && open final_p6_plan.html
