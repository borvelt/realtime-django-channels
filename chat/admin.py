from django.contrib import admin

from .models import (Room, Chat)

admin.site.register(Room,
                    list_display=["id", "name", "members"],
                    list_display_links=["id"],
                    search_fields=['id', 'members']
                    )
admin.site.register(Chat,
                    list_display=["id", "text", "is_seen"],
                    list_display_links=["id", "text"],
                    search_fields=['id', 'text']
                    )
