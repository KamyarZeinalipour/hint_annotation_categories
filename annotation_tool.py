import argparse
import os
import pandas as pd
import gradio as gr

def main(annotator_name, input_file_path):
    if not os.path.isfile(input_file_path):
        print(f"Input file {input_file_path} does not exist.")
        return
    
    df_input = pd.read_csv(input_file_path)
    required_columns = ['title', 'context', 'question', 'extracted_answer', 'category']
    for col in required_columns:
        if col not in df_input.columns:
            print(f"Column '{col}' is missing in the input CSV.")
            return
    
    input_filename = os.path.splitext(os.path.basename(input_file_path))[0]
    output_file_path = f"{input_filename}_annotated_{annotator_name}.csv"
    
    df_output = df_input.copy()
    if os.path.isfile(output_file_path):
        df_output = pd.read_csv(output_file_path)
        print(f"Resuming annotations using existing output file {output_file_path}.")
    else:
        if 'category_annotated' not in df_output.columns:
            df_output['category_annotated'] = pd.NA
        if 'modified_flag' not in df_output.columns:
            df_output['modified_flag'] = pd.NA
    
    total_annotations = len(df_output)
    unannotated_indices = df_output[df_output['category_annotated'].isna()].index.tolist()
    completed_annotations = total_annotations - len(unannotated_indices)
    
    if not unannotated_indices:
        print("All rows have been annotated.")
        return
    
    current_index = unannotated_indices[0]
    
    def annotate(category_annotated):
        nonlocal current_index, unannotated_indices, completed_annotations
        
        original_category = df_output.at[current_index, 'category']
        
        if category_annotated != "No Change":
            df_output.at[current_index, 'category_annotated'] = category_annotated
        else:
            df_output.at[current_index, 'category_annotated'] = original_category
        
        df_output.at[current_index, 'modified_flag'] = 'Changed' if category_annotated != "No Change" else 'No Change'
        df_output.to_csv(output_file_path, index=False)
        
        unannotated_indices = df_output[df_output['category_annotated'].isna()].index.tolist()
        completed_annotations = total_annotations - len(unannotated_indices)
        
        if unannotated_indices:
            current_index = unannotated_indices[0]
            return (df_output.at[current_index, 'title'], df_output.at[current_index, 'context'],
                    df_output.at[current_index, 'question'], df_output.at[current_index, 'extracted_answer'],
                    df_output.at[current_index, 'category'], "No Change",
                    f"Annotation saved. ({completed_annotations} of {total_annotations} completed)")
        else:
            return ("", "", "", "", "", "No Change", "Annotation complete! All rows have been annotated.")
    
    initial_values = [df_output.at[current_index, col] for col in required_columns]
    
    with gr.Blocks() as demo:
        gr.Markdown(f"# CSV Annotation Tool - Annotator: {annotator_name}")
        
        with gr.Row():
            with gr.Column():
                title_box = gr.Textbox(value=initial_values[0], label="Title", interactive=False)
                context_box = gr.Textbox(value=initial_values[1], label="Context", interactive=False)
                question_box = gr.Textbox(value=initial_values[2], label="Question", interactive=False)
            
            with gr.Column():
                extracted_answer_box = gr.Textbox(value=initial_values[3], label="Extracted Answer", interactive=False)
                category_box = gr.Textbox(value=initial_values[4], label="Category", interactive=False)
                category_radio = gr.Radio(["No Change", "person", "place", "quantity", "time", "general"], label="Correct Category?", value="No Change")
        
        submit_button = gr.Button("Save Annotation", interactive=False)
        status = gr.Textbox(value=f"{completed_annotations} of {total_annotations} completed", interactive=False, label="Status")

        def enable_button(selected_option):
            return gr.update(interactive=bool(selected_option))
        
        category_radio.change(enable_button, inputs=[category_radio], outputs=[submit_button])
        
        submit_button.click(annotate, inputs=[category_radio],
                            outputs=[title_box, context_box, question_box, extracted_answer_box,
                                     category_box, category_radio, status])
        
        submit_button.click(lambda: "No Change", outputs=[category_radio])
        
    demo.launch()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CSV Annotation Tool")
    parser.add_argument("annotator_name", help="Name of the annotator")
    parser.add_argument("input_file_path", help="Path to the input CSV file")
    
    args = parser.parse_args()
    main(args.annotator_name, args.input_file_path)
