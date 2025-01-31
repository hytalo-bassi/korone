"""
``korone.commands`` is responsible for starting Pyrogram's Client and
handling all the commands modules.
"""

# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2022 Victor Cebarros <https://github.com/victorcebarros>

import logging
from dataclasses import dataclass

from pyrogram import Client

from korone import constants
from korone.commands import modules

log = logging.getLogger(__name__)


@dataclass
class AppParameters:
    """Pyrogram's Client parameters."""

    api_hash: str
    api_id: str
    bot_token: str
    in_memory: bool = True
    ipv6: bool = False
    name: str = constants.DEFAULT_NAME
    workers: int = constants.DEFAULT_WORKERS


class App:
    """Handles Pyrogram's Client and Korone's Database."""

    def __init__(self, parameters: AppParameters):
        self.app: Client | None = None
        self.parameters: AppParameters = parameters

    def setup(self) -> None:
        """
        The setup function is called when the module is loaded. It creates a new
        Pyrogram Client object and stores it in self.app for later use.

        :param self: Access the attributes and methods of the class in python
        :return: None
        """
        log.debug("Creating Pyrogram Client object")
        self.app = Client(
            api_hash=self.parameters.api_hash,
            api_id=self.parameters.api_id,
            bot_token=self.parameters.bot_token,
            in_memory=self.parameters.in_memory,
            ipv6=self.parameters.ipv6,
            name=self.parameters.name,
            workers=self.parameters.workers,
        )

        log.debug("Loading modules")
        modules.load(self.app)

    def run(self) -> None:
        """
        The run function is the main entry point for the client. It is responsible
        for initializing and running the application, as well as handling any errors
        that may occur during execution.

        :param self: Access the attributes and methods of the class inside a method
        :return: None
        """
        if self.app is None:
            raise RuntimeError("App is not initialized!")

        log.info("Running client")
        self.app.run()
