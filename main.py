# main.py
import csv
import time
import os  # Import the os module
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
    print("Process: Loading CSV data from file...")  # Print process
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            csv_data = file.read()
        print("Process: CSV data loaded successfully.")  # Print process
        return csv_data
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def export_to_csv(filename, boxes):
    """
    Exports box data to a CSV file in the D:\BoxLoadExport folder.

    Args:
        filename (str): The name of the CSV file.
        boxes (list): List of Box objects to export.
    """
    export_dir = "D:\\BoxLoadExport"  # Define the export directory
    os.makedirs(export_dir, exist_ok=True)  # Create the directory if it doesn't exist
    filepath = os.path.join(export_dir, filename)  # Create the full file path

    with open(filepath, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Box Type', 'Priority', 'Position X', 'Position Y', 'Position Z', 'Dimensions (w,l,h) (mm)', 'Quantity'])
        for box in boxes:
            writer.writerow([
                box.box_type, box.priority, box.position[0], box.position[1], box.position[2],
                f"{box.width * 10}x{box.length * 10}x{box.height * 10}", box.qty
            ])


def main():
    """
    Main function of the program.
    """
    start_time = time.time()  # Record the start time
    print(f"Start Time: {time.ctime(start_time)}")

    filepath = "D:\\forimport.csv"  # Replace with your actual file path
    csv_data = load_csv_from_file(filepath)

    if csv_data is None:
        return  # Exit if there was an error loading the file

    print("Process: Loading box data from CSV...")  # Print process
    boxes = load_boxes_from_csv(csv_data)  # Load box data from CSV
    print("Process: Box data loaded successfully.")  # Print process
    print("Process: Creating pallet...")  # Print process
    pallet = Pallet(106, 106, 135, frame_height=15)  # Create pallet
    print("Process: Pallet created successfully.")  # Print process
    print("Process: Creating containers...")  # Print process
    containers = [F15Container()]  # Create list of containers
    print("Process: Containers created successfully.")  # Print process

    all_placed_boxes = []
    all_unplaced_boxes = []
    total_container_volume = 0
    total_box_volume = 0

    for container in containers:
        container.x = (pallet.width - container.length) / 2  # Set container x position
        container.y = (pallet.length - container.width) / 2  # Set container y position
        print(f"Process: Processing container: {container.container_type}")  # Print process

        print("Process: Arranging boxes on pallet...")  # Print process
        placed, unplaced = pallet.arrange_boxes(  # Arrange boxes on pallet
            boxes,
            container_x=container.x,
            container_y=container.y,
            container_length=container.length,
            container_width=container.width,
            container_height=container.height
        )
        print("Process: Boxes arranged on pallet.")  # Print process

        # Stop calculation if no boxes can be placed
        if not placed:
            print("No boxes could be placed. Moving remaining boxes to roller and stopping calculation.")
            all_unplaced_boxes.extend(unplaced)
            break

        # Check if any box's z position approaches the container's height minus 20 cm
        for box in placed:
            if box.position[2] + box.height >= container.height - 20:
                print("Box height approaches container height limit. Moving remaining boxes to roller and stopping calculation.")
                all_unplaced_boxes.extend(unplaced)
                all_unplaced_boxes.extend(placed)
                placed = []
                break

        all_placed_boxes.extend(placed)
        all_unplaced_boxes.extend(unplaced)
        total_container_volume += container.length * container.width * container.height

        # Print during calculation of total box volume
        print("Process: Calculating total box volume...")
        for box in placed:
            box_volume = box.get_volume()
            print(f"  - Calculating volume for box {box.box_type}: {box_volume}")
            total_box_volume += box_volume
        print(f"Process: Total box volume calculated: {total_box_volume}")

    # Calculate volume utilization percentage
    print("Process: Calculating volume utilization...")  # Print process
    volume_utilization = (total_box_volume / total_container_volume) * 100 if total_container_volume > 0 else 0
    print(f"Volume Utilization: {volume_utilization:.2f}%")  # Display on screen
    print("Process: Volume utilization calculated.")  # Print process

    print("=" * 70)
    print(f"{'Box Type':<10}{'Priority':<10}{'Position (x,y,z)':<20}{'Dimensions (w,l,h)':<20}")
    print("-" * 70)
    print("Process: Displaying placed box information...")  # Print process
    for box in all_placed_boxes:  # Display placed box information
        print(
            f"{box.box_type:<10}{box.priority:<10}{str(box.position):<20}{f'{box.width}x{box.length}x{box.height}':<20}")
    print("Process: Placed box information displayed.")  # Print process

    print("\nUnplaced Boxes:")
    print("Process: Displaying unplaced box information...")  # Print process
    for box in all_unplaced_boxes:  # Display unplaced box information
        print(f"- {box}")
    print("Process: Unplaced box information displayed.")  # Print process

    print("\n" + "=" * 70)
    print(f"Total Container Volume: {total_container_volume:.2f} cubic units")
    print(f"Total Box Volume: {total_box_volume:.2f} cubic units")
    print(f"Volume Utilization: {volume_utilization:.2f}%")
    
    Cal_time = time.time()  # Record the end time
    elapsed_Cal_time = Cal_time - start_time
    print(f"Total Calculate Time: {elapsed_Cal_time:.4f} seconds")
    print("Process: Plotting pallet and boxes...")  # Print process
    print(f"Debug: Calculated Volume Utilization = {volume_utilization:.2f}%")  # Debugging
    plot_pallet(pallet, containers, utilization=volume_utilization)  # Pass utilization to visualization
    print("Process: Pallet and boxes plotted.")  # Print process

    # Print the count of placed and unplaced boxes
    print(f"Number of boxes placed: {len(all_placed_boxes)}")
    print(f"Number of boxes unplaced: {len(all_unplaced_boxes)}")
    print("=" * 70)
    end_time = time.time()  # Record the end time
    print(f"End Time: {time.ctime(end_time)}")
    elapsed_time = end_time - start_time  # Calculate the elapsed time
    print(f"Total Execution Time: {elapsed_time:.4f} seconds")
    print("Finished")

    export_to_csv('placed.csv', all_placed_boxes)
    export_to_csv('to_free_roller.csv', all_unplaced_boxes)  # Export กล่องที่วางไม่ได้


if __name__ == "__main__":
    main()
