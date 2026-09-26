#ifndef RESIN_HW_H
    #define RESIN_HW_H

    #include <stdint.h>

    #define RESIN_W 160
    #define RESIN_H 128
    #define RESIN_BUFSIZE (RESIN_W * RESIN_H)

    #define PALETTE_SIZE 16

    void rh_display_init(void);
    void rh_display_window_start(int x, int y, int w, int h);
    void rh_display_finish(void);
    void rh_display_madctl(uint8_t value);

    void rh_dma_init(void);
    void rh_dma_clear(uint8_t color_idx);
    void rh_dma_send_window_indexed(int x, int y, int w, int h, const uint8_t *src_buf);
    void rh_dma_present(void);

    void rh_input_init(void);

    void rh_cdc_init(void);
    void rh_cdc_push(uint8_t byte);

    extern const uint8_t resin_palette_rgb[PALETTE_SIZE][3];

    uint8_t *rh_dma_framebuffer(void);

    uint8_t rh_input_held(void);

    uint16_t rh_cdc_available(void);
    uint8_t rh_cdc_read(void);
#endif
