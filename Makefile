LD_FLAGS := -Lc-lib-stack/build -lstack

LIBSTACK := c-lib-stack/build/libstack.a

all: gen-src a_or_b a_star

gen-src:
	mkdir -p gen-src

a_or_b: gen-src $(LIBSTACK) | a_or_b.basm src/template.c
	python3.12 src/basm.py a_or_b.basm > gen-src/a_or_b.c
	clang -o a_or_b gen-src/a_or_b.c $(LD_FLAGS)

a_star: gen-src $(LIBSTACK) | a_star.basm src/template.c
	python3.12 src/basm.py a_star.basm > gen-src/a_star.c
	clang -o a_star gen-src/a_star.c $(LD_FLAGS)

$(LIBSTACK):
	$(MAKE) -C c-lib-stack build/libstack.a

clean:
	rm -f a_star
	rm -f a_or_b
	rm -rf gen-src

.PHONY: clean all
