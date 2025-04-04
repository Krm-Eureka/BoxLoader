# box.py
class Box:
    """
    คลาส Box: แทนกล่องสินค้าแต่ละชิ้น
    """
    def __init__(self, box_type, width, length, height, max_weight, conveyor, priority, qty=1):
        """
        Constructor ของคลาส Box
        Args:
            box_type (str): ชนิดของกล่อง (เช่น 'C12', 'C11')
            width (float): ความกว้างของกล่อง (หน่วย: เซนติเมตร)
            length (float): ความยาวของกล่อง (หน่วย: เซนติเมตร)
            height (float): ความสูงของกล่อง (หน่วย: เซนติเมตร)
            max_weight (float): น้ำหนักสูงสุดที่กล่องรับได้ (หน่วย: กิโลกรัม)
            conveyor (int): หมายเลขสายพานลำเลียง
            priority (int): ลำดับความสำคัญในการจัดเรียง (ยิ่งน้อยยิ่งสำคัญ)
            qty (int): จำนวนกล่องชนิดนี้
        """
        self.box_type = box_type
        self.width = width
        self.length = length
        self.height = height
        self.max_weight = max_weight
        self.conveyor = conveyor
        self.priority = priority
        self.qty = qty
        self.position = None  # ตำแหน่งของกล่องบนพาเลท (x, y, z)
        self.color = self._assign_color()  # กำหนดสีของกล่อง

    def _assign_color(self):
        """
        กำหนดสีให้กับกล่องตามชนิดของกล่อง
        Returns:
            tuple: สีของกล่องในรูปแบบ RGB (red, green, blue)
        """
        color_map = {
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
        return color_map.get(self.box_type, (0.7, 0.7, 0.7))  # Default gray if no match

    def get_volume(self):
        """
        คำนวณปริมาตรของกล่อง
        Returns:
            float: ปริมาตรของกล่อง (กว้าง x ยาว x สูง)
        """
        return self.width * self.length * self.height

    def can_rotate(self):
        """
        Allow box rotation for placement.
        """
        return [
            (self.width, self.length, self.height),  # Original orientation
            (self.length, self.width, self.height)  # Rotated orientation
        ]

    def __repr__(self):
        """
        กำหนดรูปแบบการแสดงผลของกล่องเมื่อใช้ print()
        Returns:
            str: ข้อมูลของกล่อง
        """
        if self.position:
            return f"{self.box_type}(P{self.priority}): {self.width * 10}x{self.length * 10}x{self.height * 10} mm @ {self.position}"
        return f"{self.box_type}(P{self.priority}): {self.width * 10}x{self.length * 10}x{self.height * 10} mm"
