class DeleteChatUseCase:
    def __init__(self, chat_room_repo):
        self.chat_room_repo = chat_room_repo

    async def execute(self, room_id: str, account_id: int) -> bool:
        room = await self.chat_room_repo.find_by_id(room_id)

        if not room:
            return False

        if room.account_id != account_id:
            return False

        return await self.chat_room_repo.delete_by_room_id(room_id)