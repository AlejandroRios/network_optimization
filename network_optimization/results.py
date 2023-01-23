from ortools.linear_solver import pywraplp
import re 
import datetime as dt
import pandas as pd
from objective_function_constraints import compute_constraint_value
from postprocessing import postprocessing_results
from plotting import plot_frequencies

def print_results(
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
        ):
    """This function print the results, apply postprocessing for profit calculation,
    plot the frequencies matrix and save the results to csv file
    :param inputs: Contains the list of list with the inputs required to define
            the problem. Here the froms and tos list are used.
    :param solver: pywraplp.Solver.CreateSolver object
    :param flow_variable_list:
        List of ortools Variable objects
    :param flow_variable_list_names,: list of str
        List of flow decision variable names
    :param acft_variable_list:
        List of ortools Variable objects
    :param acft_variable_list_names: list of str
        List of acft variable names
    :param filename_output (str) : output filename
    :param startdate (datetime object): date at which simulation starts
    :param constraint_list: list of Constraint objects
        List of constraints
        already added to the optimization model
    :return
    """

    if status != pywraplp.Solver.OPTIMAL:
        print("The problem does not have (or did not find) an optimal solution!")
        if status == pywraplp.Solver.FEASIBLE:
            print('It found a feasible solution')
        """
        debug_constraints(
            constraint_list, 
            flow_variable_list_names, 
            flow_variable_list, 
            acft_variable_list_names, 
            acft_variable_list
        )
        """
    else:
        print("Optimal solution found")
        print(('Problem solved in %f milliseconds' % solver.wall_time()))

        aircraft_info = inputs.list_excel_df[3].T.to_dict()
        acft_number = len(aircraft_info)
        total_flow = []
        for i in range(len(flow_variable_list)):
            if flow_variable_list[i].solution_value() != 0:
                print(flow_variable_list_names[i] + ': {}'.format(flow_variable_list[i].solution_value()))
                total_flow.append(flow_variable_list[i].solution_value())
        
        total_num_acft = []
        for k in range(acft_number):
            for i in range(len(acft_variable_list[k])):
                if acft_variable_list[k][i].solution_value() != 0:
                    print(acft_variable_list_names[k][i] + ': {}'.format(acft_variable_list[k][i].solution_value()))
                    total_num_acft.append(acft_variable_list[k][i].solution_value())
                    
    
        print('Objective value: {}'.format(solver.Objective().Value()))

        print('Total flow of pax:', sum(total_flow))
        print('Total num of acft:', sum(total_num_acft))
    

        # compute the results of previous objective functions
        result_constraints = compute_constraint_value(
                constraint_list[0], flow_variable_list, acft_variable_list, inputs
                )
        
        # postprocessing of results to obtain Profit and other parameters
        revenue_total, DOC_total, profit, net_parameters, total_acft_matrix= postprocessing_results(
            inputs, 
            solver, 
            flow_variable_list, 
            flow_variable_list_names, 
            acft_variable_list, 
            acft_variable_list_names,
            )
        
        for k in range(acft_number):
            plot_frequencies(inputs, total_acft_matrix[k])

        # df = results_to_csv(
        #         allocation, 
        #         inputs, 
        #         global_intervals, 
        #         startdate, 
        #         results_objective_functions
        #         )
        # file_name ='./Output/allocation_' + filename_output + '.csv'
        # df.to_csv(file_name, index=False)
        
        # # save solution fig
        # fig = plot_results(
        #         time_instances,
        #         inputs, 
        #         mro, 
        #         allocation,
        #         startdate
        #         )
        # file_name ='./Output/allocation_' + filename_output + '.png'
        # fig.savefig(file_name)