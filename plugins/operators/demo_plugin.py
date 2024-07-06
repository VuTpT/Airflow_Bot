from airflow.models import BaseOperator
import logging as log
from airflow.utils.decorators import apply_defaults
# from airflow.plugins_manager import AirflowPlugin


class DataTransferOperator(BaseOperator):

    @apply_defaults
    def __init__(self, source_file_path, dest_file_path, delete_list, *args, **kwargs):

        self.source_file_path = source_file_path
        self.dest_file_path = dest_file_path
        self.delete_list = delete_list
        super().__init__(*args, **kwargs)

    def execute(self, context):

        sourceFile = self.source_file_path
        destinationFile = self.dest_file_path
        deleteList = self.delete_list

        log.info("### custom operator execution starts ###")
        log.info('source_file_path: %s', sourceFile)
        log.info('dest_file_path: %s', destinationFile)
        log.info('delete_list: %s', deleteList)

        fin = open(sourceFile)
        fout = open(destinationFile, "a")

        for line in fin:
            log.info('### reading line: %s', line)
            for word in deleteList:
                log.info('### matching string: %s', word)
                line = line.replace(word, "")

            log.info('### output line is: %s', line)
            fout.write(line)

        fin.close()
        fout.close()


# class DemoPlugin(AirflowPlugin):
#     name = 'dataTransfer'
#     operators = [DataTransferOperator]
