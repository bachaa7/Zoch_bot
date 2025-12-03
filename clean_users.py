from sc_client.client import connect, is_connected
from sc_client.constants import sc_types
from sc_kpm import ScKeynodes
from sc_client.models import ScTemplate
from sc_client.client import template_search, delete_elements

def simple_clean():
    """Простая очистка пользователя со связями"""
    connect("ws://localhost:8090/ws_json")
    
    user_id = 1539623821
    user_node_idtf = f"user_{user_id}"
    user_node = ScKeynodes.resolve(user_node_idtf, sc_types.NODE_CONST)
    
    if not user_node.is_valid():
        print("❌ Пользователь не найден")
        return
    
    elements_to_delete = [user_node]
    
    # Простой поиск связей: user -> edge -> something
    template = ScTemplate()
    template.triple(
        user_node,
        sc_types.EDGE_D_COMMON_VAR,
        sc_types.NODE_VAR
    )
    
    try:
        results = template_search(template)
        for result in results:
            for key, element in result.items():
                if element and element.is_valid():
                    elements_to_delete.append(element)
                    print(f"🗑️ Найдена связь: {key}")
    except Exception as e:
        print(f"⚠️ Ошибка поиска связей: {e}")
    
    # Добавляем узлы отношений
    relations = ["nrel_name", "nrel_age", "nrel_phone"]
    for rel in relations:
        rel_node = ScKeynodes.resolve(f"{rel}_{user_id}", sc_types.NODE_CONST_ROLE)
        if rel_node.is_valid():
            elements_to_delete.append(rel_node)
            print(f"🗑️ Найдено отношение: {rel}_{user_id}")
    
    if elements_to_delete:
        print(f"🔄 Удаляю {len(elements_to_delete)} элементов...")
        delete_elements(*elements_to_delete)
        print("✅ Очистка завершена!")
    else:
        print("ℹ️ Нечего удалять")

if __name__ == "__main__":
    simple_clean()