def configure_objective(
        inputs, 
        solver, 
        acft_variable_list
        ):
    """This function the objectve of the network optimization problem:
        - min(total network operation cost)
    :param inputs: Contains the list of list with the inputs required to define
        the problem.
    :param solver: pywraplp.Solver.CreateSolver object
    :param acft_variable_list:
        List of ortools Variable objects
    :return
        objective: solver.Objective object
    """
    aircraft_info = inputs.list_excel_df[3].T.to_dict()
    acft_number = len(aircraft_info)

    from_list = inputs.list_inputs[3]
    docs_list = inputs.list_inputs[2]
    arcs = list(range(len(from_list)))
    
    docs_lists = []
    for i in range(acft_number):
        docs_lists.extend(inputs.list_inputs[2][i])


    acft_variable_list =  [item for sublist in acft_variable_list for item in sublist]


    objective = solver.Objective()
    direction = 'minimization'
    objective = solver.Minimize(sum([acft_variable_list[i]*docs_lists[i] for i in range(len(docs_lists))]))


    return objective