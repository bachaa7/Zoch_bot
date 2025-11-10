from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.rag_data_manager import rag_data_manager
from app.keyboards import knowledge_categories_keyboard
from ostis_manager import create_node_in_ostis, extract_data_from_ostis, find_node_in_ostis  # Новый импорт

router = Router()

class CreateKnowledgeStates(StatesGroup):
    waiting_for_title = State()
    waiting_for_content = State()
    waiting_for_category = State()

@router.callback_query(F.data == "create_rag_knowledge")
async def start_create_knowledge(callback: CallbackQuery, state: FSMContext):
    """Начало создания знания - сохраняем в OSTIS, затем в векторную БД"""
    await callback.message.answer(
        "📝 *Создание нового знания*\n\n"
        "Знание будет:\n"
        "1. 📚 Сохранено в OSTIS (основная база)\n"
        "2. 🔄 Автоматически извлечено в векторную БД\n"
        "3. 💬 Станет доступно для ИИ-ассистента\n\n"
        "Введите название темы (будет идентификатором в OSTIS):"
    )
    await state.set_state(CreateKnowledgeStates.waiting_for_title)
    await callback.answer()

@router.message(CreateKnowledgeStates.waiting_for_title)
async def process_knowledge_title(message: Message, state: FSMContext):
    """Обработка названия темы"""
    title = message.text.strip()
    if not title:
        await message.answer("Пожалуйста, введите название темы:")
        return
    
    # Заменяем пробелы на подчеркивания для OSTIS идентификатора
    ostis_idtf = title.replace(" ", "_").replace("-", "_").lower()
    
    await state.update_data(title=title, ostis_idtf=ostis_idtf)
    await message.answer(
        f"📖 *Тема:* {title}\n"
        f"🔖 *ID в OSTIS:* {ostis_idtf}\n\n"
        "Теперь введите содержание знания:"
    )
    await state.set_state(CreateKnowledgeStates.waiting_for_content)

@router.message(CreateKnowledgeStates.waiting_for_content)
async def process_knowledge_content(message: Message, state: FSMContext):
    """Обработка содержания знания"""
    content = message.text.strip()
    if not content:
        await message.answer("Пожалуйста, введите содержание:")
        return
    
    await state.update_data(content=content)
    
    await message.answer(
        "🎯 Выберите категорию для этого знания:",
        reply_markup=knowledge_categories_keyboard()
    )
    await state.set_state(CreateKnowledgeStates.waiting_for_category)

@router.callback_query(CreateKnowledgeStates.waiting_for_category, F.data.startswith("category_"))
async def process_knowledge_category(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора категории и сохранение в обеих базах"""
    category = callback.data.replace("category_", "")
    
    data = await state.get_data()
    title = data['title']
    ostis_idtf = data['ostis_idtf']
    content = data['content']
    
    await callback.message.answer("🔄 Сохраняю знание в OSTIS систему...")
    
    # 1. СОХРАНЯЕМ В OSTIS (основное хранилище)
    try:
        node = create_node_in_ostis(ostis_idtf, content)
        ostis_success = node is not None
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка сохранения в OSTIS: {e}")
        await state.clear()
        await callback.answer()
        return
    
    if not ostis_success:
        await callback.message.answer(
            "❌ Не удалось сохранить в OSTIS систему. Попробуйте другой идентификатор."
        )
        await state.clear()
        await callback.answer()
        return
    
    await callback.message.answer("✅ Сохранено в OSTIS!\n🔄 Извлекаю данные в векторную БД...")
    
    # 2. ИЗВЛЕКАЕМ ИЗ OSTIS В ВЕКТОРНУЮ БД
    import asyncio
    await asyncio.sleep(1)
    
    # Извлекаем данные из OSTIS в векторную БД
    extracted_data = extract_data_from_ostis(ostis_idtf, node)
    
    if extracted_data:
        vector_success = await rag_data_manager.add_knowledge_item(
            title=ostis_idtf,
            content=extracted_data["content"],
            category=category
        )
    else:
        vector_success = False
    
    if ostis_success and vector_success:
        response = f"✅ *Знание успешно добавлено!*\n\n"
        response += f"📚 *Тема:* {title}\n"
        response += f"🔖 *OSTIS ID:* {ostis_idtf}\n"
        response += f"🎯 *Категория:* {category}\n\n"
        response += f"💾 *Сохранено в:* OSTIS + Векторная БД\n\n"
        response += f"Теперь можете спрашивать ИИ о '{title}'!"
    elif ostis_success:
        response = f"⚠️ *Знание добавлено в OSTIS, но не в векторную БД*\n\n"
        response += f"ИИ может не найти эту информацию сразу. Попробуйте спросить позже."
    else:
        response = "❌ Не удалось сохранить знание."
    
    await callback.message.answer(response)
    await state.clear()
    await callback.answer()

@router.callback_query(F.data == "view_rag_knowledge")
async def view_rag_knowledge(callback: CallbackQuery):
    """Просмотр всех знаний в векторной БД"""
    knowledge_items = await rag_data_manager.get_all_knowledge()
    
    if not knowledge_items:
        await callback.message.answer(
            "📭 Векторная БД пуста.\n\n"
            "Добавьте первое знание через '➕ Добавить знание для ИИ'\n"
            "Или задайте вопрос ИИ - он сам найдет данные в OSTIS!"
        )
        await callback.answer()
        return
    
    response = "📚 *Знания в векторной БД (извлечены из OSTIS):*\n\n"
    
    for i, item in enumerate(knowledge_items, 1):
        source_icon = "🔄 OSTIS" if item.get('source') == 'ostis_kb' else "📝 Пользователь"
        response += f"{i}. *{item['title']}*\n"
        response += f"   {source_icon} | {item['category']}\n"
        response += f"   {item['content_preview']}\n\n"
    
    response += f"Всего знаний: {len(knowledge_items)}"
    
    await callback.message.answer(response)
    await callback.answer()