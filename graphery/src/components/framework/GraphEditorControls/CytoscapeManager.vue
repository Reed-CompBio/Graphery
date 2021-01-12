<script>
  export default {
    data() {
      return {
        storedClassNames_: [],
      };
    },
    computed: {
      cytoscape_() {
        return null;
      },
      storedClassNames() {
        return this.storedClassNames_;
      },
    },
    methods: {
      genClassQueryName(className) {
        if (!className.startsWith('.')) {
          return `.${className}`;
        }
        return className;
      },
      generateColoredClass(className, color) {
        const queryClassName = this.genClassQueryName(className);

        if (!this.storedClassNames.includes(className)) {
          const colorClassStyle = [
            {
              selector: queryClassName,
              style: {
                'overlay-color': color,
                'overlay-opacity': 0.4,
                'overlay-padding': 4,
              },
            },
          ];
          this.addStyle(colorClassStyle);
          this.storedClassNames.push(className);
        }
      },
      clearStoredClassNames() {
        this.storedClassNames_ = [];
      },
      addStyle(styleJsonObject) {
        if (!Array.isArray(styleJsonObject)) {
          styleJsonObject = [styleJsonObject];
        }

        this.cytoscape_.style([
          ...this.cytoscape_.style().json(),
          ...styleJsonObject,
        ]);
      },
      toggleElementsClassName(className, flag) {
        this.cytoscape_
          ?.$(this.genClassQueryName(className))
          .toggleClass(className, flag);
      },
      removeElementsClassName(className) {
        this.cytoscape_
          ?.$(this.genClassQueryName(className))
          .removeClass(className);
      },
      addClassNameByIds(className, ids) {
        this.cytoscape_.$(ids).addClass(className);
      },
      addClassNameById(id, className) {
        const idName = `#${id}`;
        this.cytoscape_.$(idName).addClass(className);
      },
    },
  };
</script>
