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

        if (!(className in this.storedClassNames)) {
          const colorClassStyle = [
            {
              selector: queryClassName,
              style: {
                'overlay-color': color,
                'overlay-opacity': 0.5,
                'overlay-padding': 5,
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
        const temp = [...this.cytoscape_.style().json(), ...styleJsonObject];
        this.cytoscape_.style(temp);
      },
      toggleElementsClassName(className, flag) {
        this.cytoscape_
          .$(this.genClassQueryName(className))
          .toggleClass(className, flag);
      },
      removeElementsClassName(className) {
        this.cytoscape_
          .$(this.genClassQueryName(className))
          .removeClass(className);
      },
      addClassNameByIds(ids, className) {
        this.cytoscape_.$(ids).addClass(className);
      },
      addClassNameById(id, className) {
        const idName = `#${id}`;
        this.cytoscape_.$(idName).addClass(className);
      },
    },
  };
</script>
