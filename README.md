# Python-driven resume engine
Using python file: 
`python engine.py <order> <infile> <format dir> <flags> >> <outfile>`

Using `make`: `make [order=<order>] [flags=<flags>]`. Default values in makefile.

`<order>` is an ordered subset of `ecpws`, where
- `e` is the Education section
- `c` is the Clubs section
- `p` is the Projects section
- `w` is the Work section
- `s` is the Skills section

`<flags>` define the OR-gated inclusion/exclusion flags for objects, where the
inclusion flags have prefix `+` and exclusion flags have prefix `-`. The
included elements will have at least one flag in common with the inclusions and
no flags in common with the exclusions.

At a high level, the engine:
1. Reads JSON file into dictionary
2. Recursively filters elements from dictionary using flags
3. Generates LaTeX using format files in a user-specified directory with defined names.
4. Prints that LaTeX to stdout. Use I/O redirection to send to TeX file.

TODO:
- Fix Skills section to appropriately space column items when page is not almost
  full
