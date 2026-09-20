#!/bin/bash
set -e

echo "=== slides.pdf ==="
latexmk -cd -pdf -interaction=nonstopmode slides.tex
rm -f slides.{aux,log,out,nav,snm,toc,vrb,fdb_latexmk,fls}

echo "=== handout.pdf ==="
latexmk -cd -pdf -interaction=nonstopmode handout.tex
rm -f handout.{aux,log,out,fdb_latexmk,fls}

echo "=== solutions.pdf ==="
latexmk -cd -pdf -interaction=nonstopmode solutions.tex
rm -f solutions.{aux,log,out,fdb_latexmk,fls}

echo "Done"