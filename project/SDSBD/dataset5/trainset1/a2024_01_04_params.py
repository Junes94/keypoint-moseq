## General
project_name = 'SDSBD'
dataset_name = 'dataset5'
core_syllables = list(range(25)) + [28]
fs = 20   # sampling rate of the video data
total_rec_duration = 10*60  # (seconds) total recording duration of the video data
start = round(fs * 5)  # start frame to be analyzed
end = round(fs * total_rec_duration - fs * 5)  # end frame to be analyzed

## (git\kp-moseq) results directory
TRAINED_MODEL_DIR = r"C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD\dataset5\trainset1\2024_01_04-13_41_21"
RESULT_DIR = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD\dataset5\trainset1\2024_01_04-13_41_21\results' # directory where results(syllables) from kp-moseq are saved

## file list of each group
preSD = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD\dataset5\trainset1\2024_01_04-13_41_21\results\preSD.txt'
preSD_resilient = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD\dataset5\trainset1\2024_01_04-13_41_21\results\preSD_resilient.txt'# group of resilient
preSD_susceptible = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD\dataset5\trainset1\2024_01_04-13_41_21\results\preSD_susceptible.txt'# group of susceptible
preSD_defeated = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD\dataset5\trainset1\2024_01_04-13_41_21\results\preSD_defeated.txt'# group of defeated
preSD_control = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD\dataset5\trainset1\2024_01_04-13_41_21\results\preSD_control.txt'# group of control

# postSD = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD_trainset2\2023_07_26-dataset2_testset2\results\postSD.txt'
# postSD_extrR = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD_trainset2\2023_07_26-dataset2_testset2\results\postSD_extrR.txt'# group of extreme resilience
# postSD_extrS = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD_trainset2\2023_07_26-dataset2_testset2\results\postSD_extrS.txt'# group of extreme susceptible
# postSD_defeated = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD_trainset2\2023_07_26-dataset2_testset2\results\postSD_defeated.txt'# group of defeated
# postSD_control = r'C:\Users\MyPC\Desktop\git\kp_moseq\keypoint-moseq\project\SDSBD_trainset2\2023_07_26-dataset2_testset2\results\postSD_control.txt'# group of control