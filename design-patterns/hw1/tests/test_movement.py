import pytest

from src.creature import Creature
from src.move import move_strategies
from src.move.move_handlers import MovementHandler
from src.simulation.movement_selector import build_default_movement_chain


@pytest.fixture
def movement_chain() -> MovementHandler:
    return build_default_movement_chain()


def test_selects_fly_strategy(movement_chain: MovementHandler) -> None:
    creature = Creature(wings=2, legs=2, stamina=100)
    strategy = movement_chain.handle(creature)
    assert isinstance(strategy, move_strategies.FlyStrategy)


def test_falls_back_to_run_strategy_from_low_stamina(
    movement_chain: MovementHandler,
) -> None:
    creature = Creature(wings=2, legs=2, stamina=79)
    strategy = movement_chain.handle(creature)
    assert isinstance(strategy, move_strategies.RunStrategy)


def test_falls_back_to_run_strategy_from_no_wings(
    movement_chain: MovementHandler,
) -> None:
    creature = Creature(wings=0, legs=2, stamina=100)
    strategy = movement_chain.handle(creature)
    assert isinstance(strategy, move_strategies.RunStrategy)


def test_falls_back_to_walk_strategy(movement_chain: MovementHandler) -> None:
    creature = Creature(wings=0, legs=2, stamina=59)
    strategy = movement_chain.handle(creature)
    assert isinstance(strategy, move_strategies.WalkStrategy)


def test_falls_back_to_hop_strategy(movement_chain: MovementHandler) -> None:
    creature = Creature(wings=0, legs=1, stamina=39)
    strategy = movement_chain.handle(creature)
    assert isinstance(strategy, move_strategies.HopStrategy)


def test_falls_back_to_crawl_strategy(movement_chain: MovementHandler) -> None:
    creature = Creature(wings=0, legs=0, stamina=19)
    strategy = movement_chain.handle(creature)
    assert isinstance(strategy, move_strategies.CrawlStrategy)


def test_selects_no_strategy_when_exhausted(movement_chain: MovementHandler) -> None:
    creature = Creature(wings=2, legs=2, stamina=0)
    strategy = movement_chain.handle(creature)
    assert isinstance(strategy, move_strategies.NoStrategy)
