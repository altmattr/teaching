#!/bin/bash
set -e

echo "=== flyer.pdf ==="
latexmk -cd -pdf -interaction=nonstopmode flyer.tex
rm -f flyer.{aux,log,out,fdb_latexmk,fls}

echo "=== project/task.pdf ==="
latexmk -cd -pdf -interaction=nonstopmode project/task.tex
rm -f project/task.{aux,log,out,fdb_latexmk,fls}

for week in week{1..13}; do
    echo "=== $week/handout.pdf ==="
    latexmk -cd -pdf -interaction=nonstopmode "$week/handout.tex"
    rm -f "$week/"*.{aux,log,out,fdb_latexmk,fls}

    echo "=== $week/solutions.pdf ==="
    latexmk -cd -pdf -interaction=nonstopmode "$week/solutions.tex"
    rm -f "$week/"*.{aux,log,out,fdb_latexmk,fls}
done

echo "=== full_unit.pdf ==="
latexmk -cd -pdf -interaction=nonstopmode full_unit.tex
rm -f full_unit.{aux,log,out,fdb_latexmk,fls}

echo "Done"
