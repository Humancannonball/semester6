import os
# import argparse # No longer needed for this specific batch processing
from PIL import Image as PILImage # Use an alias to avoid conflict with reportlab.graphics.Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4 # Or letter, etc.

def create_pdf_from_pngs(image_folder, output_pdf_filename):
    """
    Creates a PDF from all PNG images in a specified folder.
    Each page will contain one image and its filename.

    Args:
        image_folder (str): Path to the folder containing PNG images.
        output_pdf_filename (str): Desired name for the output PDF file.
    """

    if not os.path.isdir(image_folder):
        print(f"Error: Folder '{image_folder}' not found.")
        return

    # Get all PNG files, sort them by modification date (oldest first)
    # If modification date is not available or consistent, fallback to alphabetical
    try:
        png_files_with_mtime = []
        for f_name in os.listdir(image_folder):
            if f_name.lower().endswith(".png"):
                full_path = os.path.join(image_folder, f_name)
                png_files_with_mtime.append((os.path.getmtime(full_path), full_path))
        
        # Sort by modification time (the first element of the tuple)
        png_files_with_mtime.sort(key=lambda x: x[0])
        png_files = [item[1] for item in png_files_with_mtime] # Get just the paths
    except Exception as e_sort:
        print(f"Warning: Could not sort by modification date due to '{e_sort}'. Falling back to alphabetical sort.")
        png_files = sorted([
            os.path.join(image_folder, f)
            for f in os.listdir(image_folder)
            if f.lower().endswith(".png")
        ])


    if not png_files:
        print(f"No PNG files found in '{image_folder}'.")
        return

    # --- PDF Setup ---
    doc = SimpleDocTemplate(output_pdf_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Define page dimensions and margins (A4 example)
    page_width, page_height = A4
    margin = 0.75 * inch # 0.75 inch margin on all sides
    
    # Available width and height for content (image + text)
    # We'll reserve some space for the filename text
    filename_text_height_approx = 0.5 * inch
    available_width = page_width - 2 * margin
    available_height_for_image = page_height - 2 * margin - filename_text_height_approx

    print(f"Processing {len(png_files)} PNG files for {output_pdf_filename}...")

    for i, image_path in enumerate(png_files):
        filename = os.path.basename(image_path)
        print(f"  Adding '{filename}' to PDF...")

        # 1. Add Filename
        filename_paragraph = Paragraph(filename, styles['h2']) # Use a heading style for filename
        story.append(filename_paragraph)
        story.append(Spacer(1, 0.2 * inch)) # Add a little space below the filename

        # 2. Add Image
        try:
            # Open image with Pillow to get its dimensions
            pil_img = PILImage.open(image_path)
            img_width_px, img_height_px = pil_img.size

            # Calculate scaling factor to fit image within available space while maintaining aspect ratio
            scale_w = available_width / img_width_px
            scale_h = available_height_for_image / img_height_px
            
            # Use the smaller scaling factor to ensure the whole image fits
            # Also, don't scale up if the image is already smaller than available space
            scale_factor = min(scale_w, scale_h, 1.0) 

            # Create reportlab Image object
            rl_image = Image(image_path)
            rl_image.drawWidth = img_width_px * scale_factor
            rl_image.drawHeight = img_height_px * scale_factor
            rl_image.hAlign = 'CENTER' # Center the image on the page

            story.append(rl_image)

        except Exception as e:
            print(f"  Error processing image '{filename}': {e}")
            # Add a placeholder or error message to the PDF for this image
            error_paragraph = Paragraph(f"Error loading image: {filename}<br/>{e}", styles['Normal'])
            story.append(error_paragraph)

        # 3. Add Page Break (unless it's the last image)
        if i < len(png_files) - 1:
            story.append(PageBreak())

    # --- Build PDF ---
    try:
        doc.build(story)
        print(f"PDF '{output_pdf_filename}' created successfully!")
    except Exception as e:
        print(f"Error building PDF for '{output_pdf_filename}': {e}")
    print("-" * 30)


if __name__ == "__main__":
    base_communications_dir = "/var/home/mark/Documents/semester6/Communications"
    lab_folders_to_process = ["lab3", "lab4", "lab5", "lab6"]

    for lab_folder_name in lab_folders_to_process:
        input_lab_folder = os.path.join(base_communications_dir, lab_folder_name)
        output_lab_pdf = os.path.join(base_communications_dir, f"{lab_folder_name}.pdf")
        
        print(f"Starting PDF generation for {lab_folder_name}...")
        create_pdf_from_pngs(input_lab_folder, output_lab_pdf)
    
    print("All lab PDF processing complete.")