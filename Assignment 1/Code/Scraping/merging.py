import glob
path =r'../Assignment 1/Data/Generated/By Algorithms/final_files' # use your path
allFiles = glob.glob(path + "/*.csv")

list_ = []

for file_ in allFiles:
    df = pd.read_csv(file_,index_col=None, header=0)
    list_.append(df)

frame = pd.concat(list_, axis = 0, ignore_index = True)
frame.to_csv("../Assignment 1/Data/Generated/By Algorithms/NT_Scraped.csv",index=False, encoding='utf8')
