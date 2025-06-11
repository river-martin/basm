# rasm

An assembler-like tool for a regex assembly language (RASM).

## Build

```Bash
python3 -m venv .env
source .env/bin/activate
git submodule init
git submodule update
make
```

## Run examples

```Bash
./bin/a_or_b a
./bin/a_or_b b
./bin/a_or_b c
```

```Bash
./bin/a_star ""
./bin/a_star a
./bin/a_star aa
```
