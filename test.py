import json
import unittest
from troposphere import Template
from creator import stack

ENV = "Production"

# create template with Production parameter
template = stack.create_template(Template(), ENV)

# read out the saved version of reference template
expected_template_file_name = "test_templates/test-template-production.json"
with open(expected_template_file_name, 'r') as fd:
    expected_template = fd.read()

class TestFirewallStack(unittest.TestCase):

  def test_stack(self):
      self.assertEqual(template.to_dict(), json.loads(expected_template))

