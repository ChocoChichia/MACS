import logging

from src.constraints.constraints import Constraints
from src.simulation.chase_engine import GreedyChaseEngine
from src.simulation.evolution_engine import DefaultEvolutionEngine
from src.simulation.fight_engine import SimpleFightEngine
from src.simulation.simulation import Simulator


def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def main() -> None:
    setup_logging()
    evolution_engine = DefaultEvolutionEngine()
    chase_engine = GreedyChaseEngine()
    fight_engine = SimpleFightEngine()

    simulator = Simulator(
        evolution_engine=evolution_engine,
        chase_engine=chase_engine,
        fight_engine=fight_engine,
    )

    for i in range(1, Constraints.N_SIMULATION + 1):
        logging.info(f"==================== SIMULATION #{i} ====================")
        simulator.run()


if __name__ == "__main__":
    main()
