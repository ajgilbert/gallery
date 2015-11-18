#!/usr/bin/env python
import argparse
import os
import json
from collections import defaultdict

PLOT_ELE="""
  <div class="plot-element{tags}">
      <p class="file-title">{file}</p>
      <a href="{file}">
      <img src="{file}" alt="image">
      </a>{extra}
  </div>\n"""

OTHER_FORMATS="""
	<p>Other formats: {text}</p>"""

SINGLE_FORMAT="""
	<a href="{file}">[{ext}]</a>"""

BUTTON="""<button class="button" data-filter=".{FILTER}">{NAME}</button>"""

BUTTON_GROUP="""\n
<div class="button-group js-radio-button-group" data-filter-group="{GROUP}">
  <button class="button is-checked" data-filter="">All {TITLE}</button>
  {BUTTONS}
</div>"""

def CleanStr(arg):
	return '-'.join(arg.split())

parser = argparse.ArgumentParser()
parser.add_argument('input', help='input directory')
parser.add_argument('--verbose', '-v', action='store_true', help='print some info to the screen')
# parser.add_argument('output', help='output directory')
args = parser.parse_args()

indir = args.input
# outdir = args.output

if not os.path.isdir(indir):
	raise RuntimeError('Input argument %s is not a directory' % indir)

files = [f for f in os.listdir(indir) if os.path.isfile(os.path.join(indir,f))]
# print files

all_base_files = defaultdict(set)
for f in files:
	name,ext = os.path.splitext(f)
	all_base_files[name].add(ext)

# only keep the entries that have a png
base_files = {k: v for k, v in all_base_files.items() if '.png' in v}

elements = ''

groups = defaultdict(set)

for f, all_exts in base_files.iteritems():
	exts = [e for e in all_exts if e not in ['.png', '.json']]
	tags=''
	if '.json' in all_exts:
		json_data = {}
		with open(os.path.join(indir,f+'.json')) as jsonfile:
			json_data = json.load(jsonfile)
		for key, val in json_data.iteritems():
			groups[key].add(val)
		if len(json_data) > 0:
			tags = ' ' + ' '.join([CleanStr(x) for x in json_data.values()])
	do_exts = [SINGLE_FORMAT.format(file=f+e,ext=e) for e in exts]
	extra = ''
	info = '>> Adding %s.png to gallery' % f
	if len(do_exts) > 0:
		extra = OTHER_FORMATS.format(text=' '.join(do_exts))
		info += ' with extra extensions %s' % ','.join(exts)
	if args.verbose:
		print info
	elements += PLOT_ELE.format(file='%s.png'%f, tags=tags, extra=extra)

page_title = os.path.basename(os.path.normpath(indir))

button_groups=''
# The user has added some properties so we need to make buttons
if len(groups) > 1:
	for key, val in groups.iteritems():
		buttons='\n'.join([BUTTON.format(NAME=v, FILTER=CleanStr(v)) for v in val])
		button_groups += BUTTON_GROUP.format(GROUP=CleanStr(key), TITLE=key, BUTTONS=buttons)

# Get the template file
script_dir = os.path.dirname(os.path.realpath(__file__))
with open(script_dir+'/resources/index.html') as index_file:
    index = index_file.read()

index = index.replace('{TITLE}', page_title)
index = index.replace('{ELEMENTS}', elements)
index = index.replace('{BUTTONS}', button_groups)

# Write the html to the output folder
with open(os.path.join(indir,'index.html'), "w") as outfile:
    outfile.write(index)

