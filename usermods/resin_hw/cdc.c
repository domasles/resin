// TinyUSB bridge for data transfer (future implementation for sending games, may change).

#include "resin_hw.h"

#define RH_CDC_RING_SIZE 2048

static uint8_t ring[RH_CDC_RING_SIZE];

static volatile uint16_t head;
static volatile uint16_t tail;

void rh_cdc_init(void) {
    head = tail = 0;
}

void rh_cdc_push(uint8_t byte) {
    uint16_t next = (head + 1) % RH_CDC_RING_SIZE;

    if (next == tail) return;  // Buffer full

    ring[head] = byte;
    head = next;
}

uint16_t rh_cdc_available(void) {
    return (uint16_t)((head - tail + RH_CDC_RING_SIZE) % RH_CDC_RING_SIZE);
}

uint8_t rh_cdc_read(void) {
    if (head == tail) return 0;  // Buffer empty guard

    uint8_t byte = ring[tail];
    tail = (tail + 1) % RH_CDC_RING_SIZE;
    return byte;
}
