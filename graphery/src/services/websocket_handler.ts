import { BASE_SOCKET } from '@/services/api_entry';

let websocket: WebSocket | null;

function createNewWebsocket(): WebSocket {
  const socket = new WebSocket(BASE_SOCKET);
  socket.onopen = function(event) {
    console.debug(`new websocket opened: `, event);
  };
  socket.onclose = function(event) {
    console.debug(`websocket closed: `, event);
  };

  return socket;
}

export function establishWebsocketConnection(
  onMessage: ((this: WebSocket, ev: Event) => any) | null,
  onError: ((this: WebSocket, ev: Event) => any) | null,
  onOpen: ((this: WebSocket, ev: Event) => any) | null
): WebSocket {
  if (!websocket || websocket.readyState === WebSocket.CLOSED) {
    websocket = createNewWebsocket();
    websocket.onopen = onOpen;
  }
  websocket.onerror = onError;
  websocket.onmessage = onMessage;
  return websocket;
}

export function websocketSend(
  message: string,
  onMessage: ((this: WebSocket, ev: Event) => any) | null,
  onError: ((this: WebSocket, ev: Event) => any) | null,
  before: Function | undefined = undefined,
  after: Function | undefined = undefined
) {
  if (before) {
    before();
  }

  const socket = establishWebsocketConnection(onMessage, onError, function(
    event
  ) {
    this.send(message);
  });

  if (socket.readyState === WebSocket.OPEN) {
    socket.send(message);
  }

  if (after) {
    after();
  }
}
