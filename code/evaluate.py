import json

def evaluate(fns):
    result = []

    with open("data/race_test.json", "r") as f:
        data = json.load(f)
    
    def getresult(fn):
        result = []
        with open(fn, "r") as f:
            l = f.readline()
            while l:
                l = l.strip().split()
                for i in range(len(l)):
                    l[i] = float(l[i])
                result += [l]
                l = f.readline()
        return result
    results = []

    for fn in fns:
        results += [getresult(fn)]
    
    result = []
    for i in range(len(results[0])):
        result += [[0] * len(results[0][0])]

    for i in range(len(results)):
        for j in range(len(results[i])):
            for k in range(len(results[i][j])):
                result[j][k] += results[i][j][k]
                
    for i in range(len(result)):
        best = 0
        for j in range(1, len(result[i])):
            if result[i][j] > result[i][best]:
                best = j
        result[i] = best

    k = 0
    acc, all = 0, 0
    for i in range(len(data)):
        for j in range(len(data[i][1])):
            all += 1
            if data[i][1][j]["choice"][result[k]] == data[i][1][j]["answer"]:
                acc += 1
            k += 1

    print('accuracy =', 0 if all == 0 else float(acc)/all)

if __name__ == '__main__':
    print("original order:")
    evaluate(["submission/pred_test_logits.txt"])
    print("reverse order:")
    evaluate(["submission_oqd/pred_test_logits.txt"])
    print("ensemble:")
    evaluate(["submission/pred_test_logits.txt", "submission_oqd/pred_test_logits.txt"])
