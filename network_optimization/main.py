from readinputs import InputData
from variables import configure_decision_variables
from constraints import configure_constraints
from objective import configure_objective
from results import print_results
from ortools.linear_solver import pywraplp
import time
import re

def run(
        filename,
        startdate
):
    """This function parses the input data, and executes the allocation
    problem for the network optimization considering a daily demand.
    :param filename: str
        Name of the file containing input data:
            - Daily demand
            - Distance between airports [NM]
            - Direct operational cost [US$]
    :param startdate: datetime object
        Date at which simulation starts
    """

    # Read inputs data
    inputs = InputData(filename)

    solver = pywraplp.Solver.CreateSolver('SCIP')
    # solver = pywraplp.Solver.CreateSolver('SAT')
    if not solver:
        return
    (
    flow_variable_list, 
    flow_variable_list_names, 
    acft_variable_list, 
    acft_variable_list_names
    ) = configure_decision_variables(inputs,solver)

    constraint_list = configure_constraints(
        inputs, 
        solver, 
        flow_variable_list, 
        acft_variable_list
        )

    objective = configure_objective(
        inputs, 
        solver, 
        acft_variable_list
        )

    # solve the network objective
    status = solver.Solve()
    print('Network operational cost')
    net_operational_cost = solver.Objective().Value()
    print(net_operational_cost)

    print('Solver status:')
    print('Optimal = 0: ',status)


    filename_output = re.split('\.', filename)[0]

    print_results(
            inputs, 
            solver, 
            flow_variable_list, 
            flow_variable_list_names, 
            acft_variable_list, 
            acft_variable_list_names,
            filename_output,
            startdate,
            status,
            constraint_list
            )




if __name__ == '__main__':

    filename = 'Network_inputs_5airports.xlsx'
    startdate = 'stardate'
    startrun = time.time()
    run(filename, startdate)
    print(time.time()- startrun)
    