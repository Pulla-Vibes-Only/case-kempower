class Rooms:
    def __init__(self, rooms: dict[int, dict]):
        self.__rooms = rooms

    def get_sections(self, room_id: int):
        return list(self.__rooms.get(room_id, {}).get("sections", {}).keys())

    def get_brightness(self, room_id: int, section: str):
        return (
            self.__rooms
            .get(room_id, {})
            .get("sections", {})
            .get(section, {})
            .get("brightness")
        )
    
if __name__ == "__main__":
    rooms = {
        101: {
            "sections": {
                "bathroom": {"brightness": 70, "color": "white"},
                "bed": {"brightness": 40, "color": "white"},
                "main": {"brightness": 0, "color": "white"}
            }
        },
        102: {
            "sections": {
                "bathroom": {"brightness": 60, "color": "white"},
                "bed": {"brightness": 30, "color": "white"},
                "main": {"brightness": 80, "color": "white"}
            }
        }
    }
    r = Rooms(rooms)

    print(r.get_brightness(101, "bed"))
    print(r.get_sections(102))