export const allTutorialAbstractInfoQuery = `
query ($translation: String, $default: String = "en-us") {
  allTutorialInfo {
    url
    isPublished
    categories
    content (translation: $translation, default: $default) {
      title
      authors
      abstract
      isPublished
      modifiedTime
    }
  }
}`;
// TODO look into the defaults

// TODo the graph id is pulled twice hmmm
export const pullTutorialDetailQuery = `
query ($url: String, $translation: String, $default: String = "en-us") {
  tutorial(url: $url) {
    id
    isPublished
    categories
    content(translation: $translation, default: $default) {
      title
      authors
      contentHtml
      isPublished
      modifiedTime
    }
    graphSet {
      name
      id
      isPublished
      graphInfo
      priority
      cyjs
    }
    code {
      code
      execresultjsonSet {
        json
        graph {
          id
        }
      }
    }
  }
}`;

export const allCategoryQuery = `
query {
  allCategories {
    category
  }
}`;
