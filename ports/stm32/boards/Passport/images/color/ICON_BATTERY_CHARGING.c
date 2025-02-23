// SPDX-FileCopyrightText: 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
// SPDX-License-Identifier: GPL-3.0-or-later
//

#ifdef LV_LVGL_H_INCLUDE_SIMPLE
#include "lvgl.h"
#else
#include "lvgl/lvgl.h"
#endif

#ifndef LV_ATTRIBUTE_MEM_ALIGN
#define LV_ATTRIBUTE_MEM_ALIGN
#endif
#ifndef LV_ATTRIBUTE_IMG_ICON_BATTERY_CHARGING
#define LV_ATTRIBUTE_IMG_ICON_BATTERY_CHARGING
#endif
const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_IMG_ICON_BATTERY_CHARGING uint8_t ICON_BATTERY_CHARGING_map[] = {
  0x00, 0x00, 0x00, 0x00, 	/*Color of index 0*/
  0xff, 0xff, 0xff, 0x4c, 	/*Color of index 1*/
  0xfe, 0xfe, 0xfe, 0x97, 	/*Color of index 2*/
  0xfe, 0xfe, 0xfe, 0xf9, 	/*Color of index 3*/

  0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x40, 0x00, 0x00, 
  0x7f, 0xf1, 0xe3, 0xff, 0xd0, 
  0xff, 0xf2, 0xd3, 0xff, 0xf0, 
  0xf0, 0x07, 0xc0, 0x00, 0xf0, 
  0xf0, 0x0b, 0x80, 0x00, 0xfd, 
  0xf0, 0x0f, 0x94, 0x00, 0x7f, 
  0xf0, 0x0b, 0xfd, 0x00, 0x0f, 
  0xf0, 0x01, 0xbd, 0x00, 0x0f, 
  0xf0, 0x00, 0x7d, 0x00, 0x7f, 
  0xf0, 0x00, 0xb8, 0x00, 0xfd, 
  0xf0, 0x00, 0xf4, 0x00, 0xf0, 
  0xff, 0xf1, 0xf3, 0xff, 0xf0, 
  0x7f, 0xf2, 0xd3, 0xff, 0xd0, 
  0x00, 0x00, 0x40, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 
};

const lv_img_dsc_t ICON_BATTERY_CHARGING = {
  .header.cf = LV_IMG_CF_INDEXED_2BIT,
  .header.always_zero = 0,
  .header.reserved = 0,
  .header.w = 20,
  .header.h = 20,
  .data_size = 117,
  .data = ICON_BATTERY_CHARGING_map,
};
