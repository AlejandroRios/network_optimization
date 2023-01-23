import numpy as np

def list_to_matrix(list,size):
    """This function convert a list (without i=j) of parameters
    to the matrix form (including i=j)
    Example: if the network considers 5 airports the input list
    has len = 20. The output matrix will be size(5,5)
    :param list: list of variables to be converted to matrix form
    :param size: value of the size of the matrix
    :return
        marix: array containing the output matrix size(size,size)
    """
    matrix = np.zeros((size,size))

    list_size = size**2 - size
    idx = 0
    while idx<list_size/2:
        for i in range(size):
            for j in range(size):
                if j>i:
                    matrix[i][j] = list[idx]
                    idx = idx+1
    while idx<list_size:
        for i in range(size):
            for j in range(size):
                if j<i:
                    matrix[i][j] = list[idx]
                    idx = idx+1
    return matrix

def matrix_to_list(matrix, size):
    """This function convert a matrix (including i=j) to a list
    (without i=j)
    :param marix: array containing the input matrix size(size,size)
    :param size: value of the size of the matrix
    :return
        list: list of variables from the matrix
    """
    list = []
    for i in range(size):
        for j in range(size):
            if i != j and i < j:
                list.append(matrix[i][j])
    for i in range(size):
        for j in range(size):
            if i != j and i > j:
                list.append(matrix[i][j])

    return list

def restructure_data(aux_mat,n):
    """
    :param
    :return
    """

    aux_mat = np.reshape(aux_mat, (n,n-1))
    new_mat = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i == j:
                new_mat[i][j] = 0
            elif j<=i:
                new_mat[i][j] = aux_mat[i][j]
            else:
                new_mat[i][j] = aux_mat[i][j-1]
    return new_mat

def passenger_load(list_flow, airports_number, inputs):
    """This function evaluate the aircraft load percentage and split it
    into a list with full loadaded and non-full loaded aircraft. It returns
    the distribution of loads in matrix a list form
    :param list_flow: flow of passenger list
    :param airports_number: number of airports whitin the network
    :param inputs: aircraft inputs
    :return
       full_acft: matrix of aircraft full loaded
       frac_acft: matrix of aircraft non-full loaded
       full_acft_list: list of aircraft full loaded
       frac_acft_list: list of aircraft non-full loaded
    """
    aircraft_info = inputs.list_excel_df[3].T.to_dict()
    acft_number = len(aircraft_info)
    payload = np.array(inputs.list_inputs[5])
    passenger_weight = int(inputs.list_excel_df[3]['passenger_weight'][0]) 

    print(payload)
    print(passenger_weight)
    # capacity = [int(x / passenger_weight) for x in payload[0]]
    capacity = []
    for i in range(acft_number):
        print(i)
        aux = [int(x / passenger_weight) for x in payload[i]]
        capacity.append(aux)
    flow_matrix = list_to_matrix(list_flow,airports_number)
    
    capacity_matrix = []
    fraction = []
    full_acft_matrix = []
    frac_acft_matrix = []
    full_acft_list = []
    frac_acft_list = []

    for i in range(acft_number):
        
        aux1 = list_to_matrix(capacity[i],airports_number)
        capacity_matrix.append(aux1)

        aux2 = np.nan_to_num(flow_matrix/aux1)
        fraction.append(aux2)

        aux3 = np.floor(aux2)
        full_acft_matrix.append(aux3)
        
        aux4 = aux2-aux3
        frac_acft_matrix.append(aux4)

        aux5= matrix_to_list(aux3, airports_number)
        full_acft_list.append(aux5)

        aux6 = matrix_to_list(aux4, airports_number)
        frac_acft_list.append(aux6)

    total_acft_matrix = []
    for k in range(acft_number):
        aux = np.zeros((airports_number,airports_number))
        for i in range(airports_number):
            for j in range(airports_number):
                if frac_acft_matrix[k][i][j] > 0.5:
                    aux[i][j] = 1
                    
        total_acft_matrix.append(full_acft_matrix[k]  + aux)

    return full_acft_matrix, frac_acft_matrix, total_acft_matrix, full_acft_list, frac_acft_list

def revenue(full_acft_list, frac_acft_list, list_flow, inputs, airports_number):
    """This function computes the revenue from the network results
    :param full_acft_list: list of aircraft full loaded
    :param frac_acft_list: list of aircraft non-full loaded
    :param list_flow: flow of passenger list
    :param inputs: Contains the list of list with the inputs required to define
        the problem.
    :param airports_number: number of airports whitin the network
    :return
        revenue_total: total revenue of the network [US$]
    """
    min_capacity = float(inputs.list_excel_df[3]['min_capacity_per'][0]) 
    avg_ticket_price = float(inputs.list_excel_df[3]['avg_ticket_price'][0]) 

    payload = inputs.list_inputs[5]
    passenger_weight = int(inputs.list_excel_df[3]['passenger_weight'][0]) 
    capacity = [int(x / passenger_weight) for x in payload]

    distances_list = inputs.list_inputs[0]
    list_size = airports_number**2 - airports_number

    revenue_full_list = []
    for i in range(len(full_acft_list)):
        if (list_flow[i] <= 0 or full_acft_list[i] <= 0):
            revenue_full_list.append(0)
        else:
            revenue_full_list.append(capacity[i]*full_acft_list[i]*distances_list[i]*(capacity[i]*full_acft_list[i]*avg_ticket_price)/(capacity[i]*full_acft_list[i]*distances_list[i]))

    revenue_full_list = [0 if x != x else x for x in revenue_full_list]

    revenue_fracc_list = []
    for i in range(len(frac_acft_list)):
        if (list_flow[i] <= 0 or frac_acft_list[i] <= min_capacity):
            revenue_fracc_list.append(0)
        else:
            revenue_fracc_list.append(capacity[i]*frac_acft_list[i]*distances_list[i]*(capacity[i]*frac_acft_list[i]*avg_ticket_price)/(capacity[i]*frac_acft_list[i]*distances_list[i]))
    revenue_fracc_list = [0 if x != x else x for x in revenue_fracc_list]

    revenue_total_list = [x + y for x, y in zip(revenue_full_list,revenue_fracc_list)]
    revenue_total = sum(revenue_total_list)

    revenue_matrix = list_to_matrix(revenue_total_list,airports_number)

#     print('Revenue matrix:', revenue_matrix)

    return revenue_total


def processed_doc(airports_number, aircraft_matrix, inputs):
    """This function computes the DOC after consider the total
    used aircraft that presents the min. load requirement
    :param airports_number: number of airports whitin the network
    :param aircraft_matrix: aircraft frequencies matrix
    :param inputs: Contains the list of list with the inputs required to define
        the problem.
    :return
        DOC_total: total DOC of the network [US$]
    """
    doc = inputs.list_excel_df[2]
    DOCmat =  np.zeros((airports_number,airports_number))
    for i in range(airports_number):
        for j in range(airports_number):
            if i != j:
                DOCmat[i][j] = np.round(doc[i][j])
            else:
                DOCmat[i][j] = 0

    DOC_proccessed = np.zeros((airports_number,airports_number))
    for i in range(airports_number):
        for j in range(airports_number):
            DOC_proccessed[i][j] = DOCmat[i][j]*aircraft_matrix[i][j]

#     print('Processed DOC:', DOC_proccessed)

    DOC_total = np.sum(DOC_proccessed)

    return DOC_total

def network_parameters(aircraft_matrix,
                airports_number,
                inputs):
    """ This function computes network parameters:
        Active arcs
        Degree of nodes
        Cluster coefficient
    :param aircraft_matrix: aircraft frequencies matrix
    :param airports_number: number of airports whitin the network
    :param inputs: Contains the list of list with the inputs required to define
        the problem.
    :return
        network parameters
    """
    active_arcs_matrix = np.zeros(np.shape(aircraft_matrix))
    for i in range(airports_number):
        for j in range(airports_number):
            if aircraft_matrix[i][j] != 0:
                active_arcs_matrix[i][j] = 1

    active_arcs = np.sum(active_arcs_matrix)
    print('Active arcs: ', active_arcs)

    DON = np.zeros(airports_number)
    for i in range(airports_number):
        DON[i] = 0
        for j in range(airports_number):
            if i != airports_number:
                if active_arcs_matrix[i,j] == 1:
                    DON[i] = DON[i]+1

    print('Degree of nodes: ', DON)
    avg_DON = np.mean(DON)
    print('Avg. degree of nodes: ', avg_DON)

    list_distances = inputs.list_inputs[0]

    distances_matrix = list_to_matrix(list_distances,airports_number)

    R = 500
    C = np.zeros(airports_number)
    for i in range(airports_number):
        CON =0
        MAXCON = 0
        for j in range(airports_number):
            if i != j:
                if distances_matrix[i,j] <= R:
                    MAXCON = MAXCON + 1
                    if active_arcs_matrix[i,j] == 1:
                        CON = CON+1
        if MAXCON>0:
            C[i] = CON/MAXCON
        else:
            C[i] = 0

    print('Cluster', C)
    avg_C = np.mean(C)
    print('Avg. clustering: ', np.mean(C))

    net_parameters = [active_arcs, avg_DON, avg_C]
    return net_parameters

def postprocessing_results(
    inputs,
    solver,
    flow_variable_list, 
    flow_variable_list_names, 
    acft_variable_list, 
    acft_variable_list_names
    ):
    """ This funtion postprocess the data resulting from the network optimization
    :param inputs: Contains the list of list with the inputs required to define
        the problem.
    :param flow_variable_list:
        List of ortools Variable objects
    :param flow_variable_list_names,: list of str
        List of flow decision variable names
    :param acft_variable_list:
        List of ortools Variable objects
    :param acft_variable_list_names: list of str
        List of acft variable names
    :return
        postprocessed results
    """

    airports_number = len(inputs.list_excel_df[0])

    list_flow = []
    list_acft = []

    for i in range(len(flow_variable_list)):
        list_flow.append(flow_variable_list[i].solution_value())
        # print(flow_variable_list[i].solution_value())

    for i in range(len(acft_variable_list)):
        list_acft.append(acft_variable_list[i].solution_value())

    aircraft_matrix = list_to_matrix(list_acft,airports_number)
    full_acft_matrix, frac_acft_matrix, total_acft_matrix, full_acft_list, frac_acft_list = passenger_load(list_flow, airports_number, inputs)

    revenue_total = revenue(full_acft_list, frac_acft_list, list_flow, inputs, airports_number)

    DOC_total = processed_doc(airports_number, total_acft_matrix, inputs)

    print('Revenue:', revenue_total)
    print('DOC total', DOC_total)


    profit = int(1.0*revenue_total - 1.2*DOC_total)

    print('Profit:', profit)
    print('Margin: ',profit/revenue_total)

    net_parameters = network_parameters(total_acft_matrix,
                airports_number,
                inputs)



    return revenue_total, DOC_total, profit, net_parameters, total_acft_matrix






