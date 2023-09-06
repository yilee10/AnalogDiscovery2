import csv
import time
import matplotlib.pyplot as plt
import numpy as np

#################### 기존 파일들 삭제#############################
import os
file_list = os.listdir()

# ".csv"로 끝나는 파일 모두 삭제
for file_name in file_list:
    if file_name.startswith("record") and file_name.endswith(".csv"):
        try:
            os.remove(file_name)
            print(f"{file_name} 파일이 삭제되었습니다.")
        except Exception as e:
            print(f"파일 삭제 중 오류 발생: {e}")
           
#################### 기존 파일들 삭제#############################

n_time_save = 2

i = 0
while (i < n_time_save):
    try:
        sample_list = []
        time_list = []
        with open(f"record_{i}.csv", 'r', newline=''):
            #파일 열어서 데이터 저장
            sample_list = np.genfromtxt(f"record_{i}.csv", delimiter=',')
            cnt = 0
            for row in sample_list:
                time_list.append(cnt)
                cnt += 1
            print("sample_list")
            print(len(sample_list))
            #그래프 그리기
            plt.ion()
            fig, (ax0) = plt.subplots(nrows=1, ncols=1,figsize=(15, 8))
            line, = ax0.plot(sample_list,time_list)

            line.set_xdata(time_list)
            line.set_ydata(sample_list)
                
            ax0.relim()
            ax0.autoscale_view()

            plt.show() 
            plt.pause(1)
            plt.close()

            i += 1  # 다음 파일
    except FileNotFoundError:
        #pass
        # 파일이 아직 생성되지 않았으면 대기
        print("파일이 아직 생성되지 않았습니다. 대기 중...")
        time.sleep(1)  # 1초 대기 후 다시 시도