def compute_constraint_value(constraint_list, flow_variable_list, acft_variable_list, inputs):
    """This function computes the value of a constraint based on the
    solution of each flow_variable_list and acft_variable_list
    :param constraint_list: list of Constraint objects
    :param flow_variable_list:
        List of ortools Variable objects
    :param acft_variable_list:
        List of ortools Variable objects
    """
    aircraft_info = inputs.list_excel_df[3].T.to_dict()
    acft_number = len(aircraft_info)

    result = 0
    for i, flow_var in enumerate(flow_variable_list):
        coefficient = constraint_list.GetCoefficient(flow_var)
        var_val = flow_variable_list[i].solution_value()
        result += coefficient*var_val

    for k in range(acft_number):
        for i, acft_var in enumerate(acft_variable_list[k]):
            coefficient = constraint_list.GetCoefficient(acft_var)
            var_val = acft_variable_list[k][i].solution_value()
            result += coefficient*var_val

    return result