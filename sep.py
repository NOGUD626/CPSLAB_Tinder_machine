import json
import glob
import ast
import requests
imageTotal = []
fileList = glob.glob("./user/*.json")
num = 0
for i in fileList:
    print(i)
    with open('{0}'.format(i)) as f:
        df = json.load(f)
        dic = ast.literal_eval(df)
        imageTotal.extend(dic['imageLIST'])
        num = num + int(len(dic['imageLIST']))

SET = set(imageTotal)
print(num,len(SET))
for url in list(SET):
    if len(url) == 0:
        continue
    response = requests.get(url)
    image = response.content
    fileName = url.split('/')[-1]
    with open("./images/{0}".format(fileName), "wb") as aaa:
        aaa.write(image)