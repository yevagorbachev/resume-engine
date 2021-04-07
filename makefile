ifndef $(order)
	order = ecwps
endif

ifndef $(flags)
	flags = +flag1 -flag2
endif

all:
	python3 engine.py $(order) resume.json resume/basic $(flags) > resume/resume.tex
	make -C resume
