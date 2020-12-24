# Frontend Issues

A list contains the TODO and FIXME found in graphery frontend.

**Continuously updating**

Table of Contents
=================

   * [Frontend Issues](#frontend-issues)
   * [Topography](#topography)
   * [Header](#header)
         * [Ajax bar](#ajax-bar)
      * [Drawer](#drawer)
   * [Home](#home)
   * [Footer](#footer)
   * [Graph](#graph)
      * [Separator](#separator)
      * [Article](#article)
   * [Accessibility](#accessibility)
      * [Colorblind Friendly](#colorblind-friendly)
      * [Tab navigation](#tab-navigation)
   * [About](#about)
   * [Account](#account)
   * [Control Panel](#control-panel)
   * [Settings](#settings)
   * [Miscellaneous](#miscellaneous)
         * [Alert Notification (helper.ts)](#alert-notification-helperts)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)
# Topography

Webpage headings should be unified, topography should be read-friendly in a mordern design fashion.

~~`font-size`, `font-family`~~

- Should the *global* design be looser or tighter?
- FIXME: We should accentuate the content of the body, maybe the header needs to be smaller? (In order not to detract from the visual effect, too large header often leads to user distraction)

# Header

The toolbar is implemented in the header and the buttons can be re-styled in a metaphorical way.

Text button + Icon button(such as settings and login, or they are merged in a context menu)

### Ajax bar

Color?

## Drawer

FIXME

The drawer will only work if the screen width is smaller than the breakpoint `$q.screen.lt.md`

- The title text GRAPHERY is not in the form of logo text.
- The card border should not be rounded
- The menu button
  - Icon size and text size do not match perfectly
  - The color of the icons is too conspicuous, which affects the readability of the text.

# Home

Or the Welcome interface.

FIXME: The current buttons group is too boring, and should be redesigned in a more metaphor way.

- reorganize in funtions
- use button styles

# Footer

The footer content shows in the non-graph page.

Maintaining the status quo.

TODO: modify the content of footer

# Graph

## Tutorials & Graphs

The page of archive indexing, redesign:

- the search box

- paginator

- Filter categories placeholder blank - label name

  *Practice in* `/src/components/ControlPanel/parts/selectors/CategorySelection.vue`

## Separator

(Maybe) An option for remember/ not remember the position of the separators

FIXME: The position of the vertical separators (**Split Pos**) on the following two pages cannot be mixed given their different functions.

- Tutorials (Graph,Code|Article)

- Graphs (Graph|Code)

  ```js
  // Graph.vue & Tutorial.vue
  splitPos: {
          set(d) {
            this.$store.dispatch(
              'settings/changeGraphSplitPos',
              Math.round(d * 10) / 10
            );
          },
  ```

  ```ts
  // /store/modules/settings.ts
  160 dispatch('changeGraphSplitPos', graphSplitPos);
  ```

  

## Article

- FIXME: style of chips
- FIXME: hide back-to-top button when it’s already at the top

- FIXME: redesign the CC declaration

# Accessibility

## Colorblind Friendly

- [Visual Disabilities Color-blindness - WebAIM](https://webaim.org/articles/visual/colorblind)

TBD

## Tab navigation

- [Keyboard Accessibility - WebAIM](https://webaim.org/techniques/keyboard/)

- [ARIA: tab role in MDN](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Roles/Tab_Role)

The quasar framework has perfectly done the adaptation of the tab navigation for us, just click <kbd>Tab</kbd>, the content slection will be highlighted.



# About

Imperfect, just redesign

# Account

TODO: Redesign

- Login

- Accout

# Control Panel

Imperfect, just redesign

# Settings

the line-height and so on.

Make it a compact layout



# Miscellaneous

### Alert Notification (helper.ts)

FIXME

Redesign with proper color

- warningDialog
- errorDialog

backend server downtime will trigger more alert pop-ups in the same time, unfriendly.