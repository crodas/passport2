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
#ifndef LV_ATTRIBUTE_IMG_ICON_PIN
#define LV_ATTRIBUTE_IMG_ICON_PIN
#endif
const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_IMG_ICON_PIN uint8_t ICON_PIN_map[] = {
  0x00, 0x00, 0x00, 0x00, 	/*Color of index 0*/
  0xfe, 0xfe, 0xfe, 0x3d, 	/*Color of index 1*/
  0xfe, 0xfe, 0xfe, 0x98, 	/*Color of index 2*/
  0xfe, 0xfe, 0xfe, 0xec, 	/*Color of index 3*/

  0x00, 0x00, 0x14, 0x00, 0x00, 
  0x00, 0x02, 0xbf, 0x40, 0x00, 
  0x00, 0x0b, 0xa7, 0xe0, 0x00, 
  0x00, 0x1e, 0x00, 0xb4, 0x00, 
  0x00, 0x3c, 0x00, 0x38, 0x00, 
  0x00, 0x38, 0x00, 0x2c, 0x00, 
  0x00, 0x38, 0x00, 0x2c, 0x00, 
  0x00, 0x38, 0x00, 0x2c, 0x00, 
  0x01, 0xbe, 0xaa, 0xbe, 0x40, 
  0x0b, 0xff, 0xff, 0xff, 0xe0, 
  0x0e, 0x00, 0x00, 0x00, 0xb0, 
  0x0e, 0x00, 0x00, 0x00, 0xb0, 
  0x0e, 0x10, 0x41, 0x04, 0xb0, 
  0x0e, 0x79, 0xe7, 0x9e, 0xb0, 
  0x0e, 0x75, 0xd7, 0x5d, 0xb0, 
  0x0e, 0x00, 0x00, 0x00, 0xb0, 
  0x0e, 0x00, 0x00, 0x00, 0xb0, 
  0x0b, 0x99, 0x99, 0x99, 0xf0, 
  0x07, 0xff, 0xff, 0xff, 0xd0, 
  0x00, 0x55, 0x55, 0x55, 0x00, 
};

const lv_img_dsc_t ICON_PIN = {
  .header.cf = LV_IMG_CF_INDEXED_2BIT,
  .header.always_zero = 0,
  .header.reserved = 0,
  .header.w = 20,
  .header.h = 20,
  .data_size = 117,
  .data = ICON_PIN_map,
};
