from game.components.power_ups.power_up import PowerUp
from game.utils.constants import HEART

class MachineGun(PowerUp):
    def __init__(self):
        super().__init__(HEART, 'machine_gun')