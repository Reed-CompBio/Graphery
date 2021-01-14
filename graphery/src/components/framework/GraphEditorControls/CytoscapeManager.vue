<script>
  const TOGGLE_CLASS_NAME = 'toggleClass';
  const TOGGLE_CLASS_QUERY_NAME = '.' + TOGGLE_CLASS_NAME;
  export default {
    data() {
      return {
        storedClassNames_: [],
        defaultGraphStyle: [
          {
            selector: 'node',
            style: {
              label: 'data(name)',
              'text-valign': 'center',
              'text-halign': 'center',
              'text-outline-color': 'white',
              'text-outline-opacity': 1,
              'text-outline-width': 1,
              height: '20px',
              width: '20px',
              'font-size': '8px',
              'border-color': 'black',
              'border-opacity': 1,
              'border-width': 1,
            },
          },
        ],
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
      addToggleClass() {
        this.addStyle({
          selector: TOGGLE_CLASS_QUERY_NAME,
          style: {
            'overlay-opacity': 0.1,
          },
        });
      },
      clearStoredClassNames() {
        for (const className of this.storedClassNames_) {
          this.removeElementsClassName(className);
        }
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
      toggleElementsByIds(ids, className, flag) {
        this.cytoscape_.$(ids).toggleClass(className, flag);
      },
      toggleElementsClassName(className, flag) {
        if (this.cytoscape_) {
          this.cytoscape_
            .$(this.genClassQueryName(className))
            .toggleClass(TOGGLE_CLASS_NAME, !flag);
        }
      },
      removeElementsClassName(className) {
        if (this.cytoscape_) {
          this.cytoscape_
            .$(this.genClassQueryName(className))
            .removeClass(className);
        }
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
