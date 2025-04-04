# pallet.py
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection


class Pallet:
    """
    คลาส Pallet: แทนพาเลทสำหรับวางกล่อง
    """

    def __init__(self, width, length, height, frame_height=15):
        """
        Constructor ของคลาส Pallet
        Args:
            width (float): ความกว้างของพาเลท (หน่วย: เซนติเมตร)
            length (float): ความยาวของพาเลท (หน่วย: เซนติเมตร)
            height (float): ความสูงของพาเลท (หน่วย: เซนติเมตร)
            frame_height (float): ความสูงของโครงพาเลท (หน่วย: เซนติเมตร)
        """
        self.width = width
        self.length = length
        self.height = height
        self.frame_height = frame_height
        self.boxes = []  # รายการกล่องที่วางบนพาเลท
        self.occupancy_grid = np.zeros((int(width), int(length), int(height)), dtype=bool)  # ตารางแสดงพื้นที่ที่ถูกจอง

    def is_space_available(self, x, y, z, dx, dy, dz):
        """
        ตรวจสอบว่ามีพื้นที่ว่างสำหรับวางกล่องหรือไม่
        Args:
            x (float): ตำแหน่ง x ของมุมล่างซ้ายของกล่อง
            y (float): ตำแหน่ง y ของมุมล่างซ้ายของกล่อง
            z (float): ตำแหน่ง z ของมุมล่างซ้ายของกล่อง
            dx (float): ความกว้างของกล่อง
            dy (float): ความยาวของกล่อง
            dz (float): ความสูงของกล่อง
        Returns:
            bool: True หากมีพื้นที่ว่าง, False หากไม่มี
        """
        x_end = int(x + dx)
        y_end = int(y + dy)
        z_end = int(z + dz)

        # ตรวจสอบว่ากล่องเกินขอบเขตของพาเลทหรือไม่
        if x_end > self.width or y_end > self.length or z_end > self.height:
            return False

        # ตรวจสอบว่ามีพื้นที่ทับซ้อนกับกล่องอื่นหรือไม่
        return not np.any(self.occupancy_grid[int(x):x_end, int(y):y_end, int(z):z_end])

    def mark_space_occupied(self, x, y, z, dx, dy, dz):
        """
        ทำเครื่องหมายว่าพื้นที่ถูกจองแล้ว
        Args:
            x (float): ตำแหน่ง x ของมุมล่างซ้ายของกล่อง
            y (float): ตำแหน่ง y ของมุมล่างซ้ายของกล่อง
            z (float): ตำแหน่ง z ของมุมล่างซ้ายของกล่อง
            dx (float): ความกว้างของกล่อง
            dy (float): ความยาวของกล่อง
            dz (float): ความสูงของกล่อง
        """
        x_end = int(x + dx)
        y_end = int(y + dy)
        z_end = int(z + dz)
        self.occupancy_grid[int(x):x_end, int(y):y_end, int(z):z_end] = True

    def arrange_boxes(self, boxes, container_x, container_y, container_length, container_width, container_height):
        """
        จัดเรียงกล่องบนพาเลท
        Args:
            boxes (list): รายการกล่องที่จะจัดเรียง
            container_x (float): ตำแหน่ง x ของตู้คอนเทนเนอร์บนพาเลท
            container_y (float): ตำแหน่ง y ของตู้คอนเทนเนอร์บนพาเลท
            container_length (float): ความยาวของตู้คอนเทนเนอร์
            container_width (float): ความกว้างของตู้คอนเทนเนอร์
            container_height (float): ความสูงของตู้คอนเทนเนอร์
        Returns:
            tuple: รายการกล่องที่วางได้, รายการกล่องที่วางไม่ได้
        """
        sorted_boxes = sorted(boxes, key=lambda x: x.priority)  # เรียงกล่องตามลำดับความสำคัญ
        placed_boxes = []  # รายการกล่องที่วางได้
        unplaced_boxes = []  # รายการกล่องที่วางไม่ได้

        for box in sorted_boxes:
            for _ in range(box.qty):  # วนซ้ำตามจำนวนกล่อง
                placed = False

                for orientation in box.can_rotate():  # ลองหมุนกล่องในทุกรูปแบบ
                    dx, dy, dz = orientation
                    # Iterate through z-levels first, then y, then x
                    for z in np.arange(self.frame_height, container_height - dz + 1, 1):
                        # Start from the edge (container_y) and move inward
                        for y in np.arange(container_y, container_y + container_width - dy + 1, 1):
                            # Start from the edge (container_x) and move inward
                            for x in np.arange(container_x, container_x + container_length - dx + 1, 1):
                                if self.is_space_available(x, y, z, dx, dy, dz):  # ตรวจสอบพื้นที่ว่าง
                                    box.position = (x, y, z)  # กำหนดตำแหน่งกล่อง
                                    box.width, box.length, box.height = dx, dy, dz  # กำหนดขนาดกล่อง
                                    self.boxes.append(box)  # เพิ่มกล่องลงในพาเลท
                                    placed_boxes.append(box)  # เพิ่มกล่องลงในรายการกล่องที่วางได้
                                    self.mark_space_occupied(x, y, z, dx, dy, dz)  # ทำเครื่องหมายว่าพื้นที่ถูกจอง
                                    placed = True
                                    break  # Break out of x loop
                            if placed:
                                break  # Break out of y loop
                        if placed:
                            break  # Break out of z loop
                    if placed:
                        break  # Break out of orientation loop

                if not placed:
                    unplaced_boxes.append(box)  # เพิ่มกล่องลงในรายการกล่องที่วางไม่ได้

        return placed_boxes, unplaced_boxes

    def draw_pallet_frame(self, ax):
        """
        วาดโครงพาเลทลงบนกราฟ 3 มิติ
        Args:
            ax (matplotlib.axes._subplots.Axes3DSubplot): แกนของกราฟ 3 มิติ
        """
        x, y, z = 0, 0, 0
        dx, dy, dz = self.width, self.length, self.frame_height

        # กำหนดจุดยอดของโครงพาเลท
        vertices = np.array([
            [x, y, z], [x + dx, y, z], [x + dx, y + dy, z], [x, y + dy, z],
            [x, y, z + dz], [x + dx, y, z + dz], [x + dx, y + dy, z + dz], [x, y + dy, z + dz]
        ])

        # กำหนดขอบของโครงพาเลท
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # ฐาน
            [4, 5], [5, 6], [6, 7], [7, 4],  # ด้านบน
            [0, 4], [1, 5], [2, 6], [3, 7]  # ขอบแนวตั้ง
        ]

        # วาดขอบของโครงพาเลทลงบนกราฟ
        ax.add_collection3d(Line3DCollection(vertices[edges], color='black', linestyle='dashed', linewidth=2))
