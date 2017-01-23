from django.contrib import admin

from .models import (Room, Chat)

admin.site.register(Room,
                    list_display=["id", "name", "members"],
                    list_display_links=["id"],
                    )
admin.site.register(Chat,
                    list_display=["id", "text", "room"],
                    list_display_links=["id", "text"],
                    )
