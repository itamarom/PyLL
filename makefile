all: main.c
	clang -O0 -S -emit-llvm main.c
