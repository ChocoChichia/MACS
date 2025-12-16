class Constraints:
    # --- Simulation Parameters ---
    N_SIMULATION = 100

    # --- Outcome Messages ---
    PREDATOR_WON = "Some R Rated Things Have Happened :D"
    PREY_WON = "Pray Ran Into Infinity"

    # --- Creature Default Stats ---
    # Defines the starting state for any newly created creature.
    DEFAULT_STAMINA = 100
    DEFAULT_HEALTH = 100
    DEFAULT_POWER = 1
    DEFAULT_LOCATION = 0

    # --- Creature State Boundaries ---
    # Defines the valid operational range for creature stats.
    MAX_STAMINA = 100
    MIN_STAMINA = 0
    MAX_HEALTH = 100
    MIN_HEALTH = 0

    # --- Body Part Modifiers ---
    # Mapsc qualitative descriptions of parts to their in-game effect.
    CLAWS_MULTIPLIERS = {"SMALL": 2, "MEDIUM": 3, "BIG": 4}
    TEETH_ADDITIVES = {"DULL": 3, "SHARP": 6, "VICIOUS": 9}

    # --- Evolution Probabilities ---
    # Defines the weighted chances for different evolutionary outcomes.
    # The order of weights corresponds to the order of keys/choices.

    # Weapon weights [Small, Medium, Big] or [Dull, Sharp, Vicious]
    PREDATOR_CLAWS_WEIGHTS = [0.2, 0.3, 0.5]
    PREY_CLAWS_WEIGHTS = [0.5, 0.3, 0.2]

    PREDATOR_TEETH_WEIGHTS = [0.2, 0.3, 0.5]
    PREY_TEETH_WEIGHTS = [0.5, 0.3, 0.2]

    # Limb weights [0, 1, 2]
    PREDATOR_LEG_WEIGHTS = [0.1, 0.2, 0.7]
    PREY_LEG_WEIGHTS = [0.3, 0.4, 0.3]

    PREDATOR_WINGS_WEIGHTS = [0.3, 0.3, 0.4]
    PREY_WINGS_WEIGHTS = [0.6, 0.2, 0.2]

    # Special probability for Prey weapon evolution.
    PREY_CHANCE_TO_EVOLVE_WEAPON = 0.8
