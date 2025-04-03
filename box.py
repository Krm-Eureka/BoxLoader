# box.py
class Box:
    def __init__(self, box_type, width, length, height, max_weight, conveyor, priority, qty=1):
        self.box_type = box_type
        self.width = width
        self.length = length
        self.height = height
        self.max_weight = max_weight
        self.conveyor = conveyor
        self.priority = priority
        self.qty = qty
        self.position = None
        self.color = self._assign_color()

    def _assign_color(self):
        color_map = {
            'C12': (1, 0, 0),   # Red
            'C11': (0, 0, 1),   # Blue
            'C3': (0, 1, 0),    # Green
            'C4': (1, 1, 0),    # Yellow
            'C5': (0.5, 0, 0.5), # Purple
            'JP1': (1, 0.5, 0),  # Orange
            'JP2': (0, 1, 1),    # Cyan
            'JP3': (1, 0, 1)     # Magenta
        }
        return color_map.get(self.box_type, (0.7, 0.7, 0.7))  # Default gray if no match

    def get_volume(self):
        return self.width * self.length * self.height

    def can_rotate(self):
        return [
            (self.width, self.length, self.height),
            (self.length, self.width, self.height),
            (self.height, self.width, self.length),
            (self.height, self.length, self.width)
        ]

    def __repr__(self):
        if self.position:
            return f"{self.box_type}(P{self.priority}): {self.width}x{self.length}x{self.height} @ {self.position}"
        return f"{self.box_type}(P{self.priority}): {self.width}x{self.length}x{self.height}"

# ใช้สำหรับสร้าง Box Objects จากตารางข้อมูลที่คุณให้มา
def create_boxes_from_data():
    # ข้อมูลจากตาราง BoxType
    box_data = {
        'C12': (1, 0, 0),    # Red
        'C11': (0, 0, 1),    # Blue
        'C3': (0, 1, 0),     # Green
        'C4': (1, 1, 0),     # Yellow
        'C5': (0.5, 0, 0.5), # Purple
        'C6': (0.8, 0.8, 0), # Light Yellow
        'C22': (0.2, 0.8, 0), # Dark Green
        'C29': (0.8, 0.4, 0), # Brownish Orange
        'C31': (0.4, 0.2, 0.8), # Violet
        'C19': (0.7, 0.7, 0.7), # Grey
        'C13': (0.9, 0.6, 0),  # Gold
        'C15': (0.3, 0.5, 0.1), # Dark Green
        'C16': (0.9, 0.1, 0.4), # Light Red
        'C17': (0.1, 0.9, 0.5), # Mint Green
        'JP1': (1, 0.5, 0),    # Orange
        'JP2': (0, 1, 1),      # Cyan
        'JP3': (1, 0, 1),      # Magenta
        'C1': (0.2, 0.2, 0.8), # Navy Blue
        'C10': (0.8, 0.8, 0.8), # Light Grey
    }

    boxes = []
    for data in box_data:
        box_type, width, length, height, max_weight, conveyor, priority = data
        box = Box(box_type, width, length, height, max_weight, conveyor, priority)
        boxes.append(box)
    return boxes
