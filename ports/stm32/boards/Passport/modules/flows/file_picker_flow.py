# SPDX-FileCopyrightText: 2022 Foundation Devices, Inc. <hello@foundationdevices.com>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# file_picker_flow.py - Allow the user to pick a file and (optionally) navigate up/down folder hierarchy

import lvgl as lv
from animations.constants import TRANSITION_DIR_POP, TRANSITION_DIR_PUSH
from files import CardMissingError, CardSlot
from flows import Flow
from pages import FilePickerPage, StatusPage, InsertMicroSDPage
from styles.colors import COPPER
import microns
import common
from utils import get_file_list


class FilePickerFlow(Flow):
    def __init__(
            self, initial_path=None, show_folders=False, enable_parent_nav=False, suffix=None,
            filter_fn=None):
        super().__init__(initial_state=self.show_file_picker, name='FilePickerFlow: {}'.format(
            initial_path))
        self.paths = [initial_path]
        self.show_folders = show_folders
        self.enable_parent_nav = enable_parent_nav
        self.suffix = suffix
        self.filter_fn = filter_fn

    async def show_file_picker(self):
        # Get list of files/folders at the current path
        try:
            active_idx = len(self.paths) - 1
            active_path = self.paths[active_idx]
            files = get_file_list(
                active_path,
                include_folders=self.show_folders,
                include_parent=self.enable_parent_nav,
                suffix=self.suffix,
                filter_fn=self.filter_fn)

            def file_key(f):
                (filename, _fullpath, is_folder) = f
                return '{}::{}'.format('0' if is_folder else '1', filename.lower())

            files = sorted(files, key=file_key)

        except CardMissingError:
            self.goto(self.show_insert_microsd_error)
            return

        is_root = active_path == CardSlot.get_sd_root()
        if is_root:
            title = 'microSD'
            icon = lv.ICON_MICROSD
        else:
            leaf_folder_name = active_path.split('/')[-1]
            title = leaf_folder_name
            icon = lv.ICON_FOLDER

        if len(files) == 0:
            result = await StatusPage(
                text='No files found',
                card_header={'title': title, 'icon': icon},
                icon=lv.LARGE_ICON_ERROR,
                icon_color=COPPER,
                left_micron=microns.Back,
                right_micron=microns.Retry
            ).show()
            if not result:
                self.set_result(None)
                return
            else:
                # Refresh
                return
        else:
            result = await FilePickerPage(
                files=files,
                card_header={'title': title, 'icon': icon}

            ).show()

        # No file selected - go back to previous page
        if result is None:
            common.page_transition_dir = TRANSITION_DIR_POP
            if len(self.paths) <= 1:
                self.set_result(None)
            else:
                # Go back up a level
                self.paths.pop(-1)
            return

        _filename, full_path, is_folder = result
        if is_folder:
            common.page_transition_dir = TRANSITION_DIR_PUSH
            self.paths.append(full_path)
            return

        # User chose this file
        common.page_transition_dir = TRANSITION_DIR_POP
        self.set_result(result)

    async def show_insert_microsd_error(self):
        result = await InsertMicroSDPage().show()
        if not result:
            self.set_result(None)
        else:
            self.goto(self.show_file_picker)
