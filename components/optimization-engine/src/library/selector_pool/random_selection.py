# Randomized mock selection baseline for demo purposes
# Anestis Dalgkitsis | v1.3

# Modules
import random

def spinwheel(models):

    # Filter the enabled algorithms
    enabled_models = [name for name, details in models.items() if details["enabled"]]
    
    if not enabled_models:
        raise ValueError("No algorithms are enabled.")
    
    # Pick a random algorithm from the enabled ones
    return random.choice(enabled_models)

