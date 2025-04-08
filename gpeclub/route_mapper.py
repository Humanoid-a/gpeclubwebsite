# gpeclub/route_mapper.py

class RouteMapper:
    def __init__(self):
        # Main navigation routes
        self.routes = {
            'home': '/',
            'projects': '/projects/search/',
            'vocab': '/vocab/list',
            'school': '/projects/school/',
            'powerschool': '/projects/powerschool/',
            'about': '/about/',
            'old': '/old/'
        }

        # Project-specific routes
        self.project_routes = {
            'supertictactoe': '/projects/supertictactoe/',
            'polyptoton': '/projects/polyptoton/',
            'photo1': '/projects/photo1/',
            'trigonomis': '/projects/trigonomis/',
            'invective': '/projects/invective/',
            'isocolon': '/projects/isocolon/',
            'phys2': '/projects/phys2/',
            'politics': '/politics/'
        }

        # Feature-specific routes based on user intent
        self.intent_routes = {
            'vocab practice': '/vocab/list',
            'vocabulary list': '/vocab/list',
            'vocab list': '/vocab/list',
            'vocab ai': '/vocab/ai/set1/',
            'vocabulary ai': '/vocab/ai/set1/',
            'vocab mcq': '/vocab/mcq/set1/',
            'vocabulary mcq': '/vocab/mcq/set1/',
            'grade viewer': '/projects/school/',
            'grades': '/projects/school/',
            'powerschool': '/projects/powerschool/',
            'gpehub': '/',
            'gpe hub': '/',
            'gpe club': '/about/',
            'team members': '/about/',
            'tictactoe': '/projects/supertictactoe/',
            'super tic tac toe': '/projects/supertictactoe/',
            'game': '/projects/trigonomis/',
            'trigonomis game': '/projects/trigonomis/',
            'physics': '/projects/phys2/',
            'political quiz': '/politics/',
            'political test': '/politics/',
            'vocab set': '/vocab/sets/set1/'
        }

    def get_route(self, query):
        """
        Find the most relevant route based on the user's query
        """
        if not query:
            return None

        query_lower = query.lower()

        # First check direct matches with main routes
        for key, route in self.routes.items():
            if key in query_lower:
                return route

        # Then check project routes
        for key, route in self.project_routes.items():
            if key in query_lower:
                return route

        # Finally check intent-based routes
        for intent, route in self.intent_routes.items():
            if intent in query_lower:
                return route

        # Fallback to home page if no match
        return None