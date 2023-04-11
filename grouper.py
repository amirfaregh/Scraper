from PIL import Image
import os

# Set the folder path containing the images to be grouped
folder_path = "C:/Users/amirf/Desktop/1/1"

# Get a list of all image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]

# Create a new blank image to group the four images
group_image = Image.new('RGB', (1080, 2020), (255, 255, 255))

# Iterate through the list of image files and group them into a single image
for i in range(0, len(image_files), 4):
    # Open each image and paste it into the group image
    for j in range(4):
        if i + j < len(image_files):
            image = Image.open(os.path.join(folder_path, image_files[i+j]))
            image = image.resize((560, 960), Image.ANTIALIAS)
            x = j % 2 * 540
            y = j // 2 * 960 + 150  # add 100 pixels to top margin
            group_image.paste(image, (x, y))

    # Save the group image with a unique name
    group_image.save(os.path.join(folder_path, 'grouped_{}.jpg'.format(i//4)))

    # Reset the group image for the next batch
    group_image = Image.new('RGB', (1080, 2020), (255, 255, 255))
