from IPython.core.debugger import Tracer
import random
import string
import time, re
import os
class LetterHMM:
    def __init__(self, texts, N):
        # text = text.lower()
        # text = text.translate(string.maketrans("",""), string.punctuation)
        text = " ".join(texts)
        words = text.split()
        cleanedWords = [word.strip() for word in words if len(word) != 0]
        text = " ".join(cleanedWords)
        del cleanedWords




        transition_dict = {}
        phrases = set()
        for index in xrange(len(text)-N-1):
            phrase = text[index:index+N]
            phrases.add(phrase)
            if not phrase in transition_dict:
                transition_dict[phrase] = {}
                transition_dict[phrase]['total'] = 0
                transition_dict[phrase]['table'] = {}

            next = text[index + N]
            if not next in transition_dict[phrase]['table']:
                transition_dict[phrase]['table'][next] = 1
            else:
                transition_dict[phrase]['table'][next] += 1
            transition_dict[phrase]['total'] += 1

        self.word_distros = []
        for contents in texts:
            word_distro = {}
            contents = contents.lower()
            contents = contents.translate(string.maketrans("",""), string.punctuation)
            for word in contents.split():
                if not word in word_distro:
                    word_distro[word] = 1
                else:
                    word_distro[word] += 1
            self.word_distros.append(word_distro)
        self.N = N
        self.transition_dict = transition_dict
        self.phrases = phrases

    def randomwalk(self, length):
        sentence = ""
        seed = random.sample(self.phrases,1)[0]
        sentence += seed

        for i in xrange(length - self.N):
            if not seed in self.transition_dict:
                return sentence
            next = self.sampleFromTable(self.transition_dict[seed])
            sentence += next
            seed = seed[1:] + next
        return sentence



    def sampleFromTable(self, table):
        trans_table = []
        total = table['total']
        summ = 0.0
        for i in table['table']:
            summ += float(table['table'][i])/total
            trans_table.append((i, summ))
        randnum = random.random()
        for j in xrange(len(trans_table)):
            if randnum < trans_table[j][1]:
                return trans_table[j][0]
        print "error"




hmm = None
def readAndProcess(path):
    text = ""
    with open(path,'rb') as contents:
        text = contents.read()
    text = re.sub("\^\d{1,}","", text)
    text = re.sub("\*\*\*[^\*]{1,}\*\*\*"," ", text)
    text = re.sub("-{3,}"," ", text)
    text = re.sub("(\w)- (\w)","\1\2", text)
    text = re.sub("[A-Z]{5,}"," ", text)
    return text

def main():
    global hmm
    Tracer()()
    pwd = os.getcwd()
    basepath = pwd+"/corpora/"
    # Name of text files in /corpora/ directory
    paths = ("ai.txt", "mahabharat.txt")
    paths = tuple([basepath+path for path in paths])

    texts = [readAndProcess(path) for path in paths]
    N = 10
    hmm = LetterHMM(texts, N)
    Tracer()()
    while True:
        sample = hmm.randomwalk(2000)
        # print sample
        # print "\n"
        obj = re.findall("[A-Z][A-Za-z:\- ,;]{19,}\.", sample)
        if len(obj) < 1:
            continue
        for sentence in obj:
            sentence.translate(string.maketrans("",""), string.punctuation).lower()
            counts = [0,0,0,0]
            for word in sentence.split():
                if word in hmm.word_distros[0] and word in hmm.word_distros[1]:
                    counts[2] += 1
                elif word in hmm.word_distros[0]:
                    counts[0] += 1
                elif word in hmm.word_distros[1]:
                    counts[1] += 1
                else:
                    counts[3] += 1
            if counts[0] >= 2 and counts[1] >= 2:
                print sentence
                print counts
                print "\n"
        time.sleep(1)


if __name__ == "__main__":
    main()




