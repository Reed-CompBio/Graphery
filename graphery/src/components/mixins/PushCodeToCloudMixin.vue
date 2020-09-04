<script>
  import { websocketSend } from '@/services/websocket_handler';
  import { errorDialog, warningDialog } from '@/services/helpers';

  export default {
    data() {
      return {
        isExecutingRemotely: false,
        timeStamp: null,
      };
    },
    methods: {
      startCloudExecuting() {
        this.isExecutingRemotely = true;
        this.timeStamp = new Date().getTime();
      },
      finishedCloudExecution() {
        this.isExecutingRemotely = false;
        this.timeStamp = null;
      },
      wsData(code, graphId) {
        return JSON.stringify({
          instruction: 'enqueue',
          data: {
            code,
            graphId,
            timeStamp: this.timeStamp,
          },
        });
      },
      onMessage(event) {
        console.log('on message event: ', event);
        const data = JSON.parse(event.data);
        switch (data.type) {
          case 'waiting':
            this.onWaiting(data);
            break;
          case 'executed':
            this.onExecuted(data);
            break;
          case 'stopped':
            this.onStopped(data);
            break;
        }
      },
      onWaiting(data) {
        warningDialog({
          message: data.data['executing_status'],
        });
      },
      onExecuted(data) {
        console.log('original executed: ', data.data);
        return this.timeStamp !== null;
      },
      onStopped(data) {
        errorDialog({
          message: `Executed is stopped unexpectedly. ${data.errors[0].message}`,
        });
        this.finishedCloudExecution();
      },
      timeOutHelper() {
        this.finishedCloudExecution();
        errorDialog({
          message: 'Execution Timed out',
        });
      },
      timeOutReset(seconds = 10) {
        setTimeout(this.timeOutHelper, seconds * 1000);
      },
      sendDataToCloudExecutor(code, graphId) {
        this.startCloudExecuting();
        const message = this.wsData(code, graphId);
        websocketSend(message, this.onMessage);
      },
    },
  };
</script>
