# !/etc/bin/env python
# coding=utf-8

import unittest
from libs.vcenter import add_template

class TestTemplate(unittest.TestCase):

    def setUp(self):
        print "----> setup"

    def test_add_template(self):
        print "----> add template"
        template_name = 'shicheng_centos=6.4-64-8-8-60'
        sample_status = {
            "os_type": 'centos',
            "os_version": '6.4',
            "os_bit": 64,
            "cpu": 2,
            "ram": 8,
            "disk": 500,
            "username": 'shicheng',
            "password": '123456',
            "customer_id":'5f4a98d8-cbeb-496c-a65e-481cf3e49a32'
        }

        template_id = add_template(template_name, sample_status)
        print template_id
    def tearDown(self):
        print "----> tear down"
        pass

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestTemplate("test_add_template"))
    runner = unittest.TextTestRunner()
    runner.run(suite)