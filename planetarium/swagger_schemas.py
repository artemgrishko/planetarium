from drf_spectacular.utils import OpenApiParameter

astronomy_show_schema = {"parameters": [
            OpenApiParameter(
                "show_theme",
                type={"type": "array", "items": {"type": "number"}},
                description="Filter by show themes id",
            ),
            OpenApiParameter("title", type=str, description="Filter by title"),
        ]
}

show_session_schema = {"parameters": [
            OpenApiParameter(
                "show_time",
                type=str,
                description="Filter by show_time",
            ),
            OpenApiParameter(
                "astronomy_show",
                type=int,
                description="Filter by astronomy_show id",
            ),
        ]
}
