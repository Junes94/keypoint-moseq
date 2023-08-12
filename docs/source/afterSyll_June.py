import sys
sys.path.insert(0, 'C:/Users/MyPC/Desktop/git/AVATAR_motionMap')
import FileManager.csvload as acl
sys.path.insert(0, 'C:/Users/MyPC/Desktop/git/kp_moseq/keypoint-moseq/project')
import SDSBD_trainset2.params as params
import matplotlib.pyplot as plt
import copy
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib
import time
from datetime import date
import os
import keypoint_moseq as kpms
import keypoint_moseq .analysis as kpmsa
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.model_selection import permutation_test_score
from sklearn.metrics import accuracy_score
preSD_extrR = params.preSD_extrR
preSD_extrS = params.preSD_extrS
postSD_extrR = params.postSD_extrR
postSD_extrS = params.postSD_extrS
postSD_defeated = params.postSD_defeated
postSD_control = params.postSD_control

# parameters setting
start = params.start    # analysis start frame of the video
end = params.end        # analysis end frame of the video
syllable_analyzed = 10 #params.core_syllable_num
filelist_group1 = acl.get_csv_paths(params.postSD_defeated)    #[]
filelist_group2 = acl.get_csv_paths(params.postSD_control)
dataset = filelist_group1 + filelist_group2
dataset_class = [0]*len(filelist_group1) + [1]*len(filelist_group2)
if len(dataset) != len(dataset_class):
    print('Error: dataset and dataset_class should have the same length')
    sys.exit()


# read "sylable reindexed" column from each csv file and store it in a dictionary
data_moseq = {}  # Initialize an empty dictionary
for file, group in zip(dataset, dataset_class):
    file_name = os.path.splitext(os.path.basename(file))[0]
    data_moseq[file_name] = {}  # Create a new dictionary for each file with the file as the key
    data_moseq[file_name]['class'] = group  # Store the class of the file in the dictionary
    
    # Read the csv file
    df = pd.read_csv(file)
    df = df[start:end]
    
    # Convert the 'syllables reindexed' column to a numpy array, wrap it in a list, and store it in the dictionary
    data_moseq[file_name]['syllables reindexed'] = [df['syllables reindexed'].to_numpy(dtype=int)]
    frequencies, durations = kpmsa.get_syllable_statistics(data_moseq[file_name]['syllables reindexed'], max_syllable=100, count='frequency')

    # Calculate the relative frequencies
    total_frequency = sum(frequencies.values())
    relative_frequencies = {k: v / total_frequency for k, v in frequencies.items()}
    relative_frequencies = {key: value for key, value in relative_frequencies.items() if key in range(syllable_analyzed)}

    # Store relative frequencies in the dictionary
    data_moseq[file_name]['syllables relative frequency'] = relative_frequencies
    data_moseq[file_name]['syllables durations'] = durations

# Prepare data
X = []  # Features
y = []  # Response
for file_name, data in data_moseq.items():
    relative_frequency_values = list(data['syllables relative frequency'].values())
    X.append(relative_frequency_values)
    response_value = data['class']
    y.append(response_value)
X = np.array(X) # Convert to NumPy arrays
y = np.array(y)

# train and evaluate a model using repeated k-fold cross-validation
qda = QuadraticDiscriminantAnalysis()   # 분석기 초기화
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=1000, random_state=42)   # Repeated Stratified K-Fold 객체 생성

scores = [] # 결과 저장을 위한 리스트

# 교차 검증 수행
for train_index, test_index in cv.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    qda.fit(X_train, y_train) # 모델 훈련
    predictions = qda.predict(X_test) # 예측
    score = accuracy_score(y_test, predictions) # 정확도 계산
    scores.append(score)

# 평균 정확도 출력
print("Average accuracy: ", np.mean(scores))

# 분석기 초기화
qda = QuadraticDiscriminantAnalysis()

# 순열 테스트 수행
original_score, permutation_scores, pvalue = permutation_test_score(qda, X, y, scoring="accuracy", cv=cv, n_permutations=1000, n_jobs=1)

# 결과 출력
print("Model score: %s" % original_score)
print("Permutation scores: %s" % permutation_scores)
print("Permutation test p-value: %s" % pvalue)

fig, ax = plt.subplots()

ax.hist(permutation_scores, bins=20, density=True)
ax.axvline(original_score, ls="--", color="r")
score_label = f"Score on original\ndata: {original_score:.2f}\n(p-value: {pvalue:.3f})"
ax.text(0.7, 10, score_label, fontsize=12)
ax.set_xlabel("Accuracy score")
_ = ax.set_ylabel("Probability density")
plt.show()
