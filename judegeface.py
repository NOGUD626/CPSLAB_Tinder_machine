import cv2
import glob
import numpy as np
import os
from sklearn import svm
from sklearn.externals import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
#顔判別器の作成
images = []
labels = []

def Picture_Processing(fileList,label):
    global images
    global labels
    dirpath = os.path.dirname(os.path.abspath(__file__))
    for i,f in enumerate(fileList):
        img = cv2.imread(f)
        img = cv2.resize(img,(640,800))
        img_data = img.reshape(-1,) # 一次元に展開
        images.append(img_data)
        labels.append (str(label))
    
def ConvertNumpy():
    global images
    global labels
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.3, train_size=0.4,shuffle=True)
    #svmの変換器を作成
    clf = svm.LinearSVC()
    #学習
#    clf.fit(images,labels)
    clf.fit(X_train,y_train)
    #学習モデルを保存する
    joblib.dump(clf, 'clf.pkl')
    print("モデル保管完了")
    # トレーニングデータに対する精度
    pred_train = clf.predict(X_test)
    accuracy_train = accuracy_score(y_test, pred_train)
    print('トレーニングデータに対する正解率： %.2f' % accuracy_train)

def DoPlan():
    global images
    global labels
    dirpath = os.path.dirname(os.path.abspath(__file__))
    fileList = glob.glob("{0}/分別/あんまり/*.jpg".format(dirpath))[:500]
    Picture_Processing(fileList,'No')
    print('1:finish')
    fileList = glob.glob("{0}/分別/可愛い/*.jpg".format(dirpath))[:500]
    Picture_Processing(fileList,'Yes')
    print('2:finish')
    ConvertNumpy()

def Dopredict():
    # 予測モデルを復元
    clf = joblib.load('clf.pkl')
    dirpath = os.path.dirname(os.path.abspath(__file__))
    fileList = glob.glob("{0}/分別/整形/*.jpg".format(dirpath))
    for i,f in enumerate(fileList):
        img = cv2.imread(f)
        img_d = cv2.resize(img,(213,266))
        img_data = img_d.reshape(1,-1) # 一次元に展開
        # 予測結果を出力
        result = clf.predict(img_data)
        if(result == 'Yes'):
            cv2.imwrite("{0}/分別/結果/output_{1}.png".format(dirpath,i), img)
    
if __name__ == "__main__":
    DoPlan()
#    Dopredict()