<script>
  export default {
    computed: {
      cytoscape_() {
        return null;
      },
    },
    methods: {
      genClassQueryName(className) {
        return `.${className}`;
      },
      generateColoredClass(className, color) {
        const colorClassStyle = [
          {
            selector: `.${className}`,
            style: {
              'overlay-color': color,
              'overlay-opacity': 0.5,
              'overlay-padding': 5,
            },
          },
        ];
        this.addStyle(colorClassStyle);
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
      addClassNameById(id, className) {
        const idName = `#${id}`;
        this.cytoscape_.$(idName).addClass(className);
      },
    },
  };
</script>
