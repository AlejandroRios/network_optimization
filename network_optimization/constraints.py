def demand_constraint(solver,
        flow_variable_list,
        arcs,
        demand_sum,
        constraint_list):
    """This function implements the demand constraint, which ensures that 
    the sum of all the passengers transported are equal to the total demand
    :param solver: pywraplp.Solver.CreateSolver object
    :param flow_variable_list:
        List of ortools Variable objects
    :param arcs: number of arcs whitin the nework
    :param demand_sum: sum of the total daily demand (considering market share)
    :param constraint_list: list of Constraint objects
        List of constraints
        already added to the optimization model
    :return
        constraint_list: list
            List of Constraint objects appended
    """    


    constraint_list.append(solver.Add(sum([flow_variable_list[i] for i in range(len(arcs))]) == demand_sum))

    return constraint_list


def route_capacity_constraint(solver,
        flow_variable_list,
        acft_variable_list,
        arcs,
        inputs,
        constraint_list):
    """This function implements the capacity constraint, which ensures that 
    the capacity of the route is respected
    :param solver: pywraplp.Solver.CreateSolver object
    :param flow_variable_list:
        List of ortools Variable objects
    :param acft_variable_list:
        List of ortools Variable objects
    :param arcs: number of arcs whitin the nework
    :param inputs: average capacity of the aircraft (passenger capacity)
    :param constraint_list: list of Constraint objects
        List of constraints
        already added to the optimization model
    :return
        constraint_list: list
            List of Constraint objects appended
    """ 
    payload = inputs.list_inputs[5]
    passenger_weight = int(inputs.list_excel_df[3]['passenger_weight'][0]) 
    capacity = [int(x / passenger_weight) for x in payload]
    for i in arcs:
        constraint_list.append(solver.Add(flow_variable_list[i] <= acft_variable_list[i]*capacity[i]))# Capacity constraint

    return constraint_list

def flow_constraint(solver,
        flow_variable_list,
        arcs,
        nodes,
        from_list, 
        to_list,
        sup_dem_ij,
        sup_dem_ji,
        constraint_list):
    """This function implements the capacity constraint, which ensures that 
    the capacity of the route is respected
    :param solver: pywraplp.Solver.CreateSolver object
    :param flow_variable_list:
        List of ortools Variable objects
    :param arcs: number of arcs whitin the nework
    :param nodes: number of nodes whitin the nework
    :param from_list: departure index list
    :param to_list: arrival index list
    :param suply and deman relation list: 
        sup_dem_ij: from i to j
        sup_dem_ji: from j to i
    :param constraint_list: list of Constraint objects
        List of constraints
        already added to the optimization model
    :return
        constraint_list: list
            List of Constraint objects appended
    """  
    for i in range(0,len(nodes)//2):
        constraint_list.append(solver.Add(sum(flow_variable_list[j] for j in range(0,len(arcs)//2) if to_list[j] == i) - sum(flow_variable_list[j] for j in range(0,len(arcs)//2) if from_list[j] == i) == sup_dem_ij[i])) # Capacity constraint

    for i in range(0,len(nodes)//2):
        constraint_list.append(solver.Add(sum(flow_variable_list[j] for j in range(len(arcs)//2,len(arcs)) if to_list[j] == i) - sum(flow_variable_list[j] for j in range(len(arcs)//2,len(arcs)) if from_list[j] == i) == sup_dem_ji[i])) # Capacity constraint
        
    return constraint_list



def configure_constraints(
        inputs, 
        solver, 
        flow_variable_list, 
        acft_variable_list
        ):
    """This function computes the constraints for the Network Optimization
    problem
    :param inputs: Contains the list of list with the inputs required to define
        the problem.
    :param solver: pywraplp.Solver.CreateSolver object
    :param flow_variable_list:
        List of ortools Variable objects
    :param acft_variable_list:
        List of ortools Variable objects
    :return
        constraint_list: list
            List of Constraint objects appended
    Notes:
        (1) This function will modify the solver object by setting the constraints
        to it
    """

    from_list = inputs.list_inputs[3]
    to_list = inputs.list_inputs[4]
    sup_dem_ij = inputs.list_flow[0]
    sup_dem_ji = inputs.list_flow[1]

    airports_number = len(inputs.list_excel_df[0])

    arcs = list(range(len(from_list)))
    nodes = list(range(airports_number*2))

    constraint_list = []

    demand_sum = sum(inputs.list_inputs[1])
    
    # Constraint that ensures that all the demand is fulfilled
    constraint_list = demand_constraint(solver,
        flow_variable_list,
        arcs,
        demand_sum,
        constraint_list)
    
    # Constraint that avoid the extrapolation of the capacity of the route
    constraint_list = route_capacity_constraint(solver,
        flow_variable_list,
        acft_variable_list,
        arcs,
        inputs,
        constraint_list)
    
    # Consraint that ensures the correct in-out flow through the network nodes
    constraint_list = flow_constraint(solver,
        flow_variable_list,
        arcs,
        nodes,
        from_list, 
        to_list,
        sup_dem_ij,
        sup_dem_ji,
        constraint_list)

    return constraint_list