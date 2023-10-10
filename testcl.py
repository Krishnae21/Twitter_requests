from copy import copy

data = input()
dataLower = data.lower().replace(" ", ".").replace(",", ".")




tempData = copy(dataLower).lower()
tempData = list(tempData)
countWords = input()
lisWords = []
for i in range(int(countWords)):
    lisWords.append(input().lower())

while (True):
    countFind = 0

    for word in lisWords:
        wordF = dataLower.find(word)
        if (wordF != -1):
            countFind+= 1
            for i in range(len(word)):
                x = wordF + i
                tempData[x] = '.'
    dataLower = ''.join(tempData)
    if countFind == 0:
        break

for i in range(len(tempData)):
    if (tempData[i] != '.'):
        tempData[i] = '~'
print(data)
print(''.join(tempData))