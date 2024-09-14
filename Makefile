LIBSTACK := c-lib-stack/libstack.a

LD_FLAGS := -Lc-lib-stack -lstack

CODE_FILES := $(wildcard src/*.c src/*.h)


all: bin/a_or_b bin/a_star bin/memo

gen-src:
	mkdir -p gen-src

bin:
	mkdir -p bin

bin/a_or_b:  $(LIBSTACK) $(CODE_FILES) a_or_b.rasm | gen-src bin
	python3.12 src/rasm.py a_or_b.rasm > gen-src/a_or_b.c
	clang -o bin/a_or_b gen-src/a_or_b.c $(LD_FLAGS)

bin/a_star: $(LIBSTACK) $(CODE_FILES) a_star.rasm | gen-src bin
	python3.12 src/rasm.py a_star.rasm > gen-src/a_star.c
	clang -o bin/a_star gen-src/a_star.c $(LD_FLAGS)

bin/memo: $(LIBSTACK) $(CODE_FILES) memo.rasm | gen-src bin
	python3.12 src/rasm.py memo.rasm > gen-src/memo.c
	clang -o bin/memo gen-src/memo.c $(LD_FLAGS)

$(LIBSTACK):
	$(MAKE) -C c-lib-stack libstack.a

clean:
	rm -rf bin
	rm -rf gen-src

.PHONY: clean all
