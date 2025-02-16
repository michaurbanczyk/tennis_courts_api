# import logging
# from typing import List, Optional
#
# from app.models.matches import MatchBase, MatchResults
# from app.repositories.matches import MatchRepository
# from app.websocket_manager import WebSocketManager
#
#
# class MatchService:
#     def __init__(self, websocket_manager: WebSocketManager):
#         self.repository = MatchRepository()
#         self.websocket_manager = websocket_manager
#
#     async def create_match(self, match: MatchBase) -> dict:
#         match_data = match.model_dump()
#         created_match = await self.repository.create_match(match_data)
#         return created_match
#
#     async def get_matches(self) -> List[dict]:
#         return await self.repository.get_matches()
#
#     async def get_match(self, match_id: str) -> Optional[dict]:
#         match = await self.repository.get_match(match_id)
#         if match:
#             match["id"] = str(match["_id"])
#             del match["_id"]
#         return match
#
#     async def get_matches_by_tournament_id(self, tournament_id: str) -> Optional[dict]:
#         return await self.repository.get_matches_by_tournament_id(tournament_id)
#
#     async def delete_match(self, match_id: str) -> int:
#         return await self.repository.delete_match(match_id)
#
#     async def update_results(self, match_id: str, results: MatchResults) -> Optional[dict]:
#         results_data = results.model_dump()
#         updated_match = await self.repository.update_results(match_id, results_data)
#         if updated_match:
#             updated_match["id"] = str(updated_match["_id"])
#             del updated_match["_id"]
#             await self.broadcast_update({"event": "results_updated", "data": updated_match})
#         return updated_match
#
#     async def close(self):
#         await self.repository.close()
#
#     async def broadcast_update(self, message: dict):
#         logging.debug("Boradcasting")
#         await self.websocket_manager.broadcast(message)
