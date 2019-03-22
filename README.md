Reading Strategies
==================

**Status:** Archive (code is provided as-is, no updates expected).

Overview
--------
We re-implement the original core code that was finished at Tencent AI Lab (Bellevue). We have tested the code and made sure the code has the same performance to the original one reported in the paper.

If you find this code useful, please cite the following paper.

* Improving Machine Reading Comprehension with General Reading Strategies ([arXiv](https://arxiv.org/abs/1810.13441))
```
@inproceedings{sun2019improving,
  title={Improving Machine Reading Comprehension with General Reading Strategies},
  author={Sun, Kai and Yu, Dian and Yu, Dong and Cardie, Claire},
  booktitle={Proceedings of the NAACL-HLT},
  address={Minneapolis, MN},
  url={https://arxiv.org/abs/1810.13441v1},
  year={2019}
}
```

Code
----
You can follow the instructions below to train models for RACE.
* Get necessary files
  1. Go to ```code``` and create a folder named ```data``` in it.
  2. Download RACE from http://www.cs.cmu.edu/~glai1/data/race/, unzip it to ```code/data/``` so that the training, development, and testing sets are in ```code/data/RACE/train```, ```code/data/RACE/dev```, and ```code/data/RACE/test```, respectively.
  3. Execute ```python preprocess.py``` to generate ```race_train.json```, ```race_dev.json```, and ```race_test.json``` in ```code/data```.
  4. Execute ```python gencloze.py``` to generate ```race_train.json```, ```race_dev.json```, and ```race_test.json``` in ```code/cloze```.
  5. Download pre-trained language model from https://github.com/openai/finetune-transformer-lm, and copy the model folder ```model``` to ```code/```.
* Train a model with the original input sequence (i.e., ```[dq$o]``` where ```d```, ```q```, ```o``` represent document, question, and answer option, respectively, and ```[```, ```$```, ```]``` represent start token, delimiter token, and end token, respectively).
  1. Execute ```python train.py --submit --n_iter 1 --data_dir cloze/``` to fine-tune the original pre-trained model on the automatically generated cloze questions.
  2. Execute ```python train.py --submit --n_iter 5 --resume``` to fine-tune the model to RACE dataset with 5 training epochs.
* Train a model with the reverse input sequence (i.e., ```[o$qd]```)
  1. ```python train.py --submit --n_iter 1 --data_dir cloze/ --submission_dir submission_oqd/ --save_dir save_oqd/  --log_dir log_oqd/```.
  2. ```python train.py --submit --n_iter 5 --resume --submission_dir submission_oqd/  --save_dir save_oqd/ --log_dir log_oqd/```.
* Get the accuracy on the test set of each single model and the ensemble model.
  1. ```python evaluate.py```.

**Tips:**
 1. You may want to specify ```--n_gpu``` (e.g., 8) and ```--n_batch``` (e.g., 1) based on your environment.
 2. There is randomness in both cloze question generation and model training, so you may want to run multiple times to choose the best model based on development set performance. You may also want to set different seeds (specify ```--seed``` when running ```train.py```).


Environment
-----------
The code has been tested with Python 3.6/3.7, Tensorflow 1.4, and Tesla P40. 
