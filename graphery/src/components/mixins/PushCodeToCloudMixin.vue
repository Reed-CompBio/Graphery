<script>
  import { websocketSend } from '@/services/websocket_handler';
  import { errorDialog, warningDialog } from '@/services/helpers';

  const TIME_OUT_SECONDS = 10;

  export default {
    data() {
      return {
        isExecutingRemotely: false,
        timeStamp: null,
        timer: null,
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
        warningDialog(
          {
            message: data.data['executing_status'],
          },
          1000
        );
      },
      onExecuted(data) {
        clearTimeout(this.timer);
        return this.timeStamp !== null;
      },
      onStopped(data) {
        clearTimeout(this.timer);
        errorDialog(
          {
            message: `Executed is stopped unexpectedly. ${data.errors[0].message}`,
          },
          0
        );
        this.finishedCloudExecution();
      },
      onWebsocketError() {
        errorDialog({
          message: 'Cannot process request due to connection error.',
        });
        this.finishedCloudExecution();
      },
      timeOutHelper() {
        this.finishedCloudExecution();
        errorDialog({
          message: `Request Timed Out After ${TIME_OUT_SECONDS}s`,
        });
      },
      timeOutReset(seconds = TIME_OUT_SECONDS) {
        return setTimeout(this.timeOutHelper, seconds * 1000);
      },
      sendDataToCloudExecutor(code, graphId) {
        this.startCloudExecuting();
        const message = this.wsData(code, graphId);
        websocketSend(message, this.onMessage, this.onWebsocketError);
        this.timer = this.timeOutReset();
      },
    },
  };
</script>
