mutation {
  createPost(
    title: "GraphQLPosTest"
    text: "GraphQLPosT tresc"
    topicId: 2
    slug: "GraphQLPosTest"
    createdById: 1
  ) {
    success
    message
    post {
      id
      title
      text
      slug
      topic {
        id
        name
      }
      createdBy {
        id
        username
      }
      createdAt
    }
  }
}







mutation {
  updatePost(
    id: 8
    title: "TutolUpdate"
    text: "Updated treść"
    slug: "GraphQLPosTest"
    topicId: 2
  ) {
    success
    message
    post {
      id
      title
      text
      slug
      topic {
        id
        name
      }
      createdBy {
        id
        username
      }
      createdAt
    }
  }
}



mutation {
  deletePost(id: 8) {
    success
    message
  }
}