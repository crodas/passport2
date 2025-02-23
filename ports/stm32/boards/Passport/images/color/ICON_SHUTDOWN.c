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
#ifndef LV_ATTRIBUTE_IMG_ICON_SHUTDOWN
#define LV_ATTRIBUTE_IMG_ICON_SHUTDOWN
#endif
const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_IMG_ICON_SHUTDOWN uint8_t ICON_SHUTDOWN_map[] = {
  0x00, 0x00, 0x00, 0x00, 	/*Color of index 0*/
  0xfe, 0xfe, 0xfe, 0x3e, 	/*Color of index 1*/
  0xfe, 0xfe, 0xfe, 0xb9, 	/*Color of index 2*/
  0xfe, 0xfe, 0xfe, 0xf3, 	/*Color of index 3*/

  0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x28, 0x00, 0x00, 
  0x00, 0x00, 0x28, 0x00, 0x00, 
  0x00, 0x00, 0x28, 0x00, 0x00, 
  0x00, 0x40, 0x28, 0x01, 0x00, 
  0x01, 0xd0, 0x28, 0x07, 0x40, 
  0x07, 0x90, 0x28, 0x06, 0xd0, 
  0x0b, 0x40, 0x28, 0x01, 0xd0, 
  0x0a, 0x00, 0x28, 0x00, 0xb0, 
  0x1d, 0x00, 0x28, 0x00, 0x74, 
  0x1d, 0x00, 0x24, 0x00, 0x74, 
  0x1d, 0x00, 0x00, 0x00, 0x74, 
  0x1d, 0x00, 0x00, 0x00, 0x74, 
  0x0a, 0x00, 0x00, 0x00, 0xe0, 
  0x07, 0x40, 0x00, 0x01, 0xd0, 
  0x02, 0xd0, 0x00, 0x07, 0xc0, 
  0x01, 0xf4, 0x00, 0x1e, 0x40, 
  0x00, 0x6f, 0x99, 0xf9, 0x00, 
  0x00, 0x06, 0xff, 0x90, 0x00, 
  0x00, 0x00, 0x14, 0x00, 0x00, 
};

const lv_img_dsc_t ICON_SHUTDOWN = {
  .header.cf = LV_IMG_CF_INDEXED_2BIT,
  .header.always_zero = 0,
  .header.reserved = 0,
  .header.w = 20,
  .header.h = 20,
  .data_size = 117,
  .data = ICON_SHUTDOWN_map,
};
