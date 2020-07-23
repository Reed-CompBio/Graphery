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

export const allGraphAbstractInfoQuery = `
query ($translation: String, $default: String = "en-us") {
  allGraphInfo {
    url
    authors
    isPublished
    modifiedTime
    content(translation: $translation, default: $default) {
      title
      abstract
      isPublished
    }
  }
}`;

// TODo the graph id is pulled twice hmmm
export const pullTutorialDetailQuery = `
query ($url: String, $translation: String, $default: String = "en-us") {
  tutorial(url: $url) {
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
      id
      isPublished
      content(translation: $translation, default: $default) {
        title
        abstract
        isPublished
      }
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

export const loginMutation = `
mutation ($username: String!, $password: String!) {
  login(username: $username, password: $password) {
    success
    user {
      username
      email
      role
    }
  }
}`;

export const userInfoQuery = `
query {
  userInfo {
    username
    email
    role
  }
}`;

export const logoutMutation = `
mutation {
  logout {
    success
  }
}`;

export const tutorialAnchorListQuery = `
query {
  allTutorialInfo {
    name
    isPublished
    url
    id
  }
}`;

export const graphListQuery = `
query {
  allGraphInfo {
    name
    isPublished
    priority
    cyjs
    tutorials {
      name
    }
    authors
    url
    id
  }
}`;

export const categoryListQuery = `
query {
  allCategories {
    category
    id
  }
}`;

export const tutorialContentListQuery = `
query ($translation: String, $default: String = "") {
  allTutorialInfo {
    url
    name
    content (translation: $translation, default: $default) {
      title
      isPublished 
      abstract
      authors
      contentMd
      contentHtml
      id 
    }
  }
}`;
