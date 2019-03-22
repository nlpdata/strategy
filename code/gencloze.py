import random
import nltk
import os.path, os
from nltk.tokenize import sent_tokenize
import json
from preprocess import hltag
from shutil import copyfile

def read_race(fns):
    article = []
    for f1 in fns:
        for f2 in ["high", "middle"]:
            fl = os.listdir("./data/RACE/" + f1 + "/" + f2)
            for fn in fl:
                with open("./data/RACE/" + f1 + "/" + f2 + "/" + fn, "r") as f:
                    article += [json.load(f)["article"]]
    return article

def problem_gen(article, id):
    delimiter = '_[[#@]]_'
    def get_cloze(sentence, words):
        cloze = []
        ans = []
        dis = []
        sentences = sentence.split(delimiter)
        tokens = []
        for i in range(len(sentences)):
            tokens += [x for x in nltk.word_tokenize(sentences[i])]
            if i != len(sentences) - 1:
                tokens += ['_[[#@]]_']
        if len(tokens) > 50:
            return None
        used = set()
        n_cloze = min((len(tokens)-2) // 6, 4)
        if n_cloze <= 0:
            if len(tokens) >= 6:
                n_cloze = 1
        if n_cloze <= 0:
            return None
        n_cloze = random.randint(1, n_cloze)
        for i in range(n_cloze):
            while True:
                cloze_len = random.randint(1, 4)
                left = random.randint(0, len(tokens)-cloze_len)
                ok = True
                for j in range(left, left+cloze_len):
                    if j in used:
                        ok = False
                        break
                if not ok:
                    continue
                for j in range(left, left+cloze_len):
                    used.add(j)
                for j in range(left, left+cloze_len):
                    if not tokens[j].isalpha():
                        ok = False
                if ok:
                    cloze += [[left, left+cloze_len]]
                    ans += [' '.join(tokens[left:left+cloze_len])]
                break
        if len(ans) == 0:
            return None
        for i in range(len(ans)):
            dislen = max(1, random.randint(len(ans[i].split()) - 1, len(ans[i].split()) + 1))
            dislis = []
            for j in range(3):
                while True:
                    start = random.randint(0, len(words)-dislen)
                    d = ' '.join(words[start:start+dislen])
                    if d != ' '.join(ans[i]) and d not in dislis:
                        dislis += [d]
                        break
            dis += [dislis]
            for j in range(cloze[i][0], cloze[i][1]):
                tokens[j] = ''
            tokens[cloze[i][0]] = '_'
        for i in range(len(cloze)):
            for j in range(i+1, len(cloze)):
                if cloze[i][0] > cloze[j][0]:
                    cloze[i], cloze[j] = cloze[j], cloze[i]
                    ans[i], ans[j] = ans[j], ans[i]
                    dis[i], dis[j] = dis[j], dis[i]
        usedmask = set()
        for i in range(3):
            masklen = random.randint(0, max(0, len(cloze)-1))
            if masklen == 0:
                continue
            mask = [j for j in range(len(cloze)) if j not in usedmask]
            random.shuffle(mask)
            mask = mask[:masklen]
            mask.sort()
            for j in mask:
                dis[j][i] = ans[j]
                usedmask.add(j)
        ret = [' '.join((' '.join(tokens).split())), ', '.join(ans)]
        for i in range(3):
            ret +=  [', '.join([x[i] for x in dis])]
        return ret

    d = [[], [], id]
    article.replace(delimiter, '')
    sentences_raw = [x for x in sent_tokenize(article)]
    sentences = [[sentences_raw[i], i] for i in range(len(sentences_raw))]
    words = [x for x in nltk.word_tokenize(article) if x.isalpha()]

    n_problem = min(10, len(words) // 30)
    for i in range(n_problem):
        random.shuffle(sentences)
        selected = sentences[0:random.randint(1, 3)]
        selected = [x[0] for x in selected]
        question = get_cloze(delimiter.join(selected), words)
        if question is not None:
            q = {}
            q["question"] = ' '.join(question[0].replace(delimiter, '').split())
            ok = True
            for j in range(len(d[1])):
                if d[1][j]["question"] == q["question"]:
                    ok = False
                    break
            if not ok:
                continue
            q["choice"] = question[1:]
            if len(set(q["choice"])) != 4:
                continue
            random.shuffle(q["choice"])
            q["answer"] = question[1]

            d[1] += [q]
    sentences.sort(key = lambda x : x[1])
    sentences = [x[0] for x in sentences]
    d[0] += [' '.join(sentences)]
    return d

if __name__ == '__main__':
    for fn in ["train", "dev"]:
        output = []
        cnt = 0
        data = read_race([fn])        
        for i in range(len(data)):
            output += [problem_gen(data[i], str(i))]
            cnt += len(output[i][1])
        print(fn, len(output), cnt)
        output = hltag(output)
        print(fn, len(output))
        os.makedirs("cloze", exist_ok=True)
        with open("./cloze/race_" + fn + ".json", "w", encoding='utf8') as f:
            json.dump(output, f, indent=2)
    copyfile("./cloze/race_dev.json", "./cloze/race_test.json")
        
