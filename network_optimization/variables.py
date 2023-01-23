def configure_decision_variables(
        inputs, 
        solver
        ):
    """
    This function computes the list of decision variables and a list with their
    names. Two variables are defined:
        - flow_variable_list: Flow of passangeres being transported within the
        network
        - acft_variable_list: Number of aircraft to be used to fulfill the demand
    :param inputs: Contains the list of list with the inputs required to define
            the problem. Here the froms and tos list are used.
    :param solver: pywraplp.Solver.CreateSolver object
    :return
        flow_variable_list: list of Var objects
            List of int decision variables
        flow_variable_list_names,: list of str
            List of flow decision variable names
        acft_variable_list: list of Var objects
            List of int decisio variables
        acft_variable_list_names: list of str
            List of acft variable names
    """
    aircraft_info = inputs.list_excel_df[3].T.to_dict()
    acft_number = len(aircraft_info)
    # Flow of passengers decision variables and their names 
    flow_variable_list = []
    flow_variable_list_names = []
    
    # Used aircraft decision variables and their names 
    acft_variable_list = []
    acft_variable_list_names = []

    from_list = inputs.list_inputs[3]
    to_list = inputs.list_inputs[4]
    
    # number of total arcs within the network
    arcs = list(range(len(from_list)))
    infinity = solver.infinity() # Defines upper bound of the variable (infinite)
    max_allowed_acft = float(inputs.list_excel_df[3]['max_allowed_acft'][0]) # max allowed acft to fly a leg

    for t in arcs:
        flow_var_name = 'flow_' + str(from_list[t]+1) + 'to' + str(to_list[t]+1)
        flow_variable_list.append(solver.IntVar(0, infinity, flow_var_name)) # Variabe bounds definition
        flow_variable_list_names.append(flow_var_name)
    

    for k in range(acft_number):
        aux1 = []
        aux2 = []
        for t in arcs:
            acft_var_name = 'acft_'+str(k+1)+'_'+str(from_list[t]+1)+ 'to'+ str(to_list[t]+1)
            aux1.append(solver.IntVar(0, max_allowed_acft, acft_var_name))
            aux2.append(acft_var_name)
        acft_variable_list.append(aux1)
        acft_variable_list_names.append(aux2)

    return (
            flow_variable_list, 
            flow_variable_list_names, 
            acft_variable_list, 
            acft_variable_list_names
            )

    """This function convert a list (without i=j) of parameters
    to the matrix form (including i=j)
    Example: if the network considers 5 airports the input list
    has len = 20. The output matrix will be size(5,5)
    :param list: list of variables to be converted to matrix form
    :param size: value of the size of the matrix
    :return
        marix: array containing the output matrix size(size,size)
    """