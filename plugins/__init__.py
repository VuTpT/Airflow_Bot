# from __future__ import division, absolute_import, print_function
from airflow.plugins_manager import AirflowPlugin, plugins

from hooks.elastic.elastic_hook import ElasticHook
from operators.demo_plugin import DataTransferOperator


# Defining the plugin class
class AirflowElasticPlugin(AirflowPlugin):
    name = 'elastic'
    hooks = [ElasticHook]


class DataTransferOperatorPlugin(AirflowPlugin):
    name = 'dataTransfer'
    operators = [DataTransferOperator]
