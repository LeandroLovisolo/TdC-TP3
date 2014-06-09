.PHONY: all clean informe.pdf

clean:
	rm -f informe.pdf tex/*.aux tex/*.log tex/*.toc tex/*.out

informe.pdf: tex/informe.tex
	cd tex; pdflatex -interaction=nonstopmode -halt-on-error informe.tex && \
	        pdflatex -interaction=nonstopmode -halt-on-error informe.tex
	mv tex/informe.pdf .
