# pallet.py
import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection 

class Pallet:
    def __init__(self, width, length, height, frame_height=15):
        self.width = width
        self.length = length
        self.height = height
        self.frame_height = frame_height
        self.boxes = []
        self.occupancy_grid = np.zeros((int(width), int(length), int(height)), dtype=bool)

    def is_space_available(self, x, y, z, dx, dy, dz):
        x_end = int(x + dx)
        y_end = int(y + dy)
        z_end = int(z + dz)
        
        if x_end > self.width or y_end > self.length or z_end > self.height:
            return False
            
        return not np.any(self.occupancy_grid[int(x):x_end, int(y):y_end, int(z):z_end])

    def mark_space_occupied(self, x, y, z, dx, dy, dz):
        x_end = int(x + dx)
        y_end = int(y + dy)
        z_end = int(z + dz)
        self.occupancy_grid[int(x):x_end, int(y):y_end, int(z):z_end] = True

    def arrange_boxes(self, boxes, container_x, container_y, container_length, container_width, container_height):
        sorted_boxes = sorted(boxes, key=lambda x: x.priority)
        placed_boxes = []
        unplaced_boxes = []
        
        for box in sorted_boxes:
            for _ in range(box.qty):
                placed = False
                
                for orientation in box.can_rotate():
                    dx, dy, dz = orientation
                    for z in np.arange(self.frame_height, container_height - dz + 1, 1):
                        for y in np.arange(container_y, container_y + container_width - dy + 1, 1):
                            for x in np.arange(container_x, container_x + container_length - dx + 1, 1):
                                if self.is_space_available(x, y, z, dx, dy, dz):
                                    box.position = (x, y, z)
                                    box.width, box.length, box.height = dx, dy, dz
                                    self.boxes.append(box)
                                    placed_boxes.append(box)
                                    self.mark_space_occupied(x, y, z, dx, dy, dz)
                                    placed = True
                                    break
                            if placed:
                                break
                        if placed:
                            break
                    if placed:
                        break
                    
                if not placed:
                    unplaced_boxes.append(box)
            
        return placed_boxes, unplaced_boxes

    def draw_pallet_frame(self, ax):
        x, y, z = 0, 0, 0
        dx, dy, dz = self.width, self.length, self.frame_height
        
        vertices = np.array([
            [x, y, z], [x+dx, y, z], [x+dx, y+dy, z], [x, y+dy, z],
            [x, y, z+dz], [x+dx, y, z+dz], [x+dx, y+dy, z+dz], [x, y+dy, z+dz]
        ])
        
        edges = [
            [0, 1], [1, 2], [2, 3], [3, 0],  # ฐาน
            [4, 5], [5, 6], [6, 7], [7, 4],  # ด้านบน
            [0, 4], [1, 5], [2, 6], [3, 7]    # ขอบแนวตั้ง
        ]
        
        ax.add_collection3d(Line3DCollection(vertices[edges], color='black', linestyle='dashed', linewidth=2))
