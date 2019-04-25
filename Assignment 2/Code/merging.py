import glob
import pandas as pd
import os

path = os.getcwd()+"/Assignment 2/Data/Merge" # use your path
allFiles = glob.glob(path + "/*.csv")

list_ = []

for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)

frame = pd.concat(list_, axis = 0, ignore_index = True)
frame.to_csv(os.getcwd()+"/Assignment 2/Data/final_file.csv",index=False, encoding='utf8')
