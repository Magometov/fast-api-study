import json

from pydantic import BaseModel

class BaseRepository[_MT: BaseModel]:
    file_name: str
    model: type[_MT]

    def get_all(self) -> list[_MT]:
        with open(self.file_name, 'r') as file:
            result = json.load(file)
            return [self.model.model_validate(res) for res in result]

    def create(self, instance: _MT) -> _MT:
        data = self.get_all()
        with open(self.file_name, 'w') as file:
            data.append(instance)
            data_json = [el.model_dump(mode='json') for el in data]
            json.dump(data_json, file)
        return instance
