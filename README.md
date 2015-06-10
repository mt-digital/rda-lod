## Research Data Alliance 
### Metadata IG Fellow Project

Welcome to the GitHub repository for the code and documentation
generated for the efforts to enable researchers to find related
datasets by converting dataset metadata to [RDF](http://www.w3.org/RDF/) [Linked Open
Data](http://www.w3.org/standards/semanticweb/data) (see also
http://linkeddata.org/) that follows the [HCLS standard](http://www.w3.org/2001/sw/hcls/notes/hcls-dataset/).

### Building documentation

To build the .docx documentation

```
make docx
```

and

```
make pdf
```

to build the pdf version. So far there is only the one-page proposal
due before I formally begin my work with the RDA.

Building documentation requires [pandoc (install page)](http://pandoc.org/installing.html); follow the instructions on the pandoc 
install page to also install the required latex distribution if you want to build the pdf.

### ld-book

The `ld-book` directory contains examples from the book _Linked Data: Structured
data on the Web_ by David Wood, Marsha Zaidman, and Luke Ruth with Michael
Hausenblas and a Foreward by Tim Berners-Lee (Manning)
([on
amazon](http://www.amazon.com/gp/product/1617290394/ref=pd_lpo_sbs_dp_ss_2?pf_rd_p=1944687602&pf_rd_s=lpo-top-stripe-1&pf_rd_t=201&pf_rd_i=1449306594&pf_rd_m=ATVPDKIKX0DER&pf_rd_r=0EVR96BNSE3F5XK3S6JR)).


