PLOTS=tex/time_vs_size.pdf tex/time_vs_delay_and_loss_probability.pdf tex/retransmissions_vs_delay_and_loss_probability.pdf
.PHONY: all clean new

all: informe.pdf

tex/time_vs_size.pdf:
	./time_vs_size_plot -o tex/time_vs_size.pdf

tex/time_vs_delay_and_loss_probability.pdf:
	./time_vs_delay_and_loss_probability_plot -o tex/time_vs_delay_and_loss_probability.pdf

tex/retransmissions_vs_delay_and_loss_probability.pdf:
	./retransmissions_vs_delay_and_loss_probability_plot -o tex/retransmissions_vs_delay_and_loss_probability.pdf

informe.pdf: tex/informe.tex $(PLOTS)
	cd tex; pdflatex -interaction=nonstopmode -halt-on-error informe.tex && \
	        pdflatex -interaction=nonstopmode -halt-on-error informe.tex
	mv tex/informe.pdf .

clean:
	rm -f informe.pdf tex/*.aux tex/*.log tex/*.toc tex/*.out tex/*.pdf

new: clean all