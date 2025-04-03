# main.py
from loader import load_boxes_from_csv
from pallet import Pallet
from container import Container
from visualization import plot_pallet

def main():
    csv_data = """BoxType,w,l,h,Max weight,conveyor,Priority,QTY
C12,380,295,150,50,1,1,1
C12,380,295,150,50,1,2,1
C12,380,295,150,50,1,3,1
C12,380,295,150,50,1,4,1
C12,380,295,150,50,1,5,1
C22,620,250,290,100,1,6,1
C12,380,295,150,50,1,7,1
C12,380,295,150,50,1,9,1
C29,540,355,160,30,1,8,1
C16,1010,190,145,50,1,10,1
"""
    
    boxes = load_boxes_from_csv(csv_data)
    
    pallet = Pallet(106, 106, 135, frame_height=15)
    
    container = Container("F15", 100, 100, 106, 2, "brown", 0.4)
    container.x = (pallet.width - container.length)/2
    container.y = (pallet.length - container.width)/2

    placed, unplaced = pallet.arrange_boxes(
        boxes,
        container_x=container.x,
        container_y=container.y,
        container_length=container.length,
        container_width=container.width,
        container_height=container.height
    )
    
    print("="*70)
    print(f"{'Box Type':<10}{'Priority':<10}{'Position (x,y,z)':<20}{'Dimensions (w,l,h)':<20}")
    print("-"*70)
    for box in placed:
        print(f"{box.box_type:<10}{box.priority:<10}{str(box.position):<20}{f'{box.width}x{box.length}x{box.height}':<20}")
    
    print("\nUnplaced Boxes:")
    for box in unplaced:
        print(f"- {box}")
    
    plot_pallet(pallet, container)

if __name__ == "__main__":
    main()
