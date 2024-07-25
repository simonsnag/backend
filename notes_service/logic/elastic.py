from elasticsearch7 import AsyncElasticsearch
from models.note import Note
from schemas.note import DisplayNoteSchema
from settings import es_settings
from settings import logger

elastic_client = AsyncElasticsearch(
    hosts=[{"host": es_settings.es_host, "port": es_settings.es_port}]
)

INDEX_NAME = "notes_index"
INDEX_MAPPINGS = {
    "properties": {
        "id": {"type": "keyword"},
        "user_id": {"type": "keyword"},
        "title": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "content": {
            "type": "text",
            "fields": {"keyword": {"type": "keyword"}},
        },
    }
}
INDEX_SETTINGS = {"number_of_shards": 5, "number_of_replicas": 2}


async def check_and_create_index():
    try:
        await elastic_client.indices.get(index=INDEX_NAME)
        logger.info(f"Индекс'{INDEX_NAME}' уже существует.")
    except Exception:
        logger.info(f"Индекс '{INDEX_NAME}' не существует. Создаю индекс...")
        await elastic_client.indices.create(
            index=INDEX_NAME,
            mappings=INDEX_MAPPINGS,
            settings=INDEX_SETTINGS,
        )
        logger.info(f"Индекс '{INDEX_NAME}' создан.")
    return True


async def add_note_to_es(note: Note):
    await check_and_create_index()
    try:
        await elastic_client.index(index=INDEX_NAME, document=note.model_dump())
        logger.info("Заметка загружена в Elastic.")
    except Exception:
        logger.warning("Не удалось загрузить заметку в Elastic.")


async def search_note_logic(user_id: str, query: str):
    query_body = {
        "bool": {
            "filter": {"term": {"user_id": user_id}},
            "must": [
                {
                    "multi_match": {
                        "query": query,
                        "fields": ["title", "content"],
                        "type": "best_fields",
                        "fuzziness": "AUTO",
                        "operator": "and",
                    }
                }
            ],
        }
    }
    try:
        result = await elastic_client.search(index=INDEX_NAME, query=query_body)
        found_notes = []
        for note in result["hits"]["hits"]:
            found_notes.append(DisplayNoteSchema.model_validate(note["_source"]))
        logger.info("Найдены заметки.")
        return found_notes
    except Exception as e:
        logger.warning(f"Поиск не дал результатов: {e}")
        return []
