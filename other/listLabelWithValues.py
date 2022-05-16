import pandas as pd

dataRaw = pd.read_csv('./data/dataset.csv')
dataPre = pd.read_csv('./data/pre-dataset.csv')

ROW = 'Crop'

# f = open('./district-name-state-wise.txt', 'a')

result = set()

print(dataRaw[ROW][0])

# for i in dataRaw[ROW]:
#     for j in dataPre[ROW]:
#         # print(i,j)
#         result.add((i,j))

for i in range(0, len(dataRaw[ROW])):
    result.add((dataPre[ROW][i], dataRaw[ROW][i]))


print(ROW)
# print(result)

sorted_result = sorted(result)

for val in sorted_result:
    print(val)
#     f.write(str(val)+ '\n')
