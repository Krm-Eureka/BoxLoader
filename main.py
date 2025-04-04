# main.py
import csv
from loader import load_boxes_from_csv
from pallet import Pallet
from container import F15Container, F9Container
from visualization import plot_pallet


def load_csv_from_file(filepath):
    """
    Loads CSV data from a file.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        str: CSV data as a string, or None if an error occurs.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            csv_data = file.read()
        return csv_data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def main():
    """
    Main function of the program.
    """
    filepath = "D:\\forimport.csv"  # Replace with your actual file path
    csv_data = load_csv_from_file(filepath)

    if csv_data is None:
        return  # Exit if there was an error loading the file

    boxes = load_boxes_from_csv(csv_data)  # Load box data from CSV
    pallet = Pallet(106, 106, 135, frame_height=15)  # Create pallet
    containers =[F15Container()] # Create list of containers

    all_placed_boxes = []
    all_unplaced_boxes = []
    total_container_volume = 0
    total_box_volume = 0

    for container in containers:
        container.x = (pallet.width - container.length) / 2  # Set container x position
        container.y = (pallet.length - container.width) / 2  # Set container y position

        placed, unplaced = pallet.arrange_boxes(  # Arrange boxes on pallet
            boxes,
            container_x=container.x,
            container_y=container.y,
            container_length=container.length,
            container_width=container.width,
            container_height=container.height
        )

        all_placed_boxes.extend(placed)
        all_unplaced_boxes.extend(unplaced)
        total_container_volume += container.length * container.width * container.height
        total_box_volume += sum(box.get_volume() for box in placed)

    # Calculate volume utilization percentage
    volume_utilization = (total_box_volume / total_container_volume) * 100 if total_container_volume > 0 else 0

    print("=" * 70)
    print(f"{'Box Type':<10}{'Priority':<10}{'Position (x,y,z)':<20}{'Dimensions (w,l,h)':<20}")
    print("-" * 70)
    for box in all_placed_boxes:  # Display placed box information
        print(
            f"{box.box_type:<10}{box.priority:<10}{str(box.position):<20}{f'{box.width}x{box.length}x{box.height}':<20}")

    print("\nUnplaced Boxes:")
    for box in all_unplaced_boxes:  # Display unplaced box information
        print(f"- {box}")

    print("\n" + "=" * 70)
    print(f"Total Container Volume: {total_container_volume:.2f} cubic units")
    print(f"Total Box Volume: {total_box_volume:.2f} cubic units")
    print(f"Volume Utilization: {volume_utilization:.2f}%")
    print("=" * 70)

    plot_pallet(pallet, containers)  # Plot pallet and boxes


if __name__ == "__main__":
    main()
