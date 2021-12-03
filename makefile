ifndef $(order)
	order = epwcs
endif

ifndef $(flags)
	flags = +all -high -old -futuP -anci
endif

all:
	echo "Running engine with order $(order) and flags $(flags)"
	python3 engine.py $(order) resume.json resume/basic $(flags) > resume/resume.tex
	make -C resume
