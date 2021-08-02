import numpy as np
import pandas as pd
import argparse

def levenshtein(w1, w2):
    # 1. initialize distance matrix
    distances = np.zeros((len(w1) + 1, len(w2) + 1))

    # 2. set first row and first column values
    distances[0,:] = np.arange(0, len(w2) + 1)
    distances[:,0] = np.arange(0, len(w1) + 1)

    # 3. start iteration
    for i in range(1, len(w1) + 1):
        for j in range(1, len(w2) + 1):
            # 3.1. select surrounding cells
            left = distances[i, j-1]
            diag = distances[i-1, j-1]
            top  = distances[i-1, j]
            
            # 3.2. apply conditions
            if (w1[i-1] == w2[j-1]):
                distances[i, j] = diag
            else:
                distances[i, j] = min([left, diag, top]) + 1
    # 4. return levenshtein distance
    return int(distances[-1, -1])


def main(opt):
    # read data and store in dataframe
    data = pd.read_csv(opt.data_path, header=0, sep=',')
    # calculate distance to reference (Luca) for each dog name
    data['distance'] = data.apply(lambda dog: levenshtein(dog.HUNDENAME, opt.name), axis=1)

    res = data[data.distance == 1]

    res.to_csv('data/result.csv', header=True, sep=',', index=False)

    file_ = open(r"data/names.txt","w")
    file_.writelines('\n'.join(list(res.HUNDENAME.unique())))
    file_.close()



if __name__ == '__main__':
    # Hyper Parameters
    parser = argparse.ArgumentParser()

    parser.add_argument('--name', default='Luca',
                        help='reference name to be compared against')

    parser.add_argument('--data_path', default='./data/20210103_hundenamen.csv',
                        help='csv file containing dog names')

    opt = parser.parse_args()

    main(opt)