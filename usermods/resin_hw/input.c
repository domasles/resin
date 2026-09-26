// Button handling - buttons are pull-up, active-low, triggered by interrupts.
//
// Button API indices:
//   W=0
//   A=1
//   S=2
//   D=3
//   I=4
//   J=5
//   K=6
//   L=7
// 
// Pin map for Sprig's PCB:
//   W=5
//   A=6
//   S=7
//   D=8
//   I=12
//   J=13
//   K=14
//   L=15

#include "hardware/gpio.h"
#include "hardware/sync.h"
#include "hardware/irq.h"

#include "pico/stdlib.h"

#include "resin_hw.h"

static const uint8_t button_pins[8] = {5, 6, 7, 8, 12, 13, 14, 15};

void rh_input_init(void) {
    for (int i = 0; i < 8; i++) {
        gpio_init(button_pins[i]);

        gpio_set_dir(button_pins[i], GPIO_IN);
        gpio_pull_up(button_pins[i]);
    }
}

uint8_t rh_input_held(void) {
    uint8_t held = 0;

    for (int i = 0; i < 8; i++) {
        if (!gpio_get(button_pins[i])) {
            held |= (uint8_t)(1u << i);
        }
    }

    return held;
}
