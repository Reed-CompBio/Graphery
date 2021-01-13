<script>
  export default {
    data() {
      return {
        currentPictureList_: null,
        currentDisplayState_: false,
        currentPictureIndex_: 0,
      };
    },
    computed: {
      currentPictureList: {
        set(d) {
          if (Array.isArray(d)) {
            this.currentPictureList_ = d;
          } else {
            this.currentPictureList_ = [d];
          }
        },
        get() {
          return this.currentPictureList_;
        },
      },
      currentDisplayState: {
        set(d) {
          this.currentDisplayState_ = d;
        },
        get() {
          return this.currentDisplayState_;
        },
      },
      currentPictureIndex: {
        set(d) {
          this.currentPictureIndex_ = d;
        },
        get() {
          return this.currentPictureIndex_;
        },
      },
    },
    methods: {
      changeDisplayState(val) {
        this.currentDisplayState = val;
      },
      changeCurrentPictureIndex(val) {
        this.currentPictureIndex = val;
      },
      changePictureList(srcList) {
        this.currentPictureList = srcList;
      },
      setRequestPictureIndex(src) {
        this.currentPictureIndex = this.currentPictureList?.findIndex(
          (ele) => ele === src
        );
        this.currentDisplayState = true;
      },
    },
  };
</script>
