import nbformat
import re


FIRST_CELL = """############## PLEASE RUN THIS CELL FIRST! ###################

# import everything and define a test runner function
"""

UNITTEST_TEMPLATE_1 = '''### Exercise {num}

{exercise}

#### Make [this test](/edit/{path}/{module}.py) pass: `{module}.py:{test_suite}:{test}`'''


UNITTEST_TEMPLATE_2 = '''# Exercise {num}

reload({module})
run({module}.{test_suite}("{test}"))'''


PRACTICE_TEMPLATE_1 = '''### Exercise {num}
{exercise}'''


PRACTICE_TEMPLATE_2 = '''# Exercise {num}

{hints}'''


for chapter in range(1, 5):
    notebook = nbformat.v4.new_notebook()
    if chapter < 10:
        path = 'code-ch0{}'.format(chapter)
    else:
        path = 'code-ch{}'.format(chapter)
    with open('{}/examples.py'.format(path), 'r') as f:
        examples = {}
        current = ''
        current_key = None
        for line in f:
            if line.startswith('>>>') or line.startswith('...'):
                current += line[4:]
            elif line.startswith('# tag::example'):
                index = line.rfind('[')
                current_key = line[7:index]
            elif line.startswith('# end::example'):
                examples[current_key] = current
                current = ''
    with open('{}/answers.py'.format(path), 'r') as f:
        exercises = {}
        current = ''
        current_key = None
        for line in f:
            if line.startswith('# tag::exercise'):
                index = line.rfind('[')
                current_key = line[7:index]
            elif line.startswith('# end::exercise'):
                raw = current.strip()
                raw = raw[raw.find('\n\n')+1:]
                raw = raw.replace('$$', '`')
                raw = re.sub(r'([a-zA-Z+-])~(.+?)~', r'\\\\(\1_{\2}\\\\)', raw)
                raw = re.sub(r'([a-zA-Z0-9()\-+]+)\^(.+?)\^', r'\\\\(\1^{\2}\\\\)', raw)
                exercises[current_key] = raw
                current = ''
                current_key = None
            elif current_key is not None:
                current += line
    with open('{}/jupyter.txt'.format(path), 'r') as f:
        raw_cells = f.read().split('---\n')
    cells = notebook['cells']
    # first cell is always added with this:
    cells.append(nbformat.v4.new_code_cell(FIRST_CELL + raw_cells[0].strip()))
    for raw_cell in raw_cells[1:]:
        if raw_cell.startswith('exercise'):
            components = raw_cell.split(':')
            key = components[0]
            if len(components) == 4:
                template_dict = {
                    'path': path,
                    'num': key[8:],
                    'module': components[1],
                    'test_suite': components[2],
                    'test': components[3].strip(),
                    'exercise': exercises[key].strip(),
                }
                contents_1 = UNITTEST_TEMPLATE_1.format(**template_dict)
                contents_2 = UNITTEST_TEMPLATE_2.format(**template_dict)
            else:
                hints = '\n'.join(components[1:]).strip()
                template_dict = {
                    'num': key[8:],
                    'exercise': exercises[key],
                    'hints': hints,
                }
                contents_1 = PRACTICE_TEMPLATE_1.format(**template_dict)
                contents_2 = PRACTICE_TEMPLATE_2.format(**template_dict)
            cells.append(nbformat.v4.new_markdown_cell(contents_1))
            cells.append(nbformat.v4.new_code_cell(contents_2))
        elif raw_cell.startswith('example'):
            key = raw_cell.strip()
            cells.append(nbformat.v4.new_code_cell(examples[key].strip()))
        else:
            raise RuntimeError
    nbformat.write(notebook, '{}/Chapter{}.ipynb'.format(path, chapter))
    
