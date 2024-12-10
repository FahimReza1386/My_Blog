from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size=10
    
    page_size_query_param = 'page_size'
    max_page_size = 100
    

    def get_paginated_response(self, data):
        return Response(
            {
                "Links_Pagination": {
                    "Next_Page": self.get_next_link(),
                    "Previous": self.get_previous_link(),
                },
                "Posts_Count": self.page.paginator.count,
                "Total_Pages": self.page.paginator.num_pages,
                "The_Posts_Information": data,
            }
        )
