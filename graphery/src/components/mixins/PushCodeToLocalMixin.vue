<script>
  import { localServerCaller } from '@/services/apis';
  import { errorDialog, successDialog } from '@/services/helpers';

  export default {
    methods: {
      pushToLocal(code, graph, startCallback, successCallback, finalCallback) {
        return localServerCaller(code, graph)
          .then((data) => {
            if (data['error']) {
              throw Error(data['error']);
            }

            if (!('data' in data)) {
              throw Error('No valid data returned from local server');
            }

            const { codeHash, execResult } = data['data'];
            // TODO link this with workspace

            successCallback(codeHash, execResult);

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
            finalCallback();
          });
      },
    },
  };
</script>
