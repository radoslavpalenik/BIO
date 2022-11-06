import cv2

from matplotlib import pyplot as plt

def plot_borders(image):

    
    plt.plot(1290,2025, marker='+', color="orange")
    plt.plot(1500,2150, marker='+', color="orange")
    plt.plot(25,2650, marker='+', color="orange")
    plt.plot(550,2990, marker='+', color="orange")

    plt.plot(1290,1775, marker='+', color="cyan")
    plt.plot(1510,1930, marker='+', color="cyan")
    plt.plot(25,1815, marker='+', color="cyan")
    plt.plot(25,2550, marker='+', color="cyan")

    plt.plot(1400,1500, marker='+', color="yellow")
    plt.plot(1510,1750, marker='+', color="yellow")
    plt.plot(25,1835, marker='+', color="yellow")
    plt.plot(25,1200, marker='+', color="yellow")

    plt.plot(830,200, marker='+', color="red")
    plt.plot(1825,1180, marker='+', color="red")
    plt.plot(1600,1550, marker='+', color="red")
    plt.plot(320,650, marker='+', color="red")

    plt.plot(1500,25, marker='+', color="lime")
    plt.plot(2500,25, marker='+', color="lime")
    plt.plot(1905,1330, marker='+', color="lime")
    plt.plot(2230,1330, marker='+', color="lime")

    plt.plot(2270,1250, marker='+', color="salmon")
    plt.plot(2500,1530, marker='+', color="salmon")
    plt.plot(2875,25, marker='+', color="salmon")
    plt.plot(3685,780, marker='+', color="salmon")

    plt.plot(2750,1450, marker='+', color="violet")
    plt.plot(2650,1720, marker='+', color="violet")
    plt.plot(4050,1200, marker='+', color="violet")
    plt.plot(4050,1720, marker='+', color="violet")

    plt.plot(2900,1750, marker='+', color="navy")
    plt.plot(2650,1930, marker='+', color="navy")
    plt.plot(4050,1800, marker='+', color="navy")
    plt.plot(4050,2400, marker='+', color="navy")

    plt.plot(2750,2000, marker='+', color="blue")
    plt.plot(2650,2150, marker='+', color="blue")
    plt.plot(4050,2650, marker='+', color="blue")
    plt.plot(3700,2990, marker='+', color="blue")

    plt.plot(1400,2990, marker='+', color="green")
    plt.plot(2600,2990, marker='+', color="green")
    plt.plot(1800,2000, marker='+', color="green")
    plt.plot(2300,2000, marker='+', color="green")


    plt.imshow(image)
    plt.show()