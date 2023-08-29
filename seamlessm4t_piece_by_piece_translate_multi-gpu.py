# -*- coding: utf-8 -*-
import json
import argparse
import torch
import time
import logging
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from seamless_communication.models.inference import Translator

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def translate_text(translator, text, src_lang='eng', target_lang='hin'):
    try:
        translated_text, _, _ = translator.predict(text, "t2tt", target_lang, src_lang=src_lang)
        return str(translated_text), False
    except Exception as e:
        logging.warning(f"Failed to translate the whole text: {e}. Attempting sentence-by-sentence translation.")
        sentences = re.split(r'(?<=[.!?])\s+', text)
        translated_sentences = []
        exception_flag = False
        for sentence in sentences:
            try:
                translated_sentence, _, _ = translator.predict(sentence, "t2tt", target_lang, src_lang=src_lang)
                translated_sentences.append(str(translated_sentence))
            except Exception as e:
                logging.error(f"Failed to translate a sentence: {e}")
                translated_sentences.append(sentence)
                exception_flag = True
        return " ".join(translated_sentences), exception_flag

def process_row(row, translator, src_lang, target_lang):
    original_text = row.get('text', '')
    translated_text, exception_flag = translate_text(translator, original_text, src_lang, target_lang)
    row['translated_text'] = translated_text
    if exception_flag:
        row["exception"] = "Partial translation. Sentence-by-sentence translation used."
    return row

if __name__ == "__main__":
    setup_logging()
    
    parser = argparse.ArgumentParser(description='Translate text in JSONL file using SeamlessM4T.')
    parser.add_argument('input_file', type=str, help='Path to the input JSONL file')
    parser.add_argument('output_file', type=str, help='Path to the output JSONL file')
    parser.add_argument('--model_name', type=str, default='seamlessM4T_large', help='SeamlessM4T model name')
    parser.add_argument('--src_lang', type=str, default='eng', help='Source language')
    parser.add_argument('--target_lang', type=str, default='hin', help='Target language')
    parser.add_argument('--limit', type=int, default=None, help='Limit the number of rows to process')
    args = parser.parse_args()

    input_file = args.input_file
    output_file = args.output_file
    model_name = args.model_name
    src_lang = args.src_lang
    target_lang = args.target_lang
    limit = args.limit

    logging.info(f"Initializing model {model_name}...")
    translator = Translator(model_name, "vocoder_36langs", torch.device("cuda"), torch.float16)
    
    start_time = time.time()
    
    with open("exceptions.jsonl", "w") as exc_file:
        pass
    
    logging.info(f"Starting translation from {src_lang} to {target_lang}...")
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = [json.loads(line) for line in infile]
        
        with ThreadPoolExecutor() as executor:
            for i, row in enumerate(tqdm(executor.map(process_row, lines, [translator]*len(lines), [src_lang]*len(lines), [target_lang]*len(lines)), desc="Translating", unit="row")):
                if args.limit is not None and i >= args.limit:
                    break
                if "exception" in row:
                    with open("exceptions.jsonl", "a") as exc_file:
                        exc_file.write(json.dumps(row) + '\n')
                outfile.write(json.dumps(row) + '\n')
                
    elapsed_time = time.time() - start_time
    logging.info(f"Translation completed. Elapsed time: {elapsed_time:.2f} seconds.")

