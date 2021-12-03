#!/usr/bin/python3

from json import load, dumps
from sys import argv

# for debugging
# print_dict = lambda dic: print(dumps(dic, sort_keys=True, indent=4, separators=(',',': ')))

## PROCESSING

def match_flags(obj, f_in, f_ex): # match object flags
    if 'flags' in obj:
        match_in = ('all' in f_in) or f_in.intersection(obj['flags'])
        match_out = f_ex.intersection(obj['flags'])
        return match_in and not match_out
    else:
        return True

def filter_flags(obj, f_in, f_ex): # recursively filter with match_flags
    if type(obj) == list:
        filtered = (filter_flags(entry, f_in, f_ex) for entry in obj)
        return [entry for entry in filtered if entry] # only non-empty elements
    elif type(obj) == dict and match_flags(obj, f_in, f_ex):
        return {key:filter_flags(value, f_in, f_ex) for key, value in obj.items()}
    elif type(obj) == str:
        return obj # strings left unchanged

## GENERAL FORMATTING

def tex_list(lis): # convert list of strings to LaTeX list
    # lis: list<string>; list to format
    if not lis:
        return ""
    else:
        items = '\n'.join('\t\\item ' + entry for entry in lis)
        return f"\\begin{{LIST}}\n{items}\n\\end{{LIST}}"

def format_entry(obj, format_str): # convert object to LaTeX string
    # obj: dictionary; object to format
    # format_str: string; string to format
    for key, value in obj.items():
        if value:
            if type(value) == list and type(value[0]) == str:
                obj[key] = tex_list(value)
        else:
            value = ""
    try:
        return format_str.format(**obj)
    except KeyError:
        print('Format incompatible with given entry.')
        raise

def format_list(lis, formatf): # converet list of objects to section body
    # lis: list<dict>; section
    # formatf: string; path to format file for single element
    with open(formatf) as format_file:
        format_str = format_file.read()
    return '\n'.join(format_entry(entry, format_str) for entry in lis)

## SPECIFIC FORMATTING

def format_school(obj, format_dir):
    for school in obj:
        school['coursework'] = ', '.join(course['course'] for course in school['coursework'])
    return format_list(obj, f'{format_dir}/school')

def format_orgs(obj, format_dir):
    for org in obj:
        org['positions'] = format_list(org['positions'], f'{format_dir}/position')
    return format_list((org for org in obj if org['positions']), f'{format_dir}/org')

def format_projects(obj, format_dir):
    return format_list(obj, f'{format_dir}/project')

def format_skills(obj, format_dir):
    obj = {key: [skill["skill"] for skill in value] for key, value in obj.items()}
    with open(f'{format_dir}/skills') as form:
        form = form.read()
    return format_entry(obj, form)
## EXECUTION

def parse_args(args):
    # parse command line args defined in README
    return {
        'order':args[1], 'infile':args[2], 'format_dir':args[3],
        'flags_include':{flag[1:] for flag in args if flag[0]=='+'},
        'flags_exclude':{flag[1:] for flag in args if flag[0]=='-'}
    }

def gen_tex(order, infile, format_dir, flags_include, flags_exclude):
    # order: string; explained in README
    # infile: string; input file
    # format_dir: string; path to directory containing format files
    # flags_include: set<string>; inclusion flags
    # flags_exclude: set<strihg>; inclusion flags
    with open(infile) as data:
            data = load(data)
    data = filter_flags(data, flags_include, flags_exclude)

    format_funcs = { # formatting functions
        'e':format_school,
        'c':format_orgs,
        'p':format_projects,
        'w':format_orgs,
        's':format_skills
    }

    names = { # corresponding dict keys and section titles
        'e':'education',
        'c':'clubs',
        'p':'projects',
        'w':'experience',
        's':'skills',
    }

    with open(f'{format_dir}/info') as info:
        outs = '\n' + info.read().format(**data['info'])
    for c in order:
        if data[names[c]]: # exclude empty sections
            outs += f'\n\\rsection{{{names[c].upper()}}}\n' \
                + format_funcs[c](data[names[c]], format_dir)
    with open(f'{format_dir}/document') as doc:
        doc = doc.read()
    return doc.format(body = outs)

def main():
    print(gen_tex(**parse_args(argv)))

if __name__ == '__main__':
    main()
