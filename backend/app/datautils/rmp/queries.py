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

combined_query = """
query ProfessorRatingsQuery($text: String!, $schoolID: ID!) {
  newSearch {
    teachers(query: {text: $text, schoolID: $schoolID}) {
      edges {
        node {
          id
          __typename
          ... on Teacher {
            avgDifficulty
            avgRating
            numRatings
            wouldTakeAgainPercent
          }
        }
      }
    }
  }
}
"""

get_all_professors_query = '''
query ProfessorRatingsQuery($schoolID: ID!, $first: Int!) {
  newSearch {
    teachers(query: { schoolID: $schoolID  }, first: $first) {
      edges {
        node {
          id
          firstName
          lastName
          department
          avgDifficulty
          avgRating
          numRatings
          wouldTakeAgainPercent
        }
      }
    }
  }
}
'''

total_count_query = '''
query ProfessorCountQuery($schoolID: ID!) {
  newSearch {
    teachers(query: { schoolID: $schoolID }) {
      resultCount
    }
  }
}
'''