#!/usr/bin/env python3
import pygame
import time
import sys
from collections import OrderedDict


class Joystick:
    def __init__(self, id):
        self.joystick = pygame.joystick.Joystick(id)
        self.joystick.init()

    def __enter__(self):
        self.update()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.joystick.quit()

    def update(self):
        pygame.event.get()
        for button_id in range(self.joystick.get_numbuttons()):
            setattr(self, 'button_' + str(button_id),
                    self.joystick.get_button(button_id))
        for hat_id in range(self.joystick.get_numhats()):
            setattr(self, 'hat_' + str(hat_id),
                    self.joystick.get_hat(hat_id))
        for axis_id in range(self.joystick.get_numaxes()):
            setattr(self, 'axis_' + str(axis_id),
                    self.joystick.get_axis(axis_id))

    def get_button_vals(self):
        buttons = {}
        for button_id in range(self.joystick.get_numbuttons()):
            value = getattr(self, 'button_' + str(button_id))
            buttons['button_' + str(button_id)] = value
        return buttons

    def get_hat_vals(self):
        hats = {}
        for hat_id in range(self.joystick.get_numhats()):
            value = getattr(self, 'hat_' + str(hat_id))
            hats['hat_' + str(hat_id)] = value
        return hats

    def get_axis_vals(self):
        axes = {}
        for axis_id in range(self.joystick.get_numaxes()):
            value = getattr(self, 'axis_' + str(axis_id))
            axes['axis_' + str(axis_id)] = value
        return axes

    def get_all_vals(self):
        all_vals = {}
        all_vals.update(self.get_hat_vals())
        all_vals.update(self.get_axis_vals())
        all_vals.update(self.get_button_vals())
        return all_vals


if __name__ == '__main__':
    pygame.init()
    pygame.joystick.init()

    # Findout which joystick to use as controller
    controller_ids = list(range(pygame.joystick.get_count()))
    print('# of controllers: {}'.format(len(controller_ids)))
    id = None
    if len(controller_ids) == 1:
        id = controller_ids[0]
    elif controller_ids:
        print('Possible ids: {}'.format(controller_ids))
        id = int(input('Enter one of the above ids: '))
    else:
        print('No controllers found, exiting...')
        pygame.joystick.quit()
        sys.exit(1)

    # Connect to and print joystick values
    print('Connecting to joystick {}'.format(id))
    with Joystick(id) as controller:
        while True:
            try:
                controller.update()
                all_vals = controller.get_all_vals()
                all_vals = OrderedDict(sorted(all_vals.items(), key=lambda d: d[0]))
                print(*all_vals.items(), sep='\n')
                time.sleep(0.05)
            except KeyboardInterrupt:
                break

    pygame.joystick.quit()
