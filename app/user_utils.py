from sc_client.constants import sc_types
from sc_client.models import ScTemplate, ScAddr
from sc_client.client import template_search, delete_elements
from sc_kpm import ScKeynodes
from sc_kpm.utils import (
    create_edges,
    get_link_content_data,
    create_nodes,
    create_links
)
from typing import Dict, Optional
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserManager:
    @staticmethod
    def _create_node(node_type: int, idtf: str = None) -> ScAddr:
        """Создает узел с уникальным идентификатором"""
        logger.info(f"Создание узла: {idtf}")
        if idtf:
            existing_node = ScKeynodes.resolve(idtf, node_type)
            if existing_node.is_valid():
                logger.warning(f"Узел {idtf} уже существует!")
                return existing_node
        
        node = create_nodes(node_type)[0]
        if idtf:
            ScKeynodes.__setattr__(idtf, node)
        logger.info(f"Создан новый узел: {idtf}")
        return node

    @staticmethod
    async def create_user(user_id: int, user_data: Dict[str, str]) -> bool:
        """Создает пользователя в SC-памяти"""
        try:
            logger.info(f"Создание пользователя с ID: {user_id}")
            logger.info(f"Данные пользователя: {user_data}")
            
            # Сначала удаляем старые данные (если есть)
            await UserManager.delete_user(user_id)

            # Создаем уникальный узел пользователя
            user_node_idtf = f"user_{user_id}"
            user_node = UserManager._create_node(sc_types.NODE_CONST, user_node_idtf)
            
            logger.info(f"Создан узел пользователя: {user_node_idtf}")

            relations = {
                'nrel_name': 'name',
                'nrel_age': 'age', 
                'nrel_phone': 'phone'
            }

            for rel_type, data_key in relations.items():
                if data_key in user_data and user_data[data_key]:
                    # Создаем УНИКАЛЬНОЕ отношение для этого пользователя
                    rel_node_idtf = f"{rel_type}_{user_id}"
                    rel_node = UserManager._create_node(sc_types.NODE_CONST_ROLE, rel_node_idtf)
                    
                    logger.info(f"Создано отношение: {rel_node_idtf}")

                    # Создаем ссылку с данными
                    value_content = str(user_data[data_key])
                    value_link = create_links(value_content)[0]
                    
                    logger.info(f"Создана ссылка с данными: {value_content}")

                    # Связываем: user -> value
                    edge = create_edges(
                        sc_types.EDGE_D_COMMON_CONST,
                        user_node,
                        value_link
                    )[0]

                    # Указываем тип связи: rel_node -> edge
                    create_edges(
                        sc_types.EDGE_ACCESS_CONST_POS_PERM,
                        rel_node,
                        edge
                    )

                    # Связываем с общим типом отношения (nrel_name -> rel_node)
                    common_rel_node = ScKeynodes.resolve(rel_type, sc_types.NODE_CONST_ROLE)
                    if common_rel_node.is_valid():
                        create_edges(
                            sc_types.EDGE_ACCESS_CONST_POS_PERM,
                            common_rel_node,
                            rel_node
                        )

            logger.info(f"Пользователь {user_id} успешно создан")
            return True
            
        except Exception as e:
            logger.error(f"Ошибка создания пользователя {user_id}: {e}")
            return False

    @staticmethod
    async def delete_user(user_id: int) -> bool:
        """Удаляет все данные пользователя"""
        try:
            logger.info(f"Удаление пользователя: {user_id}")
            
            user_node = ScKeynodes.resolve(f"user_{user_id}", sc_types.NODE_CONST)
            if not user_node.is_valid():
                logger.info(f"Пользователь {user_id} не найден для удаления")
                return True

            elements_to_delete = []
            
            # Добавляем основной узел пользователя
            elements_to_delete.append(user_node)
            
            # Добавляем связанные узлы отношений
            relations = ["nrel_name", "nrel_age", "nrel_phone"]
            for rel in relations:
                rel_node = ScKeynodes.resolve(f"{rel}_{user_id}", sc_types.NODE_CONST_ROLE)
                if rel_node.is_valid():
                    elements_to_delete.append(rel_node)
            
            # Ищем связанные ссылки через шаблон
            template = ScTemplate()
            template.triple_with_relation(
                user_node,
                sc_types.EDGE_D_COMMON_VAR,
                sc_types.LINK_VAR,
                sc_types.EDGE_ACCESS_VAR_POS_PERM,
                sc_types.NODE_VAR_ROLE
            )
            
            results = template_search(template)
            for result in results:
                # Добавляем все элементы из результата поиска
                for element in result.values():
                    if element and element.is_valid():
                        elements_to_delete.append(element)

            # Удаляем все найденные элементы
            if elements_to_delete:
                delete_elements(*elements_to_delete)
                logger.info(f"Пользователь {user_id} удален. Удалено элементов: {len(elements_to_delete)}")
            else:
                logger.info(f"Пользователь {user_id} не найден для удаления")
                
            return True
            
        except Exception as e:
            logger.error(f"Ошибка удаления пользователя {user_id}: {e}")
            return False

    @staticmethod
    async def is_registered(user_id: int) -> bool:
        """Проверяет, зарегистрирован ли пользователь"""
        try:
            user_node_idtf = f"user_{user_id}"
            user_node = ScKeynodes.resolve(user_node_idtf, sc_types.NODE_CONST)
            
            is_registered = user_node.is_valid()
            logger.info(f"Проверка регистрации пользователя {user_id}: {is_registered}")
            
            return is_registered
            
        except Exception as e:
            logger.error(f"Ошибка проверки регистрации пользователя {user_id}: {e}")
            return False

    @staticmethod
    async def get_user_data(user_id: int) -> Optional[Dict[str, str]]:
        """Получает данные пользователя"""
        try:
            logger.info(f"Получение данных пользователя: {user_id}")
            
            user_node = ScKeynodes.resolve(f"user_{user_id}", sc_types.NODE_CONST)
            if not user_node.is_valid():
                logger.info(f"Пользователь {user_id} не найден")
                return None

            data = {}
            relations = {
                "nrel_name": "name",
                "nrel_age": "age",
                "nrel_phone": "phone"
            }

            for sc_rel, data_key in relations.items():
                rel_node = ScKeynodes.resolve(f"{sc_rel}_{user_id}", sc_types.NODE_CONST_ROLE)
                if not rel_node.is_valid():
                    continue

                # Ищем связь: user_node -> link (через rel_node)
                template = ScTemplate()
                template.triple_with_relation(
                    user_node,
                    sc_types.EDGE_D_COMMON_VAR,
                    sc_types.LINK_VAR,
                    sc_types.EDGE_ACCESS_VAR_POS_PERM,
                    rel_node
                )
                
                results = template_search(template)
                if results:
                    for result in results:
                        link_addr = result.get(2)  # LINK_VAR
                        if link_addr and link_addr.is_valid():
                            content = get_link_content_data(link_addr)
                            if content:
                                data[data_key] = str(content)  # Просто преобразуем в строку
                                break

            logger.info(f"Данные пользователя {user_id}: {data}")
            return data if data else None
            
        except Exception as e:
            logger.error(f"Ошибка получения данных пользователя {user_id}: {e}")
            return None