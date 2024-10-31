from flask import jsonify
from flask_graphql import GraphQLView
from graphql import GraphQLError


class BadRequestException(GraphQLError):
    """
    Custom exception class to handle bad requests in GraphQL with a 400 status code.
    """

    pass


class CustomGraphQLView(GraphQLView):
    """
    Custom GraphQL view to handle exceptions and return a JSON response with status code 400
    when a BadRequestException is raised.
    """

    def execute_graphql_request(self, *args, **kwargs):
        try:
            # Attempt to execute the GraphQL request
            result = super().execute_graphql_request(*args, **kwargs)
            return result
        except BadRequestException as e:
            # Capture BadRequestException and return a 400 error
            response = jsonify({"errors": [{"message": str(e)}], "data": None})
            response.status_code = 400
            return response
