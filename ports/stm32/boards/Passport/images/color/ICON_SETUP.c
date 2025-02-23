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
#ifndef LV_ATTRIBUTE_IMG_ICON_SETUP
#define LV_ATTRIBUTE_IMG_ICON_SETUP
#endif
const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_IMG_ICON_SETUP uint8_t ICON_SETUP_map[] = {
  0x00, 0x00, 0x00, 0x00, 	/*Color of index 0*/
  0xff, 0xff, 0xff, 0x22, 	/*Color of index 1*/
  0xfe, 0xfe, 0xfe, 0x9e, 	/*Color of index 2*/
  0xfe, 0xfe, 0xfe, 0xe4, 	/*Color of index 3*/

  0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x6b, 0x90, 0x00, 0x00, 
  0x00, 0xbe, 0xf8, 0x00, 0x00, 
  0x00, 0x7d, 0x6e, 0x00, 0x00, 
  0x19, 0x1f, 0x4b, 0x40, 0x00, 
  0x2f, 0x47, 0xd7, 0x80, 0x00, 
  0x2f, 0xd2, 0xd2, 0xc0, 0x00, 
  0x2d, 0xfb, 0x82, 0xc0, 0x00, 
  0x2d, 0x7e, 0x03, 0x80, 0x00, 
  0x1e, 0x04, 0x07, 0xd0, 0x00, 
  0x0b, 0x80, 0x11, 0xf4, 0x00, 
  0x02, 0xfa, 0xf4, 0x7d, 0x00, 
  0x00, 0x6f, 0xbd, 0x1f, 0x40, 
  0x00, 0x00, 0x1f, 0x47, 0xd0, 
  0x00, 0x00, 0x07, 0xd1, 0xf4, 
  0x00, 0x00, 0x01, 0xf4, 0x78, 
  0x00, 0x00, 0x00, 0x7d, 0x38, 
  0x00, 0x00, 0x00, 0x1f, 0xf8, 
  0x00, 0x00, 0x00, 0x06, 0xd0, 
  0x00, 0x00, 0x00, 0x00, 0x00, 
};

const lv_img_dsc_t ICON_SETUP = {
  .header.cf = LV_IMG_CF_INDEXED_2BIT,
  .header.always_zero = 0,
  .header.reserved = 0,
  .header.w = 20,
  .header.h = 20,
  .data_size = 117,
  .data = ICON_SETUP_map,
};
