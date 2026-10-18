C_COMPILER = clang
C_FLAGS = -g -Wall -Wextra

all: frequency_analysis_s26 viginere_v26

frequency_analysis_s26: frequency_analysis_s26.o
	${C_COMPILER} ${C_FLAGS} frequency_analysis_s26.o -o frequency_analysis_s26

frequency_analysis_s26.o: frequency_analysis_s26.c
	${C_COMPILER} ${C_FLAGS} -c frequency_analysis_s26.c

viginere_v26: viginere_v26.o
	${C_COMPILER} ${C_FLAGS} viginere_v26.o -o viginere_v26

viginere_v26.o: viginere_v26.c
	${C_COMPILER} ${C_FLAGS} -c viginere_v26.c

clean:
	rm frequency_analysis_s26 frequency_analysis_s26.o viginere_v26 viginere_v26.o

