import pickle

levels = {1: [["ttttttttt","         "],
                           ["t       t","         "],
                           ["t       t","         "],
                           ["t       t","         "],
                           ["t       t","         "],
                           ["t 4 =3+1t","  1 0000 "],
                           ["ttttttttt","         "]],

                       2: [["ttttttttttt","          "],
                           ["t         t","          "],
                           ["t         t","          "],
                           ["t         t","          "],
                           ["t         t","          "],
                           ["t 3x4=1 2 t","  00000 3 "],
                           ["ttttttttttt","          "]],

                       3: [["ttttttttt","         "],
                           ["t       t","         "],
                           ["t       t","         "],
                           ["t       t","      0  "],
                           ["t  2    t","   0  0  "],
                           ["t  = x2 t","   0 00  "],
                           ["ttttttttt","         "]]}

with open('levels.txt', 'wb') as f:
    pickle.dump(levels, f)
f.close()