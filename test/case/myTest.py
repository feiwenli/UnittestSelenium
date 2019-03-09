# -*- coding=utf-8 -*-

class Fat(object):

    def test01(self):
        self.te01 = '01'



class Sun(Fat):

    def test01(self):
        super().test01()

    def test02(self):
        print(self.te01)


Sun().test02()