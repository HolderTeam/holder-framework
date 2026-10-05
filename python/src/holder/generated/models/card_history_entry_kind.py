from enum import StrEnum


class CardHistoryEntryKind(StrEnum):
    CREATED = "created"
    DELETED = "deleted"
    LINKS = "links"
    MERGED = "merged"
    MILESTONES = "milestones"
    MOVED = "moved"
    PERMANENTLY_DELETED = "permanently_deleted"
    RESTORED = "restored"
    UPDATED = "updated"

    def __str__(self) -> str:
        return str(self.value)
