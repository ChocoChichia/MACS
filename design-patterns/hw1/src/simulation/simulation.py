import logging

from src.constraints.constraints import Constraints
from src.features.damage_feature import DamageComponent
from src.simulation.interfaces import ChaseEngine, EvolutionEngine, FightEngine

logger = logging.getLogger(__name__)


class Simulator:
    def __init__(
        self,
        evolution_engine: EvolutionEngine,
        chase_engine: ChaseEngine,
        fight_engine: FightEngine,
    ):
        self._evolution_engine = evolution_engine
        self._chase_engine = chase_engine
        self._fight_engine = fight_engine

    def run(self) -> None:
        predator: DamageComponent = self._evolution_engine.evolve_predator()
        prey: DamageComponent = self._evolution_engine.evolve_prey()

        logger.info("--- CHASE PHASE ---")
        prey_was_caught = self._chase_engine.chase(predator, prey)

        if prey_was_caught:
            logger.info("--- FIGHT PHASE ---")
            outcome = self._fight_engine.fight(predator, prey)
        else:
            outcome = Constraints.PREY_WON

        logger.info(f"\nFINAL OUTCOME: {outcome}\n")
