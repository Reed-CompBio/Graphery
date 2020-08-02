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
    id
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
    id
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
mutation($id: UUID!, $category: String!, $isPublished: Boolean) {
  updateCategory(id: $id, category: $category, isPublished: $isPublished) {
    success
    model {
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
mutation ($id: UUID!, $url: String!, $name: String!, $categories: [String], $isPublished: Boolean) {
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

export const updateGraphMutation = `
mutation ($id: UUID!, $url: String!, $name: String!, $cyjs: JSONString!, $isPublished:Boolean, $priority: Int, $authors: [String], $categories: [String], $tutorials: [String]) {
  updateGraph(id: $id, url: $url, name: $name, cyjs: $cyjs, isPublished: $isPublished, priority: $priority, authors: $authors, categories: $categories, tutorials: $tutorials) {
    success
    model {
      id
    }
  }
}`;

export const codeQuery = `
query ($id: UUID!) {
  code(id: $id) {
    code
    tutorial {
      id
    }
  }
}`;

export const allTutorialNoCodeQuery = `
query ($code: UUID) {
  allTutorialInfoNoCode (code: $code) {
    id
    name
  }
}`;

export const updateCodeMutation = `
mutation ($id: UUID!, $code: String!, $tutorial: UUID!){
  updateCode (id:$id, code:$code, tutorial: $tutorial) {
    success
    model {
      id
    }
  }
}`;

export const resultJsonGetGraphsQuery = `
query ($id: UUID!) {
  code(id: $id) {
    tutorial {
      graphSet {
        id
        name
        cyjs
      }
    }
    execresultjsonSet {
      graph {
        id
      }
      json
    }
  }
}`;

export const tutorialContentQuery = `
query ($id: String!, $translation: String!, $default: String = "en-us") {
  tutorial(id: $id) {
    url
    content(translation: $translation, default: $default) {
      id
      title
      isPublished
      authors {
        id
      }
      abstract
      contentMd
    }
  }
}`;

export const tutorialContentMutation = `
mutation ($lang:String!, $content: TutorialContentInputType!){
  updateTutorialContent(lang: $lang, content: $content) {
    success
    model {
      id
    }
  }
}`;

export const uploadImage = `
mutation ($linkId: UUID!, $where: UploadWhere!){
  uploadStatics(linkId: $linkId, where: $where) {
    success
    url
  }
}`;

export const deleteImage = `
mutation ($url: String!){
  deleteStatics(url: $url) {
    success
  }
}`;

export const graphInfoContentQuery = `
query ($id: String!, $translation: String!, $default: String = "en-us") {
  graph(id: $id) {
    url
    content(translation: $translation, default: $default) {
      id
      title
      abstractMd
      abstract
      isPublished
    }
  }
}`;

export const graphInfoContentMutation = `
mutation ($lang: String!, $content: GraphContentInputType!) {
  updateGraphInfoContent(lang: $lang, content: $content) {
    success
    model {
      id
    }
  }
}`;

export const resultJsonsMutation = `
mutation ($codeId: UUID!, $resultJsonDict: GenericScalar!) {
  updateResultJson (codeId: $codeId, resultJsonDict: $resultJsonDict) {
    success
  }
}`;

export const invitationKeyQuery = `
query {
  invitationCodes
}`;

export const refreshInvitationMutation = `
mutation {
  refreshInvitationCode {
    success
    invitationCodes
  }
}`;
