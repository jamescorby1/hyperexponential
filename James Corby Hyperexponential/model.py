#
# Starter code for Modelling Case Study Exercise
#
import math

def get_example_data():
    """
    Return an example data structure containing the inputs and placeholder outputs for the drone pricing model
    """
    example_data = {
        "insured": "Drones R Us",
        "underwriter": "Michael",
        "broker": "AON",
        "brokerage": 0.3,
        "max_drones_in_air": 2,
        "drones": [
            {
                "serial_number": "AAA-111",
                "value": 10000,
                "weight": "0 - 5kg",
                "has_detachable_camera": True,
                "tpl_limit": 1000000,
                "tpl_excess": 0,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            },
            {
                "serial_number": "BBB-222",
                "value": 12000,
                "weight": "10 - 20kg",
                "has_detachable_camera": False,
                "tpl_limit": 4000000,
                "tpl_excess": 1000000,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            },
            {
                "serial_number": "AAA-123",
                "value": 15000,
                "weight": "5 - 10kg",
                "has_detachable_camera": True,
                "tpl_limit": 5000000,
                "tpl_excess": 5000000,
                "hull_base_rate": None,
                "hull_weight_adjustment": None,
                "hull_final_rate": None,
                "hull_premium": None,
                "tpl_base_rate": None,
                "tpl_base_layer_premium": None,
                "tpl_ilf": None,
                "tpl_layer_premium": None
            }
        ],
        "detachable_cameras": [
            {
                "serial_number": "ZZZ-999",
                "value": 5000,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "YYY-888",
                "value": 2500,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "XXX-777",
                "value": 1500,
                "hull_rate": None,
                "hull_premium": None
            },
            {
                "serial_number": "WWW-666",
                "value": 2000,
                "hull_rate": None,
                "hull_premium": None
            }

        ],
        "gross_prem": {
            "drones_hull": None,
            "drones_tpl": None,
            "cameras_hull": None,
            "total": None
        },
        "net_prem": {
            "drones_hull": None,
            "drones_tpl": None,
            "cameras_hull": None,
            "total": None
        }
    }

    return example_data


def main():
    """
    Perform the rating calculations replicating 
    """

    # Get the example data structure
    model_data = get_example_data()
    
    #Add the paremeters from the model spreadsheet to be used for calculations. 
    gross_base_rates = { "hull" : 0.06, "liability": 0.02}
    riebesell = {"base_limit": 1000000,"z": 0.2}
    adjusted_weights = {"0 - 5kg": 1, "5 - 10kg": 1.2, "10 - 20kg": 1.6, ">20kg": 2.5}
    
    #Calculating the values that are associated with the drones
    for drone in model_data['drones']:
            
        #Add in the rates for both Hull and TPL
        drone['hull_base_rate'] = gross_base_rates["hull"]
        drone['tpl_base_rate'] = gross_base_rates["liability"]
        
        # Hull calculations
        if drone['weight'] == "0 - 5kg":
            drone['hull_weight_adjustment'] = adjusted_weights["0 - 5kg"]
        elif drone['weight'] == "5 - 10kg":
            drone['hull_weight_adjustment'] = adjusted_weights["5 - 10kg"]
        elif drone['weight'] == "10 - 20kg":
            drone['hull_weight_adjustment'] = adjusted_weights["10 - 20kg"]
        else:
            drone['hull_weight_adjustment'] = adjusted_weights[">20kg"]
        
        drone['hull_final_rate'] = drone['hull_base_rate'] * drone['hull_weight_adjustment'] if drone['value'] is not None else 0 
        drone['hull_premium'] = drone['hull_final_rate'] * drone['value'] if drone['value'] is not None else 0

        #TPL calculations
        drone['tpl_base_layer_premium'] = round(drone['value'] * drone['tpl_base_rate'] if drone['value'] is not None else 0)
        drone['tpl_ilf'] = round(((drone['tpl_limit'] + drone['tpl_excess']) / riebesell['base_limit']) ** math.log2(1 + riebesell['z']) - (drone['tpl_excess'] / riebesell['base_limit']) ** math.log2(1 + riebesell['z']), 3)
        drone['tpl_layer_premium'] = drone['tpl_base_layer_premium'] * drone['tpl_ilf'] if drone['value'] is not None else 0


    #Calculating the values associated with the camera data
    final_rates = []
    for drone in model_data['drones']:
        if drone['has_detachable_camera'] == True:
            final_rates.append(drone['hull_final_rate'])
    
    for camera in model_data['detachable_cameras']:
        camera['hull_rate'] = max(final_rates)
        camera['hull_premium'] = round(camera['value'] * camera['hull_rate'], 3) if camera['value'] is not None else 0
    
    #Calculating the premium summary values 
    model_data['net_prem']['drones_hull'] = 0 
    model_data['net_prem']['drones_tpl'] = 0
    for drone in model_data['drones']:
        model_data['net_prem']['drones_hull'] += drone['hull_premium']
        model_data['net_prem']['drones_tpl'] += drone['tpl_layer_premium']
    model_data['net_prem']['cameras_hull'] = 0
    for camera in model_data['detachable_cameras']:
        model_data['net_prem']['cameras_hull'] += camera['hull_premium']
    model_data['net_prem']['total'] = model_data['net_prem']['drones_hull'] + model_data['net_prem']['drones_tpl'] + model_data['net_prem']['cameras_hull']
    
    #Calculating the gross premium summary values 
    model_data['gross_prem']['drones_hull'] = round(model_data['net_prem']['drones_hull'] / (1 - model_data['brokerage']))
    model_data['gross_prem']['drones_tpl'] = round(model_data['net_prem']['drones_tpl'] / (1 - model_data['brokerage']))
    model_data['gross_prem']['cameras_hull'] = round(model_data['net_prem']['cameras_hull'] / (1 - model_data['brokerage']))
    model_data['gross_prem']['total'] = round(model_data['gross_prem']['drones_hull'] + model_data['gross_prem']['drones_tpl'] + model_data['gross_prem']['cameras_hull'])


    return model_data


if __name__ == '__main__':
    print(main())


