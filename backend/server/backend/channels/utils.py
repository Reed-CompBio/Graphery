import threading
from queue import Queue
from typing import Mapping

from channels.consumer import SyncConsumer

from bundle.server_utils.main_functions import time_out_execute
from bundle.server_utils.utils import create_error_response


class ProcessHandler:
    def __init__(self):
        self.lock = threading.Lock()
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
            return time_out_execute(code=code,
                                    graph_json=graph_json_obj)
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
