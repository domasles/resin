// ST7735 TFT screen communication (initialization and drawing the framebuffer)

#include "hardware/clocks.h"
#include "hardware/gpio.h"
#include "hardware/spi.h"

#include "pico/stdlib.h"

#include "resin_hw.h"

#define SPI_TFT_PORT spi0
#define SPI_TFT_CS   20
#define SPI_TFT_DC   22
#define SPI_TFT_RST  26

#define SPI_RX  16
#define SPI_TX  19
#define SPI_SCK 18

#define ST7735_SWRESET 0x01
#define ST7735_SLPOUT  0x11
#define ST7735_NORON   0x13
#define ST7735_INVOFF  0x20
#define ST7735_DISPON  0x29
#define ST7735_CASET   0x2A
#define ST7735_RASET   0x2B
#define ST7735_RAMWR   0x2C
#define ST7735_MADCTL  0x36
#define ST7735_COLMOD  0x3A

const uint8_t resin_palette_rgb[PALETTE_SIZE][3] = {
    {  0,   0,   0}, // 0: Black
    { 73,  80,  87}, // 1: Dark Gray
    {145, 151, 156}, // 2: Light Gray
    {248, 249, 250}, // 3: White
    {235,  44,  71}, // 4: Red
    {139,  65,  46}, // 5: Brown
    { 25, 177, 248}, // 6: Light Blue
    { 19,  21, 224}, // 7: Dark Blue
    {254, 230,  16}, // 8: Yellow
    {149, 140,  50}, // 9: Gold
    { 45, 225,  62}, // 10: Light Green
    { 29, 148,  16}, // 11: Dark Green
    {245, 109, 187}, // 12: Pink
    {170,  58, 197}, // 13: Purple
    {245, 113,  23}, // 14: Orange
    {  0,   0,   0}  // 15: Black
};

static inline void tft_cs_low(void)  { gpio_put(SPI_TFT_CS, 0); }
static inline void tft_cs_high(void) { gpio_put(SPI_TFT_CS, 1); }
static inline void tft_dc_low(void)  { gpio_put(SPI_TFT_DC, 0); }
static inline void tft_dc_high(void) { gpio_put(SPI_TFT_DC, 1); }

static void write_command(uint8_t cmd) {
    tft_dc_low();
    tft_cs_low();
    spi_write_blocking(SPI_TFT_PORT, &cmd, 1);
    tft_cs_high();
}

static void write_data(uint8_t data) {
    tft_dc_high();
    tft_cs_low();
    spi_write_blocking(SPI_TFT_PORT, &data, 1);
    tft_cs_high();
}

static void st7735_reset(void) {
    gpio_put(SPI_TFT_RST, 1);
    sleep_ms(10);
    gpio_put(SPI_TFT_RST, 0);
    sleep_ms(10);
    gpio_put(SPI_TFT_RST, 1);
    sleep_ms(10);
}

void rh_display_finish(void) {
    tft_cs_high();
    // SPI in 8-bit mode so commands register properly
    spi_set_format(SPI_TFT_PORT, 8, SPI_CPOL_0, SPI_CPHA_0, SPI_MSB_FIRST);
}

void rh_display_window_start(int x, int y, int w, int h) {
    // SPI in 8-bit mode so commands register properly
    spi_set_format(SPI_TFT_PORT, 8, SPI_CPOL_0, SPI_CPHA_0, SPI_MSB_FIRST);

    write_command(ST7735_CASET);
    tft_dc_high();

    uint8_t caset[] = {0x00, (uint8_t)x, 0x00, (uint8_t)(x + w - 1)};

    tft_cs_low();
    spi_write_blocking(SPI_TFT_PORT, caset, 4);
    tft_cs_high();

    write_command(ST7735_RASET);
    tft_dc_high();

    uint8_t raset[] = {0x00, (uint8_t)y, 0x00, (uint8_t)(y + h - 1)};

    tft_cs_low();
    spi_write_blocking(SPI_TFT_PORT, raset, 4);
    tft_cs_high();

    write_command(ST7735_RAMWR);
    tft_cs_low();
    tft_dc_high();

    // SPI tin 16-bit mode for DMA pixel transfers
    spi_set_format(SPI_TFT_PORT, 16, SPI_CPOL_0, SPI_CPHA_0, SPI_MSB_FIRST);
}

void rh_display_init(void) {
    gpio_init(17);
    gpio_set_dir(17, GPIO_OUT);
    gpio_put(17, 1);

    spi_init(SPI_TFT_PORT, 24000000);

    // SPI in 8-bit mode so commands register properly
    spi_set_format(SPI_TFT_PORT, 8, SPI_CPOL_0, SPI_CPHA_0, SPI_MSB_FIRST);

    gpio_set_function(SPI_RX, GPIO_FUNC_SPI);
    gpio_set_function(SPI_SCK, GPIO_FUNC_SPI);
    gpio_set_function(SPI_TX, GPIO_FUNC_SPI);

    gpio_init(SPI_TFT_CS);
    gpio_set_dir(SPI_TFT_CS, GPIO_OUT);
    gpio_put(SPI_TFT_CS, 1);

    gpio_init(SPI_TFT_DC);
    gpio_set_dir(SPI_TFT_DC, GPIO_OUT);
    gpio_put(SPI_TFT_DC, 0);

    gpio_init(SPI_TFT_RST);
    gpio_set_dir(SPI_TFT_RST, GPIO_OUT);
    gpio_put(SPI_TFT_RST, 0);

    st7735_reset();

    write_command(ST7735_SWRESET);
    sleep_ms(150);

    write_command(ST7735_SLPOUT);
    sleep_ms(120);

    write_command(ST7735_COLMOD);
    write_data(0x05);

    write_command(ST7735_MADCTL);
    write_data(0x60);

    write_command(ST7735_INVOFF);

    rh_display_window_start(0, 0, RESIN_W, RESIN_H);

    uint16_t zero = 0x0000;

    for (uint32_t i = 0; i < RESIN_BUFSIZE; i++) {
        spi_write16_blocking(SPI_TFT_PORT, &zero, 1);
    }

    rh_display_finish();

    write_command(ST7735_NORON);
    sleep_ms(10);
    write_command(ST7735_DISPON);
    sleep_ms(100);
}

void rh_display_madctl(uint8_t value) {
    write_command(ST7735_MADCTL);
    write_data(value);
}
