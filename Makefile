all: gen-src a_or_b a_star

gen-src:
	mkdir -p gen-src

a_or_b: gen-src | a_or_b.basm src/template.c
	python3 src/basm.py a_or_b.basm > gen-src/a_or_b.c

a_star: gen-src | a_star.basm src/template.c
	python3 src/basm.py a_star.basm > gen-src/a_star.c

clean:
	rm -f a_star
	rm -f a_or_b

.PHONY: clean all
