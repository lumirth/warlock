autocomplete_school_query = """
query AutocompleteSearchQuery(
  $query: String!
)
{
  autocomplete(query: $query) {
    schools {
      edges {
        node {
          id
          name
          city
          state
        }
      }
    }
  }
}
"""

search_teacher_query = """
query NewSearchTeachersQuery($text: String!, $schoolID: ID!)
{
  newSearch {
    teachers(query: {text: $text, schoolID: $schoolID}) {
      edges {
        cursor
        node {
          id
          firstName
          lastName
          school {
            name
            id
          }
        }
      }
    }
  }
}
"""

get_teacher_query = """
query TeacherRatingsPageQuery(
  $id: ID!
) {
  node(id: $id) {
    ... on Teacher {
      id
      firstName
      lastName
      school {
        name
        id
        city
        state
      }
      avgDifficulty
      avgRating
      department
      numRatings
      legacyId
      wouldTakeAgainPercent
    }
    id
  }
}
"""
