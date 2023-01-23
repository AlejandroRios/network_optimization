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

def passenger_load(list_acft, list_flow, airports_number, inputs):
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
    payload = inputs.list_inputs[5]
    aircraft_info = inputs.list_excel_df[3].T.to_dict()
    acft_number = len(aircraft_info)
    
    # Pax capacity according to leg distance
    capacity = []
    for k in range(acft_number):
        passenger_weight = int(inputs.list_excel_df[3]['passenger_weight'][k]) 
        aux = [int(x / passenger_weight) for x in payload[k]]
        capacity.append(aux)
    
    # Calculates pax flow considering max load factor
    acft_full_capacity = []
    for k in range(acft_number):
        aux2 = []
        for i in range(len(list_flow)):
            aux2.append(capacity[k][i]*list_acft[k][i])
        acft_full_capacity.append(aux2)
    

    # Calculates the flow distribution for each leg
    # This follows a fill order where the bigger acft is filled first
    initial_flow = list_flow
    demand_evol = []
    for k in reversed(range(acft_number)):
        aux3 = []
        for i in range(len(list_flow)):
            if initial_flow[i] > 0:
                new_flow = initial_flow[i]  - acft_full_capacity[k][i]
            else:
                if k == acft_number-1:
                    new_flow = initial_flow[i] 
                else:
                    new_flow = 0
            aux3.append(new_flow)
        initial_flow = aux3
        demand_evol.append(aux3)
    
    # Add initial flow list and reverse the order (smaller to bigger acft)
    demand_evol.insert(0,list_flow)
    demand_evol = list(reversed(demand_evol))

    demand_evol2 = demand_evol[1:]

    total_acft_used = []
    flow_fraction_full = []
    flow_fraction_incomplete = []
    incomplete_acft = []
    incomplete_flow = []
    deactivated_acft = []

    incomplete_flights = []
    full_flights = []
    total_flow = []

    full_flighs_flow = []
    total_flow = []
    incomplete_flow_tot = []

    total_acft_matrix = []
    full_acft_matrix = []
    incomplete_acft_matrix = []
    for k in range(acft_number):
        # Several list are created to store intermediate information related to the calculation
        # of total flow and aircraft used considering the min. load factor of each acft.
        # Acft that dont meet the min. load factor are deactivated.
        aux4 = []
        aux5 = []
        for i in range(len(list_flow)):
            if acft_full_capacity[k][i] > demand_evol2[k][i] and acft_full_capacity[k][i] > 0:
                aux4.append(demand_evol2[k][i]/acft_full_capacity[k][i])
            else:
                aux4.append(0)
        
        for i in range(len(list_flow)):
            if aux4[i] > 0:
                aux5.append(1)
            else:
                aux5.append(0)    

        incomplete_acft.append(aux5)
        flow_fraction_full.append(aux4)

        aux6 = []
        aux7 = []
        for i in range(len(list_flow)):
            if incomplete_acft[k][i] > 0:
                aux6.append(incomplete_acft[k][i]*capacity[k][i] + demand_evol[k][i])
            else:
                aux6.append(0)
        incomplete_flow.append(aux6)
        
        for i in range(len(list_flow)):
            aux7.append(incomplete_flow[k][i]/capacity[k][i])
        flow_fraction_incomplete.append(aux7)

        aux8 = []
        for i in range(len(list_flow)):
            if flow_fraction_incomplete[k][i] == 0 or flow_fraction_incomplete[k][i]> aircraft_info[k]['min_load_factor']:
                aux8.append(0)
            else:
                aux8.append(1)
        deactivated_acft.append(aux8)

        aux9 = []
        aux10 = []
        for i in range(len(list_flow)):
            if incomplete_flow[k][i] > 0 and flow_fraction_incomplete[k][i] > aircraft_info[k]['min_load_factor']:
                aux9.append(1)
            else:
                aux9.append(0)

        incomplete_flights.append(aux9)

        for i in range(len(list_flow)):
            aux10.append(list_acft[k][i] - incomplete_flights[k][i] - deactivated_acft[k][i])

        full_flights.append(aux10) 

        aux11 = []
        aux12 = []
        for i in range(len(list_flow)):
            aux11.append(full_flights[k][i]*capacity[k][i])

        full_flighs_flow.append(aux11)

        for i in range(len(list_flow)):
            if flow_fraction_incomplete[k][i] > aircraft_info[k]['min_load_factor']:
                aux12.append(flow_fraction_incomplete[k][i]*capacity[k][i])
            else:
                aux12.append(0)

        incomplete_flow_tot.append(aux12)

        aux13 = []
        aux14 = []
        for i in range(len(list_flow)):
            aux13.append(full_flighs_flow[k][i]+incomplete_flow_tot[k][i])

        total_flow.append(aux13)

        for i in range(len(list_flow)):
            aux14.append(full_flights[k][i]+incomplete_flights[k][i])
        total_acft_used.append(aux14)
        
        # Converting relevant parameters from list to matrix form
        full_acft_matrix.append(list_to_matrix(full_flights[k],airports_number))
        incomplete_acft_matrix.append(list_to_matrix(incomplete_flights[k],airports_number))
        total_acft_matrix.append(list_to_matrix(total_acft_used[k],airports_number))

    return incomplete_acft, full_flights, incomplete_flow_tot, full_flighs_flow, total_acft_matrix

def revenue(full_flights, incomplete_acft, inputs, airports_number):
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

    avg_ticket_price = float(inputs.list_excel_df[3]['avg_ticket_price'][0]) 

    distances_list = inputs.list_inputs[0]
    list_size = airports_number**2 - airports_number

    revenue_full_list = []
    for i in range(len(full_flights)):
        if full_flights[i] <= 0:
            revenue_full_list.append(0)
        else:
            revenue_full_list.append(full_flights[i]*distances_list[i]*(full_flights[i]*avg_ticket_price)/(full_flights[i]*distances_list[i]))

    revenue_full_list = [0 if x != x else x for x in revenue_full_list]

    revenue_fracc_list = []
    for i in range(len(incomplete_acft)):
        if incomplete_acft[i] <= 0:
            revenue_fracc_list.append(0)
        else:
            revenue_fracc_list.append(incomplete_acft[i]*distances_list[i]*(incomplete_acft[i]*avg_ticket_price)/(incomplete_acft[i]*distances_list[i]))
    revenue_fracc_list = [0 if x != x else x for x in revenue_fracc_list]

    revenue_total_list = [x + y for x, y in zip(revenue_full_list,revenue_fracc_list)]
    revenue_total = sum(revenue_total_list)

    revenue_matrix = list_to_matrix(revenue_total_list,airports_number)

    # print('Revenue matrix:', revenue_matrix)

    return revenue_total

def processed_doc(airports_number, aircraft_matrix, inputs,k):
    """This function computes the DOC after consider the total
    used aircraft that presents the min. load requirement
    :param airports_number: number of airports whitin the network
    :param aircraft_matrix: aircraft frequencies matrix
    :param inputs: Contains the list of list with the inputs required to define
        the problem.
    :return
        DOC_total: total DOC of the network [US$]
    """


    doc = inputs.list_excel_df[2][k]
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
    
    aircraft_info = inputs.list_excel_df[3].T.to_dict()
    acft_number = len(aircraft_info)
    print('==================================================================')
    print('Pax. flow variable results:')
    list_flow = []
    for i in range(len(flow_variable_list)):
        list_flow.append(flow_variable_list[i].solution_value())
        print(flow_variable_list_names[i],flow_variable_list[i].solution_value())

    print('==================================================================')

    print('Used acft. variable results:')
    list_acft = []
    aircraft_matrix = []
    for k in range(acft_number):
        aux = []
        for i in range(len(acft_variable_list[k])):
            print(acft_variable_list_names[k][i], acft_variable_list[k][i].solution_value())
            aux.append(acft_variable_list[k][i].solution_value())
        list_acft.append(aux)

        aircraft_matrix.append(list_to_matrix(list_acft[k],airports_number))
    print('==================================================================')


    incomplete_acft, full_flights, incomplete_flow_tot, full_flighs_flow, total_acft_matrix = passenger_load(list_acft, list_flow, airports_number, inputs)
    
    revenue_total = []
    DOC_total = []
    for k in range(acft_number):
        revenue_acft = revenue(full_flighs_flow[k], incomplete_flow_tot[k], inputs, airports_number)
        revenue_total.append(revenue_acft)


        DOC_acft = processed_doc(airports_number, total_acft_matrix[k], inputs,k)
        DOC_total.append(DOC_acft)

    print('Revenue:', sum(revenue_total))
    print('DOC total', sum(DOC_total))


    profit = int(1.0*sum(revenue_total) - 1.2*sum(DOC_total))
    print('Profit:', profit)
    print('Margin: ',profit/sum(revenue_total))
    print('==================================================================')
    net_parameters = []
    for k in range(acft_number):
        net_par_acft = network_parameters(total_acft_matrix[k],
                airports_number,
                inputs)
        net_parameters.append(net_par_acft)

    print('==================================================================')

    return revenue_total, DOC_total, profit, net_parameters, total_acft_matrix