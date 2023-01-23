# Network Optimization
Initial Proof of Concept (POC) for the network optimization problem.

# Objective
Design the mathematical model to issue the most optimised network frequencies that minimizes the cost given a daily demand. One objective functions are considered:
- Minimizing total network cost

# How to launch
Before launching make sure to have installed the python packages cited in the requirements_minimal.txt file. Also make sure to install ortools by
```
> python -m pip install --upgrade --user ortools
```

Activate environment and, in terminal launch by calling the main.py module. Two user inputs are required; (1) the name of the input file and (2) the date at which the simulation starts in the format *%d/%m/%Y %H:%M*. 
```
> python main.py --filename "Network_inputs_5airports_test.xlsx" --startdate "23/01/2022 15:57"
```

# References
[1] 
