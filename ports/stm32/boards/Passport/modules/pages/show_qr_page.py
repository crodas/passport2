# SPDX-FileCopyrightText: 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# show_qr_page.py - Show a QR code

import lvgl as lv
import microns
import common
from pages import Page
from views import QRCode
from styles.style import Stylize
from micropython import const
from data_codecs.qr_type import QRType
from data_codecs.qr_factory import make_qr_encoder
from constants import CARD_BORDER_WIDTH

_FRAME_TIME = const(300)

brightness_levels = [5, 25, 50, 75, 100]


class ShowQRPage(Page):
    """Show a page with a QR code for the user to scan"""

    def __init__(self,
                 qr_type=QRType.QR,
                 qr_args=None,
                 qr_data=None,
                 caption=None,
                 card_header=None,
                 statusbar=None,
                 left_micron=microns.Back,
                 right_micron=microns.Forward):
        super().__init__(card_header=card_header,
                         statusbar=statusbar,
                         left_micron=left_micron,
                         right_micron=right_micron)
        self.qr_type = qr_type
        self.qr_args = qr_args
        self.qr_data = qr_data
        self.caption = caption
        self.curr_fragment_len = 200

        self.qr_encoder = None
        self.prev_card_header = None
        self.prev_part = None
        self.prev_global_nav_keys = None
        self.timer = None

        self.prev_brightness = 100
        self.curr_brightness_idx = 0

        self.prev_card_descs = None
        self.prev_card_idx = common.ui.active_card_idx
        self.qr_size_idx = 2
        self.qr_card_descs = [
            {'page_micron': microns.PageQRSmall},
            {'page_micron': microns.PageQRMedium},
            {'page_micron': microns.PageQRLarge}
        ]

        self.set_size(lv.pct(100), lv.pct(100))

        with Stylize(self) as default:
            default.pad(top=4)
            default.pad_row(6)

        self.qrcode = QRCode()
        self.qrcode.set_width(lv.pct(100))
        self.qrcode.set_height(lv.pct(100))

        with Stylize(self.qrcode) as default:
            default.pad(left=CARD_BORDER_WIDTH, right=CARD_BORDER_WIDTH)
            default.align(lv.ALIGN.CENTER)
            default.flex_fill()
        self.add_child(self.qrcode)

        # Add the caption if provided
        if self.caption is not None:
            from views import Label
            from styles.colors import TEXT_GREY

            self.caption_label = Label(text=self.caption, color=TEXT_GREY, center=True)
            self.caption_label.set_size(lv.pct(100), lv.SIZE.CONTENT)
            with Stylize(self.caption_label) as default:
                default.pad(left=4, right=4)
            self.add_child(self.caption_label)

    def is_qr_resizable(self):
        return self.qr_type != QRType.QR

    def attach(self, group):
        super().attach(group)
        self.qrcode.attach(group)
        self.timer = lv.timer_create(lambda timer: self.update(), _FRAME_TIME, None)
        self.prev_card_header = common.ui.hide_card_header()

        if self.is_qr_resizable():

            self.prev_top_level = common.ui.set_is_top_level(False)
            common.keypad.set_intercept_key_cb(self.on_key)

            self.prev_card_descs = common.ui.set_micron_bar_cards(self.qr_card_descs, force_show=True)
            common.ui.set_micron_bar_active_idx(self.qr_size_idx)

        self.prev_part = None

        self.prev_brightness = common.system.get_screen_brightness(100)
        try:
            self.curr_brightness_idx = brightness_levels.index(self.prev_brightness)
        except ValueError:
            self.curr_brightness_idx = 4

    def detach(self):
        common.display.set_brightness(self.prev_brightness)

        if self.is_qr_resizable():
            # Restore the card descs and header, if they were overridden
            if self.prev_card_descs is not None:
                common.ui.set_micron_bar_cards(self.prev_card_descs, force_show=False)
                common.ui.set_micron_bar_active_idx(self.prev_card_idx)
                self.prev_card_descs = None

            common.keypad.set_intercept_key_cb(None)
            common.ui.set_is_top_level(self.prev_top_level)

        if self.prev_card_header is not None:
            common.ui.set_card_header(**self.prev_card_header, force_all=True)

        if self.timer is not None:
            self.timer._del()  # noqa
            self.timer = None

        self.qrcode.detach()

        super().detach()

    def on_key(self, key, pressed):
        from common import ui
        import passport
        is_sim = passport.IS_SIMULATOR

        if pressed:
            # TODO: Fix this so the keycodes are the same here
            if key == lv.KEY.RIGHT or (is_sim and key == 114):
                if self.qr_size_idx < 2:
                    self.qr_size_idx += 1
                    self.qr_encoder = None
                    ui.set_micron_bar_active_idx(self.qr_size_idx)
            elif key == lv.KEY.LEFT or (is_sim and key == 108):
                if self.qr_size_idx > 0:
                    self.qr_size_idx -= 1
                    self.qr_encoder = None
                    ui.set_micron_bar_active_idx(self.qr_size_idx)

            # Handle brightness changes
            elif key == lv.KEY.UP:
                if self.curr_brightness_idx < len(brightness_levels) - 1:
                    self.curr_brightness_idx += 1
                    common.display.set_brightness(brightness_levels[self.curr_brightness_idx])
            elif key == lv.KEY.DOWN:
                if self.curr_brightness_idx > 0:
                    self.curr_brightness_idx -= 1
                    common.display.set_brightness(brightness_levels[self.curr_brightness_idx])

    def update(self):
        if self.is_attached():
            if self.qr_encoder is None:
                self.qr_encoder = make_qr_encoder(self.qr_type, self.qr_args)
                # print('qr_size_idx={}'.format(self.qr_size_idx))
                self.curr_fragment_len = self.qr_encoder.get_max_len(self.qr_size_idx)
                # print('curr_fragment_len={}'.format(self.curr_fragment_len))
                self.qr_encoder.encode(self.qr_data, max_fragment_len=self.curr_fragment_len)
                self.qrcode.reset_sizing()

            part = self.qr_encoder.next_part()

            if part is None:
                return

            if self.qr_type != QRType.QR:
                part = part.upper()

            # TODO: Optimization: Don't update if the fragment is the
            #       same as last time (or, if possible, if part count == 1).
            if self.prev_part != part:
                self.prev_part = part
                data = part.encode('ascii')
                # print('data={}'.format(data))
                self.qrcode.update(data)
