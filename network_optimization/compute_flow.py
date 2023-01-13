    

def compute_supply_demand(wp):

    airports_number = len(wp.list_excel_df[0])

    dictionary_demands = wp.list_excel_df[1].T.to_dict()

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

    return list_supply_demand
