<script>
  import { localServerCaller } from '@/services/apis';
  import { errorDialog, successDialog } from '@/services/helpers';

  export default {
    methods: {
      async pushToLocal(
        code,
        graph,
        startCallback,
        successCallback,
        finalCallback
      ) {
        if (startCallback) {
          startCallback();
        }
        await localServerCaller(code, graph)
          .then((data) => {
            if (!data) {
              throw Error('No valid data returned from local server');
            }

            const { codeHash, execResult } = data;
            // TODO link this with workspace

            if (successCallback) {
              successCallback(codeHash, execResult);
            }

            successDialog({
              message: 'Exec Successfully!',
            });

            // TODO use it to pass the actual content
          })
          .catch((err) => {
            errorDialog({
              message: 'An error occurs when talking to local server. ' + err,
            });
          })
          .finally(() => {
            if (finalCallback) {
              finalCallback();
            }
          });
      },
    },
  };
</script>
