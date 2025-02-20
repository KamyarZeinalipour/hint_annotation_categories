# CSV Annotation Tool

## Overview
This tool allows annotators to categorize data from a CSV file using a user-friendly Gradio interface. The progress of annotation is displayed to track how much work is completed.

## Requirements
Make sure you have the following installed:

- Python 3.x
- Required Python packages:
  ```bash
  pip install pandas gradio
  ```

## Usage
Run the script using the following command:

```bash
python annotation_tool.py <annotator_name> <input_file_path>
```

### Parameters:
- `<annotator_name>`: Name of the annotator (used for output file naming)
- `<input_file_path>`: Path to the input CSV file containing the data to annotate

### Example:
```bash
python annotation_tool.py JohnDoe dataset.csv
```

## CSV Format
The input CSV must contain the following columns:
- `title`
- `context`
- `question`
- `extracted_answer`
- `category`

The script will create an output file named:
```bash
<dataset>_annotated_<annotator_name>.csv
```

## How It Works
1. The script loads the input CSV.
2. If an annotation file exists, it resumes from the last annotated item.
3. The annotator selects the correct category or chooses **"No Change"**.
4. Progress is displayed in the status box (e.g., **"20 of 2000 completed"**).
5. The annotated file is saved after each entry.
6. Once all annotations are completed, the tool notifies the user.

## Output File
The output CSV will include two new columns:
- `category_annotated`: The selected category.
- `modified_flag`: Shows whether the category was changed.

## Notes
- Do **not** modify the CSV structure manually while annotating.
- If all annotations are completed, the script will exit automatically.

## Troubleshooting
- If the tool does not start, check that your input CSV is correctly formatted.
- Ensure all required dependencies are installed.
- If the script closes immediately, check the terminal for errors (e.g., missing columns or incorrect file paths).

Happy Annotating! 🎉

