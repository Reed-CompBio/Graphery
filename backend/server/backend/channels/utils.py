import json
from urllib import request
from os import getenv
from queue import Queue
from typing import Mapping

from channels.consumer import SyncConsumer

from bundle.server_utils.utils import create_error_response
from bundle.server_utils.params import VERSION


_REMOTE_URL = getenv('GRAPHERY_REMOTE_EXECUTE_URL', 'http://localhost')


def post_request(url: str, data: Mapping[str, str]) -> Mapping:
    encoded_data = json.dumps(data).encode('UTF-8')
    req = request.Request(url, data=encoded_data,
                                 headers={'content-type': 'application/json'})
    return json.loads(request.urlopen(req).read().decode('UTF-8'))


class ProcessHandler:
    def __init__(self):
        self.processing_queue = Queue()

    def enqueue(self, consumer: SyncConsumer) -> None:
        self.processing_queue.put(consumer)
        self.coordinate()

    def dequeue(self) -> SyncConsumer:
        return self.processing_queue.get()

    @staticmethod
    def get_code(consumer: SyncConsumer) -> str:
        return consumer.get_code()

    @staticmethod
    def get_graph_json_obj(consumer: SyncConsumer) -> Mapping:
        return consumer.get_graph_json_obj()

    @staticmethod
    def should_execute(consumer: SyncConsumer) -> bool:
        return not consumer.is_closed

    @staticmethod
    def execute(code: str, graph_json_obj: Mapping) -> Mapping:
        if code and graph_json_obj:
            response = post_request(f'{_REMOTE_URL}:7590/run',
                                    data={'code': code,
                                          'graph': graph_json_obj,
                                          'version': VERSION})
            return response

        return create_error_response('Cannot Read Code Or Graph Object')

    @staticmethod
    def executed(consumer: SyncConsumer, result_mapping: Mapping) -> None:
        consumer.executed(result_mapping)

    def start_executing(self) -> None:
        first_consumer = self.dequeue()
        if self.should_execute(consumer=first_consumer):
            code = self.get_code(first_consumer)
            graph_json_obj = self.get_graph_json_obj(first_consumer)
            result_mapping: Mapping = self.execute(code, graph_json_obj)

            self.executed(first_consumer, result_mapping)

    def coordinate(self) -> None:
        self.start_executing()


process_handler = ProcessHandler()
