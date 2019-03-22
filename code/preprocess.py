import json
import spacy
import random
import os
import copy

def hltag(data):
    U = set(['just', 'being', 'able', 'over', 'mainly', 'still', 'yet', 'seemed', 'whose', 'based', 'also', 'writer', 'had', 'should', 'to', 'sometimesd', 'has', 'might', 'then', 'very', 'ones', 'whether', 'not', 'during', 'now', 'realize', 'did', 'this', 't', 'each', 'where', 'because', 'doing', 'some', 'likely', 'are', 'further', 'really', 'even', 'what', 'said', 'for', 'lots', 'since', 'please', 'does', 'between', 'probably', 'ever', 'either', 'available', 'be', 'recently', 'however', 'here', 'although', 'by', 'both', 'about', 'anything', 'of', 'could', 'title', 'according', 's', 'or', 'among', 'already', 'suddenly', 'seems', 'simply', 'passage', 'from', 'would', 'whom', 'there', 'been', 'few', 'too', 'was', 'until', 'that', 'but', 'else', 'with', 'than', 'those', 'must', 'showed', 'these', 'will', 'while', 'can', 'were', 'following', 'and', 'do', 'almost', 'is', 'it', 'an', 'as', 'at', 'have', 'seem', 'if', 'again', 'author', 'rather', 'when', 'how', 'other', 'which', 'instead', 'several', 'though', 'may', 'who', 'most', 'such', 'why', 'recent', 'a', 'don', 'especially', 'maybe', 'perhaps', 'so', 'the', 'having', 'nearly'])
    nlp = spacy.load('en')
    salientPosList = ['NN', 'NNP', 'NNPS', 'NNS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS', 'RB',
                      'RBR', 'RBS', 'CD', 'FW']  # 21 core pos tag
    output = []
    for i in range(len(data)):
        article = nlp(' '.join(data[i][0]))
        for j in range(len(data[i][1])):
            d = copy.deepcopy(data[i])
            d[0] = []
            question = nlp(data[i][1][j]["question"])
            for k in range(len(data[i][1][j]["choice"])):
                key = set()
                for token in question:
                    if token.tag_ in salientPosList and token.text.lower() not in U:
                        key.add(token.text.lower())
                choice = nlp(data[i][1][j]["choice"][k])
                for token in choice:
                    if token.tag_ in salientPosList:
                        key.add(token.text.lower())
                articleatt = []
                for token in article:
                    if token.tag_ in salientPosList and token.text.lower() in key:
                        articleatt += ['[[HL]]']
                        articleatt += [token.text]
                        articleatt += ['[[/HL]]']
                    else:
                        articleatt += [token.text]
                d[0] += [' '.join(articleatt)]
            d[1] = [data[i][1][j]]
            output += [d]
    return output
    
def preprocess():
    for f1 in ["train", "dev", "test"]:
        output = []
        for f2 in ["high", "middle"]:
            fl = os.listdir("./data/RACE/"+f1+"/"+f2)
            for fn in fl:
                with open("./data/RACE/"+f1+"/"+f2+"/"+fn, "r") as f:
                    data = json.load(f)
                    d = [[data["article"]],[],f1+"/"+f2+"/"+fn]
                    for i in range(len(data["questions"])):
                        q = {}
                        q["question"] = data["questions"][i]
                        q["choice"] = []
                        for j in range(len(data["options"][i])):
                            q["choice"] += [data["options"][i][j]]
                        q["answer"] = q["choice"][ord(data["answers"][i]) - ord("A")]
                        d[1] += [q]
                    output += [d]
        print(f1, len(output))
        
        output = hltag(output)

        print(f1, len(output))
        
        with open("./data/race_" + f1 + ".json", "w") as f:
            json.dump(output, f, indent=2)


if __name__ == '__main__':
    preprocess()
