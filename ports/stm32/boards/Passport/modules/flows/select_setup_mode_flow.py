# SPDX-FileCopyrightText: 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# select_setup_mode_flow.py - The main overall flow for Envoy setup - controls the process

import lvgl as lv
from flows import Flow
import common
import microns


class SelectSetupModeFlow(Flow):
    def __init__(self):
        super().__init__(initial_state=self.show_welcome, settings_key='setup_flow', name='SelectSetupModeFlow')
        self.restore()

        setup_mode = common.settings.get('setup_mode')
        if setup_mode is not None and setup_mode.endswith('done'):
            self.set_result(True)
            return

        self.statusbar = {'title': 'PASSPORT SETUP', 'icon': lv.ICON_SETUP}

    async def show_welcome(self):
        from pages import BrandmarkPage, ShutdownPage

        result = await BrandmarkPage(
            text='Welcome to Passport\n\nCongratulations on taking custody of your Bitcoin ' +
            'and reclaiming your sovereignty!',
            statusbar={'title': 'WELCOME', 'icon': lv.ICON_HOME},
            left_micron=microns.Shutdown,
            right_micron=microns.Forward).show()
        if result:
            self.goto(self.select_mode)
        else:
            await ShutdownPage().show()

    async def select_mode(self):
        from pages import SetupModeChooserPage

        setup_mode = common.settings.get('setup_mode')
        if setup_mode is None:
            setup_mode = await SetupModeChooserPage(left_micron=microns.Back).show()
            if setup_mode is None:
                self.back()
                return
            common.settings.set('setup_mode', setup_mode)

        if setup_mode is 'envoy':
            self.goto(self.show_envoy_mode)
        elif setup_mode is 'manual':
            self.goto(self.show_manual_mode)
        else:
            # The "done" cases end here so that we end up skipping this once it's been completed
            self.set_result(False)

    async def show_envoy_mode(self):
        from flows import EnvoySetupFlow

        result = await EnvoySetupFlow().run()
        if not result:
            common.settings.remove('setup_mode')
            self.back()
            return
        common.settings.set('setup_mode', 'envoy_done')
        self.set_result(True, forget_state=True)

    async def show_manual_mode(self):
        from flows import ManualSetupFlow

        result = await ManualSetupFlow().run()
        if not result:
            common.settings.remove('setup_mode')
            self.back()
            return
        common.settings.set('setup_mode', 'manual_done')
        self.set_result(True, forget_state=True)
