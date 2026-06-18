from datetime import datetime

class Photo:

    def __init__(self, id, timestamp, path, tags: list = None, rating: int = None):
        self._id = int(id)
        self._timestamp = self._parse_ts(timestamp)
        self._path = path
        self._tags = tags if tags else []
        self._rating = rating

    def _parse_ts(self, ts):
        if isinstance(ts, (int, float)):
            return int(ts)

        formatos = (
            "%Y-%m-%d %H:%M:%S",  # Para: YYYY-MM-DD HH:MM:SS
            "%Y-%m-%d %H:%M",     # Para: YYYY-MM-DD HH:MM
            "%Y-%m-%d"            # Para: YYYY-MM-DD
        )
        
        for fmt in formatos:
            try:
                data_objeto = datetime.strptime(ts, fmt)
                return int(data_objeto.timestamp())
            except ValueError:
                continue
        
        raise ValueError(f"Formato de data inválido: {ts}") 
    
    def _key(self):
        return (self.self._timestamp, self._id)

    def __le__(self, other):
        if isinstance(other, Photo):
            return self._key() <= other._key()
        return False

    def __lt__(self, other):
        if isinstance(other, Photo):
            return self._key() < other._key()
        return False

    def __gt__(self, other):
        if isinstance(other, Photo):
            return self._key() > other._key()
        return False

    def __eq__(self, other):
        if isinstance(other, Photo):
            return self._key() == other._key()
        return False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self._timestamp} {self._path}'
