
def calculate_wqi(data):
    # Assumed standards and weights
    standards = {
        'Cl-Dis': 250,
        'Cl-Tot': 250,
        'NH4N': 1.5,
        'NO2N': 1,
        'NO3N': 10,
        'O2-Dis': 5,  # Minimum standard
        'SO4-Tot': 250,
        'TN': 5,
        'TP': 1
    }

    weights = {
        'Cl-Dis': 1,
        'Cl-Tot': 1,
        'NH4N': 2,
        'NO2N': 2,
        'NO3N': 1,
        'O2-Dis': 3,
        'SO4-Tot': 1,
        'TN': 2,
        'TP': 2,
        'pH': 3
    }

    # Calculate sub-indices
    sub_indices = {}
    for param, value in data.items():
        if param in standards:
            # For O2-Dis, higher is better
            if param == 'O2-Dis':
                sub_index = ((value - standards[param]) / (standards[param])) * 100
            else:
                sub_index = ((standards[param] - value) / standards[param]) * 100

            sub_indices[param] = sub_index

    # For pH, special handling (outside the loop to ensure it's correctly computed)
    if data['pH'] < 6.5:
        sub_index_pH = (data['pH'] / 6.5) * 100
    elif data['pH'] > 8.5:
        sub_index_pH = ((9 - data['pH']) / 0.5) * 100
    else:
        sub_index_pH = 100
    sub_indices['pH'] = sub_index_pH

    # Calculate WQI
    wqi = sum(weights[param] * sub_indices[param] for param in weights if param != 'TEMP' and param != 'TOC') / sum(weights.values())

    # Categorizing WQI into qualitative descriptors
    def categorize_wqi(wqi_value):
        if wqi_value > 85:
            return "Excellent"
        elif wqi_value > 70:
            return "Good"
        elif wqi_value > 50:
            return "Fair"
        elif wqi_value > 25:
            return "Marginal"
        else:
            return "Poor"

    wqi_category = categorize_wqi(wqi)

    return wqi, wqi_category
