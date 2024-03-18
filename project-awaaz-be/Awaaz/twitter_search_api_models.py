class MetaModel:

    def __init__(self, newest_id: str, oldest_id: str, result_count: int):
        self.newest_id = newest_id
        self.oldest_id = oldest_id
        self.result_count = result_count


class DataModel:

    def __init__(self, conversation_id: str, id: str, text: str):
        self.conversation_id = conversation_id
        self.id = id
        self.text = text
