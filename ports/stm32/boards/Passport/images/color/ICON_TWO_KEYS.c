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
#ifndef LV_ATTRIBUTE_IMG_ICON_TWO_KEYS
#define LV_ATTRIBUTE_IMG_ICON_TWO_KEYS
#endif
const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_IMG_ICON_TWO_KEYS uint8_t ICON_TWO_KEYS_map[] = {
  0x00, 0x00, 0x00, 0x00, 	/*Color of index 0*/
  0xff, 0xff, 0xff, 0x24, 	/*Color of index 1*/
  0xfe, 0xfe, 0xfe, 0x77, 	/*Color of index 2*/
  0xfe, 0xfe, 0xfe, 0xea, 	/*Color of index 3*/

  0x00, 0x00, 0x00, 0x14, 0x00, 
  0x00, 0x00, 0x00, 0xbc, 0x00, 
  0x00, 0x00, 0x02, 0xf4, 0x00, 
  0x00, 0x00, 0x0b, 0xf8, 0x00, 
  0x00, 0x00, 0x2e, 0x7e, 0x00, 
  0x00, 0x50, 0xbf, 0xbd, 0x14, 
  0x1b, 0xfe, 0xeb, 0xf4, 0x7d, 
  0x3e, 0xaf, 0x81, 0x91, 0xf8, 
  0xb8, 0x07, 0xc0, 0x07, 0xfd, 
  0xf0, 0x02, 0xd0, 0x1f, 0x6f, 
  0xe0, 0x01, 0xe0, 0x7f, 0x7d, 
  0xb4, 0x0b, 0xfe, 0xf7, 0xf4, 
  0xb9, 0x2f, 0xaf, 0xd1, 0x90, 
  0x2f, 0xff, 0x02, 0xd0, 0x00, 
  0x06, 0xf4, 0x01, 0xe0, 0x00, 
  0x00, 0xb0, 0x00, 0xe0, 0x00, 
  0x00, 0xb4, 0x01, 0xe0, 0x00, 
  0x00, 0x3e, 0x07, 0xc0, 0x00, 
  0x00, 0x1f, 0xff, 0x40, 0x00, 
  0x00, 0x02, 0xa9, 0x00, 0x00, 
};

const lv_img_dsc_t ICON_TWO_KEYS = {
  .header.cf = LV_IMG_CF_INDEXED_2BIT,
  .header.always_zero = 0,
  .header.reserved = 0,
  .header.w = 20,
  .header.h = 20,
  .data_size = 117,
  .data = ICON_TWO_KEYS_map,
};
