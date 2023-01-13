import os
import pandas as pd
import datetime as dt
from copy import deepcopy
from payload_range import payloadrange_diagram

class InputData:
    def __init__(self, filename):
        """This class contains the information of all inputss
        :param filename: str
            Name of the file
        :return self
        """
        self.path = os.getcwd() + '/Inputs/' + filename
        self.list_excel_df = self._read_excel()
        self.list_inputs = self.dict_to_list()
        self.list_flow = self.compute_supply_demand()

    def _read_excel(self):
        """This method reads the Network_inputs_#airports.xlsx file and extracts all info on
        demandas, distances and DOCs matrices (inputs)
        :param self
        :return
            list_dataframes
                Contains all inputs info
        Notes
        -----
        * We expect the input file to have five sheets with the names
        {Distances, Demandas, DOCs}
        """

        print(self.path)

        df_distances = pd.read_excel(self.path, sheet_name='Distances', index_col=None, header=None)

        market_share = 0.1 # Ten percent market share
        df_demands_total = pd.read_excel(
                self.path, 
                sheet_name='Demands', index_col=None, header=None
                )
        df_demands = (df_demands_total*market_share).astype(int)

        df_DOCs = pd.read_excel(self.path, sheet_name='DOCs', index_col=None, header=None)

        df_acft = pd.read_excel(self.path, sheet_name='Aircraft')

        list_dataframes = [df_distances, df_demands, df_DOCs, df_acft]

        return list_dataframes

    def dict_to_list(self):
        """This function transformate the inputs into the correct list order
        to be used in the problem setup.
        :return
            list_inputs: list of list containing all inputs including
            list froms (froms_list) specifing the departure options and list 
            of tos (tos_list) specifing the arrival options.
        """      
        dictionary_distances = self.list_excel_df[0].T.to_dict()

        airports_number = len(self.list_excel_df[0])

        aircraft_info = self.list_excel_df[3].T.to_dict()

        print('Airports number:', airports_number)

        distances_list = []
        for i in range(airports_number): 
            for j in range(airports_number):
                if i != j and i < j:
                    distances_list.append(dictionary_distances[i][j])
        for i in range(airports_number):
            for j in range(airports_number):
                if i != j and i > j:
                    distances_list.append(dictionary_distances[i][j])

        dictionary_demands = self.list_excel_df[1].T.to_dict()
        demand_list= []
        for i in range(airports_number): 
            for j in range(airports_number):
                if i != j and i < j:
                    demand_list.append(dictionary_demands[i][j])
        for i in range(airports_number): 
            for j in range(airports_number):
                if i != j and i > j:
                    demand_list.append(dictionary_demands[i][j])

        dictionary_docs = self.list_excel_df[2].T.to_dict()
        docs_list = []
        for i in range(airports_number): 
            for j in range(airports_number):
                if i != j and i < j:
                    if (dictionary_docs[i][j] > 10000000) or (dictionary_demands[i][j]==0):
                        docs_list.append(1000000)
                    else:
                        docs_list.append(dictionary_docs[i][j])
        for i in range(airports_number): 
            for j in range(airports_number):
                if i != j and i > j:
                    if (dictionary_docs[i][j] > 10000000) or (dictionary_demands[i][j]==0):
                        docs_list.append(1000000)
                    else:
                        docs_list.append(dictionary_docs[i][j])

        froms_list = []
        for i in range(airports_number): 
            for j in range(airports_number): 
                if i != j and i < j:
                    froms_list.append(i)
        for i in range(airports_number): 
            for j in range(airports_number): 
                if i != j and i > j:
                    froms_list.append(i)

        tos_list = []
        for i in range(airports_number): 
            for j in range(airports_number): 
                if i != j and i < j:
                    tos_list.append(j)
        for i in range(airports_number): 
            for j in range(airports_number): 
                if i != j and i > j:
                    tos_list.append(j)

        payloads_list = []

        ranges = pd.eval(aircraft_info[0]['ranges'])
        payload = pd.eval(aircraft_info[0]['payloads'])

        points =  [(ranges[0],payload[0]),(ranges[1],payload[1]),(ranges[2],payload[2]),(ranges[3],payload[3])]

        payload = [payloadrange_diagram(points,x) for x in distances_list]
        
        list_inputs = [distances_list, demand_list, docs_list, froms_list, tos_list,payload]



        return list_inputs

    def compute_supply_demand(self):
        """This function computes the relation between
        in-out flow from the daily demand. In performs the sum of all the in and 
        out flow from a node. A negative value within the list means that the node
        has more outflow than inflow. A positive value means the contrary.
        :return
            list_supply_demand: list of list containing the bi-directional flow sum
        """

        airports_number = len(self.list_excel_df[0])

        dictionary_demands = self.list_excel_df[1].T.to_dict()

        nodes = list(range(airports_number*2))
        demand_aux = []
        supply_aux = []
        for i in range(airports_number):
            aux1 = [dictionary_demands[i][j] for j in range(airports_number) if i != j and i > j ]
            demand_aux.append(sum(aux1))
            aux2 = [dictionary_demands[i][j] for j in range(airports_number) if i != j and i < j ]
            supply_aux.append(sum(aux2))

        sup_dem_ij = [x - y for x, y in zip(demand_aux, supply_aux)]
        sup_dem_ji = [x - y for x, y in zip(supply_aux, demand_aux)]

        list_supply_demand = [sup_dem_ij, sup_dem_ji]

        # print('supply demand:',list_supply_demand)

        return list_supply_demand
