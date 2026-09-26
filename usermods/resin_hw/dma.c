// DMA (direct memory access) communication
// Used for pushing CPU generated framebuffer to the screen without needing to interrupt CPU work

#include <string.h>

#include "hardware/dma.h"
#include "hardware/spi.h"

#include "pico/stdlib.h"

#include "resin_hw.h"

#define SPI_TFT_PORT spi0

static uint8_t raw_framebuffer[RESIN_BUFSIZE] __attribute__((aligned(4)));
static uint16_t dma_pixel_buffer[RESIN_BUFSIZE] __attribute__((aligned(4)));

static int dma_chan = -1;
static uint16_t palette_16bit[PALETTE_SIZE];

void rh_dma_init(void) {
    for (int i = 0; i < PALETTE_SIZE; i++) {
        uint8_t r = resin_palette_rgb[i][0];
        uint8_t g = resin_palette_rgb[i][1];
        uint8_t b = resin_palette_rgb[i][2];

        // RGB565 encoding
        uint16_t rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3);
        palette_16bit[i] = rgb565;
    }

    dma_chan = dma_claim_unused_channel(true);
    dma_channel_config c = dma_channel_get_default_config(dma_chan);

    channel_config_set_transfer_data_size(&c, DMA_SIZE_16);
    channel_config_set_read_increment(&c, true);
    channel_config_set_write_increment(&c, false);
    channel_config_set_dreq(&c, spi_get_dreq(SPI_TFT_PORT, true));

    dma_channel_configure(dma_chan, &c, &spi_get_hw(SPI_TFT_PORT)->dr, NULL, 0, false);
}

uint8_t *rh_dma_framebuffer(void) {
    return raw_framebuffer;
}

void rh_dma_clear(uint8_t color_idx) {
    memset(raw_framebuffer, color_idx & 0x0F, RESIN_BUFSIZE);
}

void rh_dma_send_window_indexed(int x, int y, int w, int h, const uint8_t *src_buf) {
    if (dma_channel_is_busy(dma_chan)) {
        dma_channel_wait_for_finish_blocking(dma_chan);

        while (spi_get_hw(SPI_TFT_PORT)->sr & SPI_SSPSR_BSY_BITS) {
            tight_loop_contents();
        }

        rh_display_finish();
    }

    int total_pixels = w * h;
    uint16_t *dst = dma_pixel_buffer;

    for (int row = 0; row < h; row++) {
        for (int col = 0; col < w; col++) {
            uint8_t pixel = src_buf[(y + row) * RESIN_W + (x + col)];
            *dst++ = palette_16bit[pixel & 0x0F];
        }
    }

    rh_display_window_start(x, y, w, h);

    dma_channel_set_read_addr(dma_chan, dma_pixel_buffer, false);
    dma_channel_set_trans_count(dma_chan, total_pixels, true);
}

void rh_dma_present(void) {
    rh_dma_send_window_indexed(0, 0, RESIN_W, RESIN_H, raw_framebuffer);
}
