export const allTutorialAbstractInfoQuery = `
query ($translation: String, $default: String = "en-us") {
  allTutorialInfo {
    url
    isPublished
    categories {
      category
    }
    content (translation: $translation, default: $default) {
      title
      authors {
        username
      }
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
    authors {
      username
    }
    categories {
      category
    }
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
    categories {
      category
    }
    content(translation: $translation, default: $default) {
      title
      authors {
        username
      }
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
      priority {
        priority
        label
      }
      cyjs
    }
    code {
      id
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

export const pullTutorialArticle = `query ($url: String, $translation: String, $default: String = "en-us") {
  tutorial(url: $url) {
    content(translation: $translation, default: $default) {
      title
      contentHtml
    }
  }
}`;

export const pullGraphAndCodeQuery = `
query ($url: String, $translation: String, $default: String = "en-us") {
  graph(url: $url) {
    id
    cyjs
    isPublished
    priority {
      priority
      label
    }
    content(translation: $translation, default: $default){
      title 
      abstract
      isPublished
    }
    execresultjsonSet {
      code {
        id 
        code
      }
      json
    }
  }
}`;

export const allCategoryQuery = `
query {
  allCategories {
    id
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
    priority {
      label
    }
    cyjs
    tutorials {
      name
    }
    authors {
      username
    }
    url
    id
  }
}`;

export const categoryListQuery = `
query {
  allCategories {
    category
    isPublished
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
      authors {
        username
      }
      contentMd
      contentHtml
      id 
    }
  }
}`;

export const graphInfoListQuery = `
query ($translation: String, $default: String = "") {
  allGraphInfo {
    name 
    url
    content (translation: $translation, default:$default) {
      title
      isPublished
      abstract
      id
    }
  }
}`;

export const codeListQuery = `query {
  allCode {
    tutorial {
      name
      url
    }
    code
    id
  }
}`;

export const categoryQuery = `
query ($id: String!){
  category(id: $id) {
    id
    isPublished
    category
  }
}`;

export const updateCategoryMutation = `
mutation($id: String!, $category: String!, $isPublished: Boolean) {
  updateCategory(id: $id, category: $category, isPublished: $isPublished) {
    success
    category {
      id
      isPublished
      category
    }
  }
}`;

export const tutorialQuery = `
query($id: String!) {
  tutorial(id: $id) {
    id
    url
    name
    categories {
      id
    }
    isPublished
  }
}`;

export const updateTutorialAnchorMutation = `
mutation ($id: String!, $url: String!, $name: String!, $categories: [String], $isPublished: Boolean) {
  updateTutorialAnchor(id: $id, url: $url, name: $name, categories: $categories, isPublished: $isPublished) {
    success
  }
}`;

export const graphQuery = `
query ($id: String!) {
  graph(id: $id) {
    id
    url
    name
    cyjs
    isPublished
    priority {
      priority
      label
    }
    authors {
      id
    }
    categories {
      id
    }
    tutorials {
      id
    }
  }
}`;

export const tutorialSelectQuery = `
query {
  allTutorialInfo {
    name
    id
  }
}`;

export const authorSelectQuery = `
query {
  allAuthors {
    id
    username
  }
}`;
