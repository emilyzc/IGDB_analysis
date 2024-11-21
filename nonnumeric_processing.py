import json
import plotly.graph_objects as go
from datetime import datetime



def delete_before_processing(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    # Delete unnecessary features
    features_to_delete = ['hypes', 'name', 'parent_game', 'slug', 'tags', 'updated_at', 'url', 'game_engines', 'websites', 
                      'alternative_names', 'version_parent', 'version_title', 'status', 'ports', 'remakes', 'expansions',
                      'standalone_expansions', 'remasters', 'expanded_games', 'franchise', 'forks']

    for item in data:
        for feature in features_to_delete:
            if feature in item:
                del item[feature]
    
    return data



def process_age_ratings(data):
    # Rated for adults
    desired_ratings = {5, 11, 12, 17, 22, 26, 33, 38, 39}

    for item in data:
        if 'age_ratings' in item:
            ratings_present = {rating_dict['rating'] for rating_dict in item['age_ratings']}
            # If the only rating is 27 (testing)
            if ratings_present == {27}:
                item['age_ratings'] = 0.5
            # If any of the desired ratings is present
            elif ratings_present & desired_ratings:
                item['age_ratings'] = 1
            else:
                item['age_ratings'] = 0

    return data



def process_involved_companies(data):
    # Initialize new features as empty lists
    for item in data:
        item['involved_companies_developer'] = []
        item['involved_companies_porting'] = []
        item['involved_companies_publisher'] = []
        item['involved_companies_supporting'] = []

        # Check if the item has 'involved_companies_i' feature
        if 'involved_companies' in item:
            for company in item['involved_companies']:
                # Add company id to the new features if the company is a developer, porting, publisher, or supporting
                if company['developer']:
                    item['involved_companies_developer'].append(company['company'])
                if company['porting']:
                    item['involved_companies_porting'].append(company['company'])
                if company['publisher']:
                    item['involved_companies_publisher'].append(company['company'])
                if company['supporting']:
                    item['involved_companies_supporting'].append(company['company'])

            # Delete the original 'involved_companies' feature
            del item['involved_companies']
    return data



def one_hot_encode_feature(data, feature_name):
    # Missing value
    missing_count = sum(1 for item in data if feature_name not in item or item[feature_name] is None)
    total_count = len(data)
    missing_ratio = missing_count / total_count
    print(f"The missing ratio of '{feature_name}' is: {missing_ratio}")
    
    # Visualization
    # Count the occurrences of each unique value, including null values
    value_counts = {}
    for item in data:
        if feature_name in item:
            if isinstance(item[feature_name], list):
                for val in item[feature_name]:
                    value_counts[val] = value_counts.get(val, 0) + 1
            else:
                value_counts['null'] = value_counts.get('null', 0) + 1
        else:
            value_counts['null'] = value_counts.get('null', 0) + 1

    # Plot the pie chart for the distribution of categories in feature_name
    labels = list(value_counts.keys())
    values = list(value_counts.values())

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig.update_layout(title_text=f'Distribution of categories in {feature_name}')
    fig.show()
    
    # One-hot encoding
    # Find unique values
    unique_values = set()
    for item in data:
        if feature_name in item and isinstance(item[feature_name], list):
            unique_values.update(item[feature_name])

    for item in data:
        if feature_name in item and isinstance(item[feature_name], list):
            encoded_features = {f'{feature_name}_{i}': int(i in item[feature_name]) for i in unique_values}
            item.update(encoded_features)
            del item[feature_name]

    # # Fill missing features with -1
    # for item in data:
    #     for unique in unique_values:
    #         if f'{feature_name}_{unique}' not in item:
    #             item[f'{feature_name}_{unique}'] = -1

    return data



def process_multiplayer_modes(data):
    # Initialize new features as 0 for each item in the data
    for item in data:
        item['multiplayer_modes_offlinecoop'] = 0
        item['multiplayer_modes_onlinecoop'] = 0

        # Check if 'multiplayer_modes' exists in the item
        if 'multiplayer_modes' in item:
            for mode in item['multiplayer_modes']:
                # Proceed if 'platform' exists and its value is 6
                if 'platform' in mode and mode['platform'] == 6:
                    # For offlinecoop: set to 1 if true, otherwise remain 0
                    item['multiplayer_modes_offlinecoop'] = int(mode.get('offlinecoop', False))
                    # For onlinecoop: set to 1 if true, otherwise remain 0
                    item['multiplayer_modes_onlinecoop'] = int(mode.get('onlinecoop', False))
            
            # Delete the original 'multiplayer_modes' feature to clean up the data
            del item['multiplayer_modes']

    return data



def process_language_supports(data):
    # Determine total language support and collect unique language support types
    language_support_types = set()

    for item in data:
        if 'language_supports' in item:
            item['total_language_support'] = len(set([lang['language'] for lang in item['language_supports']]))
            for support in item['language_supports']:
                language_support_types.add(support['language_support_type'])

    # Calculate unique language counts per support type for each game
    for item in data:
        if 'language_supports' in item:
            language_counts = {}
            for type in language_support_types:
                language_counts[type] = set()

            # Populate the sets with languages for each support type
            for support in item['language_supports']:
                language_counts[support['language_support_type']].add(support['language'])

            # Calculate and assign the count of unique languages for each support type to the item
            for type in language_support_types:
                item[f'unique_language_support_type_{type}'] = len(language_counts[type])

            del item['language_supports']

    return data



def process_game_localizations(data):
    # Set of all possible regions
    possible_regions = set([region['region'] for item in data for region in item.get('game_localizations', [])])

    # Initialize new features as False
    for item in data:
        for region in possible_regions:
            item[f'game_localizations_{region}'] = 0

        # If 'game_localizations' exists, set the corresponding new features to True
        if 'game_localizations' in item:
            for loc in item['game_localizations']:
                item[f'game_localizations_{loc["region"]}'] = 1

            # Delete the original 'game_localizations' feature
            del item['game_localizations']

    return data



def get_unique_values_count(data, feature_name):
    # Initialize a set to hold the unique values
    unique_values = set()

    # Iterate through each item in the data
    for item in data:
        # If the feature exists in the item
        if feature_name in item:
            # Add its values to the unique_values set
            unique_values.update(item[feature_name])

    # Return the count of unique values
    return len(unique_values)



def process_platforms(data):
    # Initialize a new feature as 1 (Done later)
    for item in data:
        # item['total_platforms_support'] = 1

        # If 'platforms' exists, assign the count of platforms to the new feature
        if 'platforms' in item:
            item['total_platforms_support'] = len(item['platforms'])
            # Delete the original 'platforms' feature
            del item['platforms']

    return data



def process_category(data):
    for item in data:
        if 'category' in item and item['category'] != 0:
            item['category'] = 1
    return data



def process_feature(data, feature_name):
    for item in data:
        # Check if the item has the specified feature
        if feature_name in item:
            # If the feature exists, set its value to 1
            item[feature_name] = 1
        else:
            # If the feature does not exist, set its value to 0
            item[feature_name] = 0
    return data



def process_timestamp(data, feature_name):
    for item in data:
        try:
            if feature_name in item:
                # Convert Unix timestamp to datetime
                timestamp = datetime.fromtimestamp(item[feature_name])
                # Convert datetime object to strings in the format "YYYY", "MM", and "DD", and then to integers
                item[f'{feature_name}_year'] = int(timestamp.strftime('%Y'))
                item[f'{feature_name}_month'] = int(timestamp.strftime('%m'))
                item[f'{feature_name}_day'] = int(timestamp.strftime('%d'))
                # After successful processing, delete the original feature
                del item[feature_name]
        except Exception as e:
            # If an error occurs, delete the problematic feature_name key from this item
            item.pop(feature_name, None)  # Remove the key if it exists, doing nothing if it doesn't
            print(f"Error processing {feature_name} for item {item['id']}: {e}")
    return data