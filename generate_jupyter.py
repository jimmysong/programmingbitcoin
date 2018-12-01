import nbformat


for chapter in range(1, 3):
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
            if line.startswith('    >>>'):
                current += line[8:]
            elif line.startswith('# tag::example'):
                index = line.rfind('[')
                current_key = line[7:index]
            elif line.startswith('# end::example'):
                examples[current_key] = current
                current = ''
    with open('{}/jupyter.txt'.format(path), 'r') as f:
        raw_cells = f.read().split('---\n')
    for raw_cell in raw_cells:
        if raw_cell.startswith('### Exercise'):
            cell = nbformat.v4.new_markdown_cell(raw_cell.strip())
        elif raw_cell.startswith('example'):
            key = raw_cell.strip()
            cell = nbformat.v4.new_code_cell(examples[key].strip())
        else:
            cell = nbformat.v4.new_code_cell(raw_cell.strip())
        notebook['cells'].append(cell)
    nbformat.write(notebook, '{}/Chapter{}.ipynb'.format(path, chapter))
    
