import csv
import time
import matplotlib.pyplot as plt
import numpy as np

#################### 기존 파일들 삭제#############################
import os

def delete_file():
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

def openCSVfile():
    sample_list = []
    with open(f"record_{file_i}.csv", 'r', newline=''):
        #파일 열어서 데이터 저장
        sample_list = np.genfromtxt(f"record_{file_i}.csv", delimiter=',')
    return  sample_list

def draw_graph():
    for i in range(ntime):
        if(len(plt_x)== 30*input_x_size):###############################################
            del plt_x[:input_x_size]
            del plt_y[:input_x_size]
        plt_x.extend(time_list[(i)*input_x_size:(i+1)*input_x_size])
        line.set_xdata(plt_x)
        plt_y.extend(sample_list[(i)*input_x_size:(i+1)*input_x_size])
        line.set_ydata(plt_y)

        ax0.relim()
        ax0.autoscale_view()

        plt.draw()
        plt.pause(1/ntime) ###############################################

if __name__ == "__main__":
    delete_file()

    nSamples = 10000 ############################################################
    n_time_save = 10 ############################################################
    input_x_size = 1000

    file_i = 0
    plt_x = []
    plt_y = []
    
    
    ntime = int(nSamples / input_x_size)
    fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(15, 8))
    line, = ax0.plot(plt_x,plt_y)
    time_list = []
    while(file_i<n_time_save):
        try:
            sample_list = openCSVfile()
            time_list = [i for i in range(file_i*nSamples,(file_i+1)*nSamples,1)]
            draw_graph()
            file_i += 1
        except FileNotFoundError:
            #pass
            # 파일이 아직 생성되지 않았으면 대기
            print("파일이 아직 생성되지 않았습니다. 대기 중...",file_i)
            time.sleep(0.2)  # 1초 대기 후 다시 시도
    time.sleep(3)  