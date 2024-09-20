import random

def generate_random_preference_profile(size):
    # Generate a list of indices based on the size input
    indices = list(range(1, size + 1))

    # Generate mpref and wpref by creating random permutations of the indices
    mpref = [random.sample(indices, size) for _ in range(size)]
    wpref = [random.sample(indices, size) for _ in range(size)]

    return {'mpref': mpref, 'wpref': wpref}


def profile_formatting(profile):
    formatted_profile = {'M': {}, 'W': {}}
    
    # Format Men's Preferences
    for i, prefs in enumerate(profile['mpref'], 1):
        # Each man's preferences will prefix 'W' to the women indices
        formatted_profile['M'][f'M{i}'] = [f'W{j}' for j in prefs]

    # Format Women's Preferences
    for i, prefs in enumerate(profile['wpref'], 1):
        # Each woman's preferences will prefix 'M' to the men indices
        formatted_profile['W'][f'W{i}'] = [f'M{j}' for j in prefs]
    
    return formatted_profile