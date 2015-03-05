import os
import io
import chardet
import cPickle as pickle

def check_text(line):
    line = line.strip()
    if '-->' in line or line == '':
        return ''
    else:
        line = line.decode('utf-8-sig', 'replace').encode('utf-8')
        if line.isdigit():
            return ''
        else:
            return line

# 
# encodes = {'3149900.srt': None, '1453405.srt': None}

def extract_file(fn, path):
    mid = fn.replace('.srt', '')
    tt = []
    if fn in encodes:
        f = open(path + fn)
        content = f.read()
        f.close()
        r = chardet.detect(content)
        charenc = r['encoding']
        encodes[fn] = charenc
        with io.open(path + fn, 'r', encoding=charenc) as g:
            for x in g:
                y = check_text(x)
                if y:
                    tt.append(y)
            text = ' '.join(tt).strip()
    else:
        with open(path + fn) as g:
            for x in g:
                y = check_text(x)
                if y:
                    tt.append(y)
            text = ' '.join(tt).strip()
            # text = ' '.join([check_text(x) for x in g]).strip()
    # i = 0
    # print 'test'
    
        # mid = fn.replace('.srt', '')
        # lines = g.readlines()
        # temp = []
        # print 'test1'
        # print type(g)

        # for x in g:

        #     print 'i=', i
        #     temp.append(check_text(x))
        # text = ' '.join(temp).strip()
        # text = ' '.join([check_text(x) for x in lines]).strip()
        
    return mid, text


# def main():
encodes = pickle.load(open('encodes2.dct'))

path1 = '../data/subscene_subtitles/2013/'
path2 = '../data/opensubtitles/2013/'
fns1 = os.listdir(path1)
fns2 = os.listdir(path2)

with open('../data/txt/sub_text_2013_2.txt', 'wb') as fout:
    for fn in fns1:
        print 'parsing ' + fn
        mid, text = extract_file(fn, path1)
        # with open(path1 + fn) as f:
        #     mid = fn.replace('.srt', '')
        #     text = ' '.join([check_text(x) for x in f]).strip()
    # return mid, text
        fout.write(mid + '\t\t' + text + '\n')
    for fn in fns2:
        print 'parsing ' + fn
        mid, text = extract_file(fn, path2)
        fout.write(mid + '\t\t' + text + '\n')

pickle.dump(encodes, open('encodes2.dct','wb'))
# if __name__ == '__main__':
#     pass




