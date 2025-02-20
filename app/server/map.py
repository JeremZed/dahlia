import json

class Map2D:
    def __init__(self, width=5, height=5, items=None):
        self.width = width
        self.height = height
        self.map = [[0 for _ in range(width)] for _ in range(height)]
        self.items = items if items else []
        self.build()

    def build(self):
        """
            Permet de construire la map en y plaçant pour les objets aux bonnes coordonnées
        """
        for elem in self.items:
            x, y, value = elem
            if 0 <= x < self.width and 0 <= y < self.height:
                self.map[y][x] = value

    def to_json(self):
        """
            Permet de retourner un objet JSON
        """
        return json.dumps({
            "width": self.width,
            "height": self.height,
            "map": self.map
        }, indent=4)

if __name__ == "__main__":

    map_2d = Map2D(
        width= 5,
        height = 5,
        items = [
            (1, 1, { 'type' : 'herbe' }),
            (3, 2, { 'type' : 'mur' }),
            (4, 4, { 'type' : 'portail' })
        ]
    )
    print(map_2d.to_json())