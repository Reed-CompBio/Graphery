export const allTutorialAbstractInfoQuery = `query ($translation: String, $default: String) {
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
