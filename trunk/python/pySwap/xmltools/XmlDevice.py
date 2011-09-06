#########################################################################
#
# XmlDevice
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
__author__="Daniel Berenguer"
__date__ ="$Aug 20, 2011 10:36:00 AM$"
#########################################################################

from xmltools.XmlSettings import XmlSettings
from swap.SwapEndpoint import SwapEndpoint
from swap.SwapCfgParam import SwapCfgParam
from swap.SwapRegister import SwapRegister
from swap.SwapValue import SwapValue
from swap.SwapDefs import SwapType

import os
import xml.etree.ElementTree as xml

class XmlDevice(object):
    """
    Device configuration settings
    """

    def getDefinition(self):
        """
        Read current config file
        """
        # Parse XML file
        tree = xml.parse(self.fileName)
        if tree is None:
            return
        # Get the root node
        root = tree.getroot()
        # Get manufacturer
        elem = root.find("developer")
        if elem is not None:
            self.manufacturer = elem.text
        # Get product name
        elem = root.find("product")
        if elem is not None:
            self.product = elem.text
        # Get Power Down flag
        elem = root.find("pwrdownmode")
        if elem is not None:
            self.pwrDownMode = (elem.text.lower() == "True")


    def getRegList(self, config=False):
        """
        Return list of registers

        'config'  Set to True in case of config registers. False for regular ones

        Return list of registers
        """
        # List of config registers belonging to the current device
        lstRegs = []

        # Parse XML file
        tree = xml.parse(self.fileName)
        if tree is None:
            return
        # Get the root node
        root = tree.getroot()
        # Get manufacturer

        # List of register elements belonging to the device
        type = "regular"
        if config == True:
            type = "config"
        lstElemReg = root.findall(type + "/reg")
        if lstElemReg is not None:
            for reg in lstElemReg:
                # Get register id
                strRegId = reg.get("id")
                if strRegId is not None:
                    regId = int(strRegId)
                    # Get register description
                    elem = reg.find("description")
                    regDescr = ""
                    if elem is not None:
                        regDescr = elem.text
                    # Create register from id and mote
                    swRegister = SwapRegister(self.mote, regId, regDescr)

                    # Initial position and sizes
                    maxParamPosByte = 0
                    maxParamPosBit = 0
                    paramSizeByte = 0
                    paramSizeBit = 0
                    # List of endpoints belonging to the register
                    if config == True:
                        elementName = "param"
                    else:
                        elementName = "endpoint"
                    lstElemParam = reg.findall(elementName)
                    for param in lstElemParam:
                        # Read XML fields
                        paramType = param.get("type", default="num")
                        paramDir = param.get("dir", default="inp")
                        elem = param.find("description")
                        paramDescr = ""
                        if elem is not None:
                            paramDescr = elem.text
                        paramPos = "0"
                        elem = param.find("position")
                        if elem is not None:
                            paramPos = elem.text
                        paramSize = "1"
                        elem = param.find("size")
                        if elem is not None:
                            paramSize = elem.text
                        paramDef = "0"
                        elem = param.find("default")
                        if elem is not None:
                            paramDef = elem.text
                        if paramType in [SwapType.NUMBER, SwapType.BINARY]:
                            try:
                                defVal = int(paramDef)
                            except ValueError:
                                raise SwapExeption("Default value " + str(paramDef) + " is not an integer")
                                return
                        else:
                            defVal = paramDef

                        if config == True:
                            # Create SWAP config parameter
                            swParam = SwapCfgParam(register=swRegister, pType=paramType, description=paramDescr,
                                            position=paramPos, size=paramSize, default=defVal)
                        else:
                            # Create SWAP endpoint
                            swParam = SwapEndpoint(register=swRegister, pType=paramType, direction=paramDir, description=paramDescr,
                                            position=paramPos, size=paramSize, default=defVal)

                        # Add current parameter to the register
                        swRegister.add(swParam)

                    # Create empty value for the register
                    swRegister.value = SwapValue([0] * swRegister.getLength())
                    swRegister.update()                    
                    # Add endpoint to the list
                    lstRegs.append(swRegister)

        if len(lstRegs) == 0:
            return None
        else:
            return lstRegs


    def __init__(self, mote=None, manufId=None, prodId=None):
        """ Class constructor """
        # Device (mote) owner of the current register
        self.mote = mote
        # Name/path of the current configuration file
        self.fileName = None
        if manufId is not None and prodId is not None:
            self.fileName = XmlSettings.deviceDir + os.sep + "{0:X}".format(manufId) + os.sep + "{0:X}".format(prodId) + ".xml"
        # Manufacturer name
        self.manufacturer = None
        # Product name
        self.product = None
        # Power down mode (True or False)
        self.pwrDownMode = False

        if self.mote is not None:
            self.fileName = XmlSettings.deviceDir + os.sep + "{0:X}".format(self.mote.manufacturerId) + os.sep + "{0:X}".format(self.mote.productId) + ".xml"

        # Read definition parameters from XML file
        self.getDefinition()

