# Extraction of Knowledge Graphs from Historical Handwritten Documents

The website with the visualisation of the result of the thesis can found [here](http://w1t0.github.io/ba-inf-2023-hp-kiefer-scholz-website).

To extract Knowledge Graphs from historical handwritten documents:

- Clone this repository

```
git clone https://github.com/W1T0/bachelorarbeit-inf-2023-hp-code.git
```

# OCR via Transkribus

- Register at [Transkribus](https://readcoop.eu/de/transkribus/)
- Use [Transkribus Lite](https://app.transkribus.eu/) or download the [Transkribus Desktop Client](https://readcoop.eu/transkribus/download/)
- Upload all documents to the Transkribus servers (the files need be PDFs)
- Set the Layout Analysis Configuration to the following:

```
Selected model: Mixed Line Orientation

Baseline detection settings
Minimal baseline length: Low
Baseline accuracy threshold: High
Use trained separators: No
Max-dist for merging baselines: Medium
Image scaling: Default

Region detection settings
Method: Custom
Nr of Text-regions: Medium
```

- Run **Layout Analysis**
- Run **Text Recognition** with the _Transkribus German Kurrent M2 (32524)_ model
- Export the transcriptions as `.txt` files and save them in the folder `./data/kiefer-scholz_collection_transcriptions/`

# NER via flair/ner-german-large, germaNER, sequence_tagging

Because these systems require different programming languages, Python versions and different libraries, it is necessary to set up two virtual machines for germaNER and sequence_tagging, respectively. VirtualBox is suitable and can be installed [here](https://www.virtualbox.org/).

For sequence_tagging Python 3.6 is necessary. Ubuntu 20.04.4 works for this.

For germaNER Java 11 is necessary. Ubuntu 22.10 works for this.

flair/ner-german-large must be installed on the same enviroment as this repository was cloned to.

## Requirements

### To install flair/ner-german-larger, run the following code in a terminal:

```
pip install flair
```

### To install germaNER, download the binary from [this link](https://github.com/tudarmstadt-lt/GermaNER/releases/download/germaNER0.9.1/GermaNER-09-09-2015.jar)

### To install sequence_tagging, you need Python 3.6 (to support Tensorflow 1.3.0) and do the following:

Clone the repository:

```
git clone https://github.com/riedlma/sequence_tagging
```

Navigate to the folder of the repository and install the requirements:

```
cd sequence_tagging
pip3 install -r requirements.txt
```

Install fastText:

```
git clone https://github.com/facebookresearch/fastText.git
cd fastText
pip3 install .
```

Install the german model:

```
cd sequence_tagging
python3 download_model_embeddings.py GermEval
```

## Usage

- Run the script `A1_tokenize_documents.py` in the folder `./code/` manually or with the following command in the main folder:

```
python .\code\A1_tokenize_documents.py
```

- Copy the folder with the tokenized documents (`./data/kiefer-scholz_collection_tokenized/`) into the folders of germaNER and sequence_tagging (`./germaNER/` and `./sequence_tagging/`) on the VMs
- Copy the provided scripts in `./code/NER-systems/` into the respective folder of the systems
- Run the scripts in the folder of the system with the following commands (this can take some time (ca. 30 second per document for germaNER and ca. 6 seconds per document for sequence_tagging))

```
python run_germaNER.py
```

```
python3 run_sequence_tagging.py
```

- Copy the output folders (`./output-germaNER/` and `./output-sequence_tagging/`) into the folder `./data/NER-systems_output/`
- Run the script `A2_TSV_Parser_and_KG_creator` in the folder `./code/` manually or with the following command in the main folder:

```
python .\code\A2_TSV_Parser_and_KG_creator.py
```

- The results are saved in the folder `./visualization/documents/KGs/`

- To visualize the results:
  - Copy the scans of the documents into the folder `./visualization/documents/scans/`
  - Copy the transcriptions exported from Transkribus into the folder `./visualization/documents/transcriptions/`
  - Add the filenames to the `id=filechooser` in `files.html` with the script `create_file-chooser_options.py` in `./code/extra/`
  - Open the file `files.html` with a local server

## flair/ner

### Links:

- [Hugging Face](https://huggingface.co/flair/ner-german-large)
- [Paper](https://arxiv.org/pdf/2011.06993v1.pdf)

### Citation:

```
@misc{schweter2020flert,
  title={FLERT: Document-Level Features for Named Entity Recognition},
  author={Stefan Schweter and Alan Akbik},
  year={2020},
  eprint={2011.06993},
  archivePrefix={arXiv},
  primaryClass={cs.CL}
}
```

## germaNER

### Links:

- [Git Hub](https://github.com/tudarmstadt-lt/GermaNER)
- [Paper](https://www.inf.uni-hamburg.de/en/inst/ab/lt/publications/2015-benikovaetal-gscl2015-germa.pdf)

### Citation:

```
@inproceedings{Benikova2015GermaNERFO,
  title={GermaNER: Free Open German Named Entity Recognition Tool},
  author={Darina Benikova and Seid Muhie Yimam and Prabhakaran Santhanam and Chris Biemann},
  booktitle={International Conference of the German Society for Computational Linguistics and Language Technology (GSCL-2015)},
  year={2015}
}
```

## sequence_tagging

### Links:

- [Git Hub](https://github.com/riedlma/sequence_tagging)
- [Paper](https://aclanthology.org/P18-2020/)

### Citation:

```
@inproceedings{riedl18:_named_entit_recog_shoot_german,
  title = {A Named Entity Recognition Shootout for {German}},
  author = {Riedl, Martin and Padó, Sebastian},
  booktitle = {Proceedings of Annual Meeting of the Association for Computational Linguistics},
  series={ACL 2018},
  address = {Melbourne, Australia},
  note = {To appear},
  year = 2018
}

```

## Visualization via ...
