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
#ifndef LV_ATTRIBUTE_IMG_ICON_PAGE_QR_SM
#define LV_ATTRIBUTE_IMG_ICON_PAGE_QR_SM
#endif
const LV_ATTRIBUTE_MEM_ALIGN LV_ATTRIBUTE_IMG_ICON_PAGE_QR_SM uint8_t ICON_PAGE_QR_SM_map[] = {
  0x00, 0x00, 0x00, 0x00, 	/*Color of index 0*/
  0xfe, 0xfe, 0xfe, 0xf7, 	/*Color of index 1*/

  0x00, 
  0x78, 
  0x78, 
  0x78, 
  0x78, 
  0x00, 
  0x00, 
};

const lv_img_dsc_t ICON_PAGE_QR_SM = {
  .header.cf = LV_IMG_CF_INDEXED_1BIT,
  .header.always_zero = 0,
  .header.reserved = 0,
  .header.w = 7,
  .header.h = 7,
  .data_size = 16,
  .data = ICON_PAGE_QR_SM_map,
};
