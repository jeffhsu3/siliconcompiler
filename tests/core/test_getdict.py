# Copyright 2020 Silicon Compiler Authors. All Rights Reserved.
import siliconcompiler
from siliconcompiler.targets import freepdk45_demo
from siliconcompiler.schema import Parameter


def test_getdict():

    chip = siliconcompiler.Chip('test')
    chip.use(freepdk45_demo)
    localcfg = chip.getdict('pdk')

    glbl_key = Parameter.GLOBAL_KEY
    assert localcfg['freepdk45']['foundry']['node'][glbl_key][glbl_key]['value'] == 'virtual'
