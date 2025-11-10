from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.rag_system import rag_system
from app.keyboards import knowledge_management_keyboard

router = Router()

class RAGStates(StatesGroup):
    waiting_for_question = State()

@router.message(F.text == "💬 Спросить у ИИ")
async def rag_ask_button(message: Message, state: FSMContext):
    """Кнопка для вопроса к RAG системе"""
    await message.answer(
        "💭 Задайте ваш вопрос о здоровье и образе жизни:\n\n"
        "Например:\n"
        "• 'Какие упражнения для пресса?'\n"  
        "• 'Как правильно питаться?'\n"
        "• 'Что такое круговая тренировка?'"
    )
    await state.set_state(RAGStates.waiting_for_question)

@router.callback_query(F.data == "rag_question")
async def rag_question_callback(callback: CallbackQuery, state: FSMContext):
    """Callback для кнопки вопроса к RAG"""
    await callback.message.answer(
        "💭 Задайте ваш вопрос о здоровье и образе жизни:\n\n"
        "Например:\n"
        "• 'Какие упражнения для пресса?'\n"  
        "• 'Как правильно питаться?'\n"
        "• 'Что такое круговая тренировка?'"
    )
    await state.set_state(RAGStates.waiting_for_question)
    await callback.answer()

@router.message(RAGStates.waiting_for_question)
async def process_rag_question(message: Message, state: FSMContext):
    """Обработка вопроса к RAG системе"""
    question = message.text.strip()
    
    if not question:
        await message.answer("Пожалуйста, введите вопрос")
        return
    
    await message.answer("🤔 Ищу ответ в базе знаний...")
    
    answer, sources = await rag_system.ask_question(question)
    
    response = f"❓ *Вопрос:* {question}\n\n"
    response += f"💡 *Ответ:* {answer}\n\n"
    
    if sources:
        response += f"📚 *Источники:* {', '.join(sources)}"
    
    await message.answer(response)
    await state.clear()

@router.message(F.text == "📚 Управление знаниями")
async def knowledge_management(message: Message):
    """Управление знаниями для ИИ"""
    await message.answer(
        "📚 *Управление базой знаний ИИ-ассистента*\n\n"
        "• *OSTIS база* - структурированные знания\n"  
        "• *Векторная БД* - быстрый поиск\n\n"
        "ИИ автоматически находит информацию в OSTIS при вопросах!",
        reply_markup=knowledge_management_keyboard()
    )

@router.callback_query(F.data == "show_rag_db")
async def show_rag_db_callback(callback: CallbackQuery):
    """Показать базу знаний через callback"""
    from app.rag_data_manager import rag_data_manager
    
    knowledge_items = await rag_data_manager.get_all_knowledge()
    
    if not knowledge_items:
        await callback.message.answer(
            "📭 Векторная БД пуста.\n\n"
            "Добавьте знания через:\n"
            "• 'Добавить понятие' - в OSTIS\n"
            "• '➕ Добавить знание' - напрямую\n\n"
            "Или просто задайте вопрос ИИ - он сам найдет данные в OSTIS!"
        )
        await callback.answer()
        return
    
    response = "📚 *Знания в векторной БД:*\n\n"
    
    for i, item in enumerate(knowledge_items, 1):
        source_icon = "🔄 OSTIS" if item['source'] == 'ostis_kb' else "📝 Пользователь"
        response += f"{i}. *{item['title']}*\n"
        response += f"   {source_icon} | {item['category']}\n\n"
    
    response += f"Всего: {len(knowledge_items)} знаний"
    
    await callback.message.answer(response)
    await callback.answer()