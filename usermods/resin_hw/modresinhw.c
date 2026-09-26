#include "py/objarray.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "resin_hw.h"

static bool initialized = false;

static mp_obj_t resin_hw_init(void) {
    if (initialized) return mp_const_none;

    rh_display_init();
    rh_dma_init();
    rh_input_init();
    rh_cdc_init();

    set_sys_clock_khz(270000, true);

    initialized = true;
    return mp_const_none;
}

static MP_DEFINE_CONST_FUN_OBJ_0(resin_hw_init_obj, resin_hw_init);

static mp_obj_t resin_hw_framebuffer(void) {
    if (!initialized) return mp_const_none;
    return mp_obj_new_bytearray_by_ref(RESIN_BUFSIZE, rh_dma_framebuffer());
}

static MP_DEFINE_CONST_FUN_OBJ_0(resin_hw_framebuffer_obj, resin_hw_framebuffer);

static mp_obj_t resin_hw_clear_screen(mp_obj_t color_obj) {
    if (!initialized) return mp_const_none;

    uint8_t color = (uint8_t)mp_obj_get_int(color_obj);
    rh_dma_clear(color);

    return mp_const_none;
}

static MP_DEFINE_CONST_FUN_OBJ_1(resin_hw_clear_screen_obj, resin_hw_clear_screen);

static mp_obj_t resin_hw_present(void) {
    if (!initialized) return mp_const_none;
    rh_dma_present();

    return mp_const_none;
}

static MP_DEFINE_CONST_FUN_OBJ_0(resin_hw_present_obj, resin_hw_present);

static mp_obj_t resin_hw_get_input(void) {
    if (!initialized) return MP_OBJ_NEW_SMALL_INT(0);
    return MP_OBJ_NEW_SMALL_INT(rh_input_held());
}

static MP_DEFINE_CONST_FUN_OBJ_0(resin_hw_get_input_obj, resin_hw_get_input);

static mp_obj_t resin_hw_get_ms(void) {
    return MP_OBJ_NEW_SMALL_INT(mp_hal_ticks_ms());
}

static MP_DEFINE_CONST_FUN_OBJ_0(resin_hw_get_ms_obj, resin_hw_get_ms);

static mp_obj_t resin_hw_set_madctl(mp_obj_t value) {
    if (!initialized) return mp_const_none;
    rh_display_madctl((uint8_t)mp_obj_get_int(value));

    return mp_const_none;
}

static MP_DEFINE_CONST_FUN_OBJ_1(resin_hw_set_madctl_obj, resin_hw_set_madctl);

static const mp_rom_map_elem_t resin_hw_module_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_resin_hw)},
    {MP_ROM_QSTR(MP_QSTR_WIDTH), MP_ROM_INT(RESIN_W)},
    {MP_ROM_QSTR(MP_QSTR_HEIGHT), MP_ROM_INT(RESIN_H)},
    {MP_ROM_QSTR(MP_QSTR_init), MP_ROM_PTR(&resin_hw_init_obj)},
    {MP_ROM_QSTR(MP_QSTR_framebuffer), MP_ROM_PTR(&resin_hw_framebuffer_obj)},
    {MP_ROM_QSTR(MP_QSTR_clear_screen), MP_ROM_PTR(&resin_hw_clear_screen_obj)},
    {MP_ROM_QSTR(MP_QSTR_present), MP_ROM_PTR(&resin_hw_present_obj)},
    {MP_ROM_QSTR(MP_QSTR_get_input), MP_ROM_PTR(&resin_hw_get_input_obj)},
    {MP_ROM_QSTR(MP_QSTR_get_ms), MP_ROM_PTR(&resin_hw_get_ms_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_madctl), MP_ROM_PTR(&resin_hw_set_madctl_obj)},
};

static MP_DEFINE_CONST_DICT(resin_hw_module_globals, resin_hw_module_globals_table);

const mp_obj_module_t resin_hw_module = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&resin_hw_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR_resin_hw, resin_hw_module);
