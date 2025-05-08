# from aiogram import Router
# from aiogram.types import Message
# from sc_kpm import ScKeynodes
# from sc_kpm.utils import search_element_by_role_relation, get_link_content_data
# from sc_client.constants import sc_types
# from sc_client.client import connect, is_connected

# router = Router()

# @router.message(lambda msg: msg.text.startswith("/define"))
# async def get_definition_command(message: Message):
#     if not is_connected():
#         connect("ws://localhost:8090/ws_json")

#     parts = message.text.strip().split(maxsplit=1)
#     if len(parts) < 2:
#         await message.answer("❗ Используй команду так: `/define идентификатор`", parse_mode="Markdown")
#         return

#     idtf = parts[1]

#     try:
#         node = ScKeynodes.resolve(idtf, sc_types.NODE_CONST_CLASS)
#         if not node.is_valid():
#             await message.answer(f"❌ Узел `{idtf}` не найден.", parse_mode="Markdown")
#             return

#         nrel_definition = ScKeynodes.resolve("nrel_definition", sc_types.NODE_ROLE)
#         link = search_element_by_role_relation(node, nrel_definition)

#         if link.is_valid():
#             content = get_link_content_data(link)
#             await message.answer(f"✅ Определение для `{idtf}`:\n```{content}```", parse_mode="Markdown")
#         else:
#             await message.answer(f"⚠️ У узла `{idtf}` нет определения.", parse_mode="Markdown")

#     except Exception as e:
#         await message.answer(f"🚫 Ошибка при получении определения: {e}")
#fd