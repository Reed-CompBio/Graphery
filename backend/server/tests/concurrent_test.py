import time

import websockets
import asyncio
from multiprocessing import Process


async def websocket_req(url, data, serial):
    async with websockets.connect(url) as websocket:
        await websocket.send(data)
        print(serial, ': ', await websocket.recv())
        print(serial, ': ', await websocket.recv())


def send_request(url, data, serial):
    asyncio.run(websocket_req(url, data, serial))


def main():
    print('start create')
    url = 'ws://127.0.0.1:8082/ws'
    data = r'''{"instruction": "enqueue", "data":{"code":"# python 3.8 \nfrom bundle.seeker import tracer\nfrom bundle.utils.dummy_graph import graph_object\n\n\n# variables whose names are in the trancer will be displayed\n@tracer('greeting', 'a_node', 'an_edge')\ndef main() -> None:\n    # since greeting is in `tracer`, it's value will be shown\n    greeting: str = 'hello world :)'\n    greeting = 'Welcome to Graphery!'\n\n    # graph elements are stored in the `graph_object`\n    # nodes can be referenced by `graph_object.nodes` or `graph_object.V`\n    a_node = graph_object.nodes[0]\n    not_traced_node = graph_object.V[1]\n\n    # Similarly, edges can be referenced by `graph_object.edges` or `graph_object.E`\n    an_edge = graph_object.edges[1]\n    not_traced_edge = graph_object.E[0]\n", "graph_id": "784e203f-0754-4044-80e2-5d398ab0edf9"}}'''
    time.sleep(1)
    for i in range(300):
        p = Process(target=send_request, args=[url, data, i])
        p.start()
        print('requested ', i)


if __name__ == '__main__':
    main()
