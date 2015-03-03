from mrjob.job import MRJob
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



class MRExtractSub(MRJob):

    def mapper(self, _, line):
        filename = os.environ['map_input_file'].split("/")[-1].split("\\")[-1].replace('.srt', '')
        text = check_text(line)
        yield filename, text

    def reducer(self, filename, text):
        yield filename, ' '.join(text).strip()

if __name__ == '__main__':
    MRExtractSub.run()

