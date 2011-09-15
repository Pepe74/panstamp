#########################################################################
#
# pluginSwap
#
# Copyright (c) 2011 Daniel Berenguer <dberenguer@usapiens.com>
#
# This file is part of the panStamp project.
#
# panStamp  is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# panStamp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with panLoader; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA
#
#########################################################################
__author__ = "Daniel Berenguer"
__date__ = "$Sep 6, 2011 2:53:32 PM$"
__appname__ = "pluginSwap"
__version__ = "1.0"
#########################################################################

from SwapManager import SwapManager
from swapexception.SwapException import SwapException

from plugins.pluginapi import PluginAPI
from twisted.internet import reactor


if __name__ == "__main__":
    """
    Run SWAP daemon for HouseAgent"
    """
    # Start HouseAgent plugin
    pluginId = "d116c674-8d86-4fd4-9b7e-0cb8624dd90a"
    pluginapi = PluginAPI(pluginId, "SWAP")

    # SWAP stuff here...
    try:
        # Start SWAP manager tool
        manager = SwapManager(pluginapi, True, True)
    except SwapException as ex:
        ex.display()

    reactor.run()
