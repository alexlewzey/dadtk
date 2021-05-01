"""
Dungeons & Dragons tool-kit
A module containing functions that simulate/calculate dice-rolls/scores
"""
import statistics
from typing import *
import random
import functools

D20: int = 20


def roll_initiative() -> int:
    modifiers = {
        'init_bonus': 3,
        'widsom': 2,
    }
    roll = roll_vantage(D20, vantage='advantage')
    init = roll + sum(modifiers.values())
    print(f'init={init}, roll={roll}, {dict2str(modifiers)}')
    return init


def roll_attack(n: int = 2, vantage: Optional[str] = None) -> List:
    attacks = []
    for _ in range(n):
        modifiers = {
            'crossbow': 5,
            'fighting_style': 2,
        }
        if vantage:
            roll = roll_vantage(D20, vantage=vantage)
        else:
            roll = random.randint(1, D20)
        attack = roll + sum(modifiers.values())
        print(f'attack={attack}, roll={roll}, {dict2str(modifiers)}')
        attacks.append(attack)
    return attacks


def roll_damage(
        n: int = 2,
        d: int = 6,
        dread_ambush: bool = False,
        humanoid: bool = False,
        hunters_mark: bool = False,
        vantage: Optional[str] = None
) -> int:
    n = 3 if dread_ambush else n
    damages = []
    for i in range(n):
        modifers = {
            'crossbow': 3,
        }
        if humanoid: modifers['humanoid'] = 2
        if hunters_mark: modifers['hunters_mark'] = random.randint(1, 6)
        if dread_ambush and (i == 0): modifers['dread_ambush'] = random.randint(1, 8)

        if vantage:
            roll = roll_vantage(d, vantage=vantage)
        else:
            roll = random.randint(1, d)
        damage = roll + sum(modifers.values())
        damages.append(damage)
        print(f'damage={damage}, roll={roll}, {dict2str(modifers)}')
    total_damage = sum(damages)
    print(f'total_damage: {total_damage}')
    return total_damage


def roll_vantage(d: int, vantage: str) -> int:
    rolls = sorted([random.randint(1, d) for _ in range(2)], reverse=True)
    func = {
        'advantage': max,
        'disadvantage': min,
    }[vantage]
    roll = func(rolls)
    print(f'{vantage}={rolls}')
    return roll


def dict2str(modifiers):
    modifiers_str = ', '.join([f'{k}={v}' for k, v in modifiers.items()])
    return modifiers_str


def avg_roll(func: Callable) -> float:
    return statistics.mean([func() for _ in range(10_000)])


roll_initiative()

avg_roll(roll_initiative)

roll_attack(
    n=2,
    vantage=None
)

args = {
    'n': 2,
    'dread_ambush': True,
    'humanoid': True,
    'hunters_mark': True,
    'vantage': 'advantage',
}
roll_damage(**args)

roll_damage_partial = functools.partial(roll_damage, **args)
avg_roll(roll_damage_partial)
