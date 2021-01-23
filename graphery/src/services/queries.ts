export const allTutorialAbstractInfoQuery = `
query ($translation: String, $filterContent: FilterContentType) {
  allTutorialInfo (filterContent: $filterContent) {
    url
    isPublished
    categories {
      id
      category
    }
    content (translation: $translation) {
      title
      authors {
        username
        firstName
        lastName
      }
      abstract
      isPublished
      modifiedTime
    }
    rank {
      level 
      section
    }
  }
}`;
// TODO look into the defaults

export const allGraphAbstractInfoQuery = `
query ($translation: String, $default: String, $filterContent: FilterContentType) {
  allGraphInfo (filterContent: $filterContent) {
    url
    authors {
      username
      firstName
      lastName
    }
    categories {
      id
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
query ($url: String, $translation: String) {
  tutorial(url: $url) {
    isPublished
    categories {
      category
    }
    rank {
      level
      section
    }
    content(translation: $translation) {
      title
      authors {
        username
        firstName
        lastName
      }
      contentHtml
      isPublished
      modifiedTime
    }
    graphSet {
      id
      isPublished
      content(translation: $translation, default: "en-us") {
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

export const pullTutorialArticle = `query ($url: String, $translation: String) {
  tutorial(url: $url) {
    content(translation: $translation) {
      title
      contentHtml
    }
  }
}`;

// TODO remove default
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
        name
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
      firstName
      lastName
    }
  }
}`;

export const userInfoQuery = `
query {
  userInfo {
    username
    email
    role
    firstName
    lastName
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
    rank {
      level
      section
    }
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
      firstName
      lastName
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
        firstName
        lastName
      }
      contentMd
      contentHtml
      id 
    }
    rank {
      level
      section
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
    name
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
    rank {
      level
      section
    }
    categories {
      id
    }
    isPublished
  }
}`;

export const updateTutorialAnchorMutation = `
mutation ($id: UUID!, $url: String!, $name: String!, $rank: RankInputType!, $categories: [String], $isPublished: Boolean) {
  updateTutorialAnchor(id: $id, url: $url, name: $name, rank: $rank, categories: $categories, isPublished: $isPublished) {
    success
    model {
      id
    }
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
    firstName
    lastName
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
    name
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
mutation ($id: UUID!, $name: String!, $code: String!, $tutorial: UUID!){
  updateCode (id:$id, name: $name, code:$code, tutorial: $tutorial) {
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
    graphSet {
      id
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

export const uploadStatic = `
mutation {
  uploadStatic {
    success
  }
}`;

export const deleteImage = `
mutation ($url: String!){
  deleteStatic(url: $url) {
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

export const registerMutation = `
mutation ($email: String!, $username: String!, $password: String!, $invitationCode: String!, $firstName: String, $lastName: String) {
  register(email: $email, username: $username, password: $password, invitationCode:$invitationCode, firstName: $firstName, lastName: $lastName) {
    success
  }
}`;

export const deleteMutation = `
mutation ($contentType: DeletionEnum!, $id: UUID!) {
  deleteContent (contentType: $contentType, id: $id) {
    success
  }
}`;

export const fetchUploads = `
query {
  allUploads {
    id
    relativeUrl
    alias
  }
}`;

export const graphSelectQuery = `
query {
  allGraphInfo {
    id
    name
  }
}`;

export const changePasswordMutation = `
mutation ($oldPassword: String!, $newPassword: String!) {
  changePassword(oldPassword: $oldPassword, newPassword: $newPassword) {
    success
    user {
      username
      firstName
      lastName
      email
      role
    }
  }
}`;

export const executeCode = `
mutation ($codeIds: [UUID]) {
  executeCode(codeIds: $codeIds){
    success
    failedMissions {
      code {
        id 
        name
      }
      graph {
        id
        name
      }
      error 
    }
  }
}`;
