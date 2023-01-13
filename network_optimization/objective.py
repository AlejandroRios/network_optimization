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
    from_list = inputs.list_inputs[3]
    docs_list = inputs.list_inputs[2]
    arcs = list(range(len(from_list)))

    objective = solver.Objective()
    direction = 'minimization'
    objective = solver.Minimize(sum([acft_variable_list[i]*docs_list[i] for i in range(len(arcs))]))


    return objective