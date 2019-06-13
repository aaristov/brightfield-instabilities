from matplotlib import pyplot as plt

def multi_imshow(*img2d, titles=None, figsize=(8,3)):
    '''
    Plots all 2D arrays in a row
    '''
    num_img = len(img2d)
    fig = plt.figure(figsize=figsize)
    for i, p in enumerate(img2d):
        fig.add_subplot(100 + num_img * 10 + i + 1)
        if titles:
            plt.title(titles[i])
        plt.imshow(p)
    plt.show()