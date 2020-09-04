<script>
  import { websocketSend } from '@/services/websocket_handler';

  export default {
    data() {
      return {
        isExecutingRemotely: false,
      };
    },
    methods: {
      wsData(code, graphId) {
        return JSON.stringify({
          instruction: 'enqueue',
          data: {
            code,
            graphId,
          },
        });
      },
      onMessage(event) {
        console.log(event);
      },
      sendDataToCloudExecutor(code, graphId) {
        const message = this.wsData(code, graphId);
        websocketSend(message, this.onMessage);
      },
    },
  };
</script>
