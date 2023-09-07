import matplotlib.pyplot as plt

# 그래프 그리기
def draw_graph(ntime,sample_list,plt_x,plt_y):
    for i in range(ntime):
        if(len(plt_x)== 50):
            del plt_x[:input_x_size]
            del plt_y[:input_x_size]
        plt_x.extend( sample_list[(i)*input_x_size:(i+1)*input_x_size])
        line.set_xdata(plt_x)
        plt_y.extend( sample_list[(i)*input_x_size:(i+1)*input_x_size])
        line.set_ydata(plt_y)
        print(plt_x)

        ax0.relim()
        ax0.autoscale_view()

        plt.draw()
        plt.pause(1)

if __name__ == "__main__":
    nSamples = 100

    plt_x = []
    plt_y = []
    input_x_size = 10
    ntime = int(nSamples / input_x_size)
    fig, ax0 = plt.subplots(nrows=1, ncols=1, figsize=(15, 8))
    line, = ax0.plot(plt_x,plt_y)

    for i in range(2):
        sample_list = [i for i in range(i*nSamples,(i+1)*nSamples,1)]
        draw_graph(ntime,sample_list,plt_x,plt_y)