import os

def check_text(line):
    line = line.strip()
    if '-->' in line or line == '':
        return ''
    else:
        if line.decode('utf-8-sig').encode('utf-8').isdigit():
            return ''
        else:
            return line


path = '../data/temp/'
fns = os.listdir(path)

with open('sub_text_loop.txt', 'wb') as fout:
    for fn in fns:
        with open(path + fn) as f:
            mid = fn.replace('.srt', '')
            text = ' '.join([check_text(x) for x in f]).strip()
        fout.write(mid + '\t' + text + '\n')



