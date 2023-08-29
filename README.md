# SeamlessM4T Piece-By-Piece Translation

![SeamlessM4T Logo](seamlessM4T.png)

## Overview

SeamlessM4T is designed to provide high-quality translation, allowing people from different linguistic communities to communicate effortlessly through speech and text. This repository contains a Python script that leverages the state-of-the-art SeamlessM4T model to translate text stored in a JSONL file. The script is highly configurable and allows you to specify the model, source language, target language, and other parameters. It also has built-in resilience to handle translation failures by falling back to sentence-by-sentence translation.

## Features

- Translation of text using the SeamlessM4T model.
- Command-line arguments for easy customization.
- The ability to start processing from an arbitrary row in the input file.
- Sentence-by-sentence translation as a fallback mechanism.
- Logging of translation exceptions and performance metrics.

SeamlessM4T covers:
- 📥 101 languages for speech input.
- ⌨️ 96 Languages for text input/output.
- 🗣️ 35 languages for speech output.

This unified model enables multiple tasks without relying on multiple separate models:
- Speech-to-speech translation (S2ST)
- Speech-to-text translation (S2TT)
- Text-to-speech translation (T2ST)
- Text-to-text translation (T2TT)
- Automatic speech recognition (ASR)

## Requirements

- Python 3.x
- PyTorch
- seamless_communication.models.inference (SeamlessM4T library)
- tqdm for progress bars
- argparse for command-line arguments

# Quick Start
## Installation

```
pip install .
```

A temporary extra requirement for fairseq2 is [libsndfile](https://github.com/libsndfile/libsndfile). From [Conda](https://docs.conda.io/en/latest/) environment it can be installed via:
```
conda install -y -c conda-forge libsndfile
```

## Usage

### Basic Command Structure

```bash
python seamlessm4t_piece_by_piece_translation.py <input_file> <output_file> [options]
```

### Arguments and Options

- `input_file`: Path to the input JSONL file containing the text to be translated.
- `output_file`: Path to the output JSONL file where the translated text will be stored.
- `--model_name`: Name of the SeamlessM4T model to use (default is `seamlessM4T_large`).
- `--src_lang`: Source language (default is `eng`).
- `--target_lang`: Target language to translate into (default is `hin`).
- `--start_row`: Row number to start processing from (default is 0).
- `--limit`: Limit the number of rows to process (default is None, meaning all rows).

### Example Usage

To translate text from an input file `Puffin_filtered_with_text.jsonl` to an output file `output_780_next.jsonl` using the SeamlessM4T_large model, translating from English to Hindi, and starting from the 780th row:

```bash
python seamlessm4t_piece_by_piece_translation.py Puffin_filtered_with_text.jsonl output_780_next.jsonl --model_name seamlessM4T_large --src_lang eng --target_lang hin --start_row 780
```

## Logging

- Logs are generated with timestamps, providing insights into the translation process and performance metrics.
- Exceptions during translation are written to an `exceptions.jsonl` file for further investigation.

## License

This project is licensed under the CC-BY-NC License. See the `LICENSE.md` file for details.

