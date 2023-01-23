import matplotlib.pyplot as plt

def plot_frequencies(inputs, aircraft_matrix):
    """ This function plots the aircraft frequencies
    :param inputs: Contains the list of list with the inputs required to define
        the problem
    :param aircraft_matrix: aircraft frequencies matrix
    :return
        plot of frequencies
    """
    airports_number = len(inputs.list_excel_df[0])

    fig, ax1 = plt.subplots()
    im = ax1.imshow(aircraft_matrix)
    im.set_clim(0, 10)
    fig.colorbar(im,orientation="vertical", pad=0.2)
    # We want to show all ticks...
    # ax1.set_xticks(np.arange(len(arrival_airports)))
    # ax1.set_yticks(np.arange(len(departure_airports)))
    # ... and label them with the respective list entries
    # ax1.set_xticklabels(arrival_airports)
    # ax1.set_yticklabels(departure_airports)

    # Loop over data dimensions and create text annotations.
    for i in range(airports_number):
        for j in range(airports_number):
            text = ax1.text(j, i, aircraft_matrix[i, j],
                            ha="center", va="center", color="w")

    ax1.xaxis.set_ticks_position('top')

    # ax.set_title("Network frequencies for optimum aircraft (112 seats)")
    fig.tight_layout()
    plt.show()
