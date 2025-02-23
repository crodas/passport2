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
#ifndef LV_ATTRIBUTE_IMG_ICON_PASSPHRASE
#define LV_ATTRIBUTE_IMG_ICON_PASSPHRASE
#endif
const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_IMG_ICON_PASSPHRASE uint8_t ICON_PASSPHRASE_map[] = {
  0x00, 0x00, 0x00, 0x00, 	/*Color of index 0*/
  0xfe, 0xfe, 0xfe, 0x38, 	/*Color of index 1*/
  0xfe, 0xfe, 0xfe, 0xa9, 	/*Color of index 2*/
  0xfe, 0xfe, 0xfe, 0xdf, 	/*Color of index 3*/

  0x00, 0x01, 0x69, 0x40, 0x00, 
  0x05, 0x6f, 0xff, 0xf9, 0x40, 
  0x2f, 0xf9, 0x41, 0x6f, 0xf4, 
  0x2d, 0x40, 0x00, 0x01, 0x78, 
  0x28, 0x02, 0xbb, 0x40, 0x28, 
  0x28, 0x02, 0x96, 0xf0, 0x28, 
  0x28, 0x02, 0x80, 0x74, 0x28, 
  0x28, 0x02, 0x80, 0x34, 0x28, 
  0x28, 0x02, 0x80, 0xb4, 0x28, 
  0x28, 0x02, 0xee, 0xe0, 0x28, 
  0x28, 0x03, 0xa5, 0x40, 0x28, 
  0x1d, 0x02, 0x80, 0x00, 0x74, 
  0x1d, 0x02, 0x80, 0x00, 0xb4, 
  0x0b, 0x40, 0x00, 0x01, 0xd0, 
  0x06, 0x90, 0x00, 0x06, 0x90, 
  0x01, 0xa4, 0x00, 0x1a, 0x40, 
  0x00, 0x6d, 0x00, 0x79, 0x00, 
  0x00, 0x1b, 0x96, 0xe4, 0x00, 
  0x00, 0x01, 0xbb, 0x40, 0x00, 
  0x00, 0x00, 0x65, 0x00, 0x00, 
};

const lv_img_dsc_t ICON_PASSPHRASE = {
  .header.cf = LV_IMG_CF_INDEXED_2BIT,
  .header.always_zero = 0,
  .header.reserved = 0,
  .header.w = 20,
  .header.h = 20,
  .data_size = 117,
  .data = ICON_PASSPHRASE_map,
};
