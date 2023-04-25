autocomplete_school_query = """
query AutocompleteSearchQuery($query: String!) {
  autocomplete(query: $query) {
    schools {
      edges {
        node {
          id
          name
          city
          state
          __typename
        }
      }
    }
  }
}
"""

search_teacher_query = """
query NewSearchTeachersQuery($text: String!, $schoolID: ID!) {
  newSearch {
    teachers(query: {text: $text, schoolID: $schoolID}) {
      edges {
        node {
          id
          __typename
        }
      }
    }
  }
}
"""

get_teacher_query = """
query TeacherRatingsPageQuery($id: ID!) {
  node(id: $id) {
    ... on Teacher {
      avgDifficulty
      avgRating
      numRatings
      wouldTakeAgainPercent
      __typename
    }
    id
  }
}
"""