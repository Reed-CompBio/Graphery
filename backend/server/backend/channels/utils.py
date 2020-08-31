import threading
from queue import Queue
from typing import Mapping

from channels.consumer import SyncConsumer

from bundle.server_utils.main_functions import time_out_execute
from bundle.server_utils.utils import create_error_response

import logging


class ProcessHandler:
    def __init__(self):
        self.lock = threading.Lock()
        self.processing_queue = Queue()
        self.executing_flag = False

    def is_executing(self) -> bool:
        with self.lock:
            return self.executing_flag

    def mark_executing(self) -> None:
        with self.lock:
            self.executing_flag = True

    def mark_not_executing(self) -> None:
        with self.lock:
            self.executing_flag = False

    def is_queue_empty(self) -> bool:
        return self.processing_queue.empty()

    def enqueue(self, consumer: SyncConsumer) -> None:
        self.processing_queue.put(consumer)
        self.notify()

    def dequeue(self) -> SyncConsumer:
        return self.processing_queue.get()

    def get_code(self, consumer: SyncConsumer) -> str:
        return consumer.get_code()

    def get_graph_json_obj(self, consumer: SyncConsumer) -> Mapping:
        return consumer.get_graph_json_obj()

    def should_execute(self, consumer: SyncConsumer) -> bool:
        return not consumer.is_closed

    def execute(self, code: str, graph_json_obj: Mapping) -> Mapping:
        if code and graph_json_obj:
            return time_out_execute(code=code,
                                    graph_json=graph_json_obj)
        return create_error_response('Cannot Read Code Or Graph Object')

    def executed(self, consumer: SyncConsumer, result_mapping: Mapping) -> None:
        consumer.executed(result_mapping)

    def start_executing(self) -> None:
        first_consumer = self.dequeue()
        if self.should_execute(consumer=first_consumer):
            code = self.get_code(first_consumer)
            graph_json_obj = self.get_graph_json_obj(first_consumer)
            result_mapping: Mapping = self.execute(code, graph_json_obj)

            self.executed(first_consumer, result_mapping)

    def coordinator(self) -> None:
        while not self.is_queue_empty():
            self.start_executing()
        self.mark_not_executing()

    def notify(self) -> None:
        if not self.is_executing():
            self.mark_executing()
            self.coordinator()


process_handler = ProcessHandler()
