{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "bZtDpjiatSN-"
   },
   "source": [
    "# KoBERT finetuning"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 115383,
     "status": "ok",
     "timestamp": 1669602057479,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "-sx87sgK7_pz",
    "outputId": "5eeefd5d-b8d9-4001-88fa-41a40873ee2b"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/\n",
      "Requirement already satisfied: ipywidgets in /usr/local/lib/python3.7/dist-packages (7.7.1)\n",
      "Requirement already satisfied: ipython-genutils~=0.2.0 in /usr/local/lib/python3.7/dist-packages (from ipywidgets) (0.2.0)\n",
      "Requirement already satisfied: widgetsnbextension~=3.6.0 in /usr/local/lib/python3.7/dist-packages (from ipywidgets) (3.6.1)\n",
      "Requirement already satisfied: traitlets>=4.3.1 in /usr/local/lib/python3.7/dist-packages (from ipywidgets) (5.1.1)\n",
      "Requirement already satisfied: ipykernel>=4.5.1 in /usr/local/lib/python3.7/dist-packages (from ipywidgets) (5.3.4)\n",
      "Requirement already satisfied: ipython>=4.0.0 in /usr/local/lib/python3.7/dist-packages (from ipywidgets) (7.9.0)\n",
      "Requirement already satisfied: jupyterlab-widgets>=1.0.0 in /usr/local/lib/python3.7/dist-packages (from ipywidgets) (3.0.3)\n",
      "Requirement already satisfied: jupyter-client in /usr/local/lib/python3.7/dist-packages (from ipykernel>=4.5.1->ipywidgets) (6.1.12)\n",
      "Requirement already satisfied: tornado>=4.2 in /usr/local/lib/python3.7/dist-packages (from ipykernel>=4.5.1->ipywidgets) (6.0.4)\n",
      "Requirement already satisfied: decorator in /usr/local/lib/python3.7/dist-packages (from ipython>=4.0.0->ipywidgets) (4.4.2)\n",
      "Requirement already satisfied: pygments in /usr/local/lib/python3.7/dist-packages (from ipython>=4.0.0->ipywidgets) (2.6.1)\n",
      "Collecting jedi>=0.10\n",
      "  Downloading jedi-0.18.2-py2.py3-none-any.whl (1.6 MB)\n",
      "\u001b[K     |████████████████████████████████| 1.6 MB 4.3 MB/s \n",
      "\u001b[?25hRequirement already satisfied: prompt-toolkit<2.1.0,>=2.0.0 in /usr/local/lib/python3.7/dist-packages (from ipython>=4.0.0->ipywidgets) (2.0.10)\n",
      "Requirement already satisfied: backcall in /usr/local/lib/python3.7/dist-packages (from ipython>=4.0.0->ipywidgets) (0.2.0)\n",
      "Requirement already satisfied: pexpect in /usr/local/lib/python3.7/dist-packages (from ipython>=4.0.0->ipywidgets) (4.8.0)\n",
      "Requirement already satisfied: pickleshare in /usr/local/lib/python3.7/dist-packages (from ipython>=4.0.0->ipywidgets) (0.7.5)\n",
      "Requirement already satisfied: setuptools>=18.5 in /usr/local/lib/python3.7/dist-packages (from ipython>=4.0.0->ipywidgets) (57.4.0)\n",
      "Requirement already satisfied: parso<0.9.0,>=0.8.0 in /usr/local/lib/python3.7/dist-packages (from jedi>=0.10->ipython>=4.0.0->ipywidgets) (0.8.3)\n",
      "Requirement already satisfied: wcwidth in /usr/local/lib/python3.7/dist-packages (from prompt-toolkit<2.1.0,>=2.0.0->ipython>=4.0.0->ipywidgets) (0.2.5)\n",
      "Requirement already satisfied: six>=1.9.0 in /usr/local/lib/python3.7/dist-packages (from prompt-toolkit<2.1.0,>=2.0.0->ipython>=4.0.0->ipywidgets) (1.15.0)\n",
      "Requirement already satisfied: notebook>=4.4.1 in /usr/local/lib/python3.7/dist-packages (from widgetsnbextension~=3.6.0->ipywidgets) (5.7.16)\n",
      "Requirement already satisfied: jinja2<=3.0.0 in /usr/local/lib/python3.7/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (2.11.3)\n",
      "Requirement already satisfied: pyzmq>=17 in /usr/local/lib/python3.7/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (23.2.1)\n",
      "Requirement already satisfied: nbformat in /usr/local/lib/python3.7/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (5.7.0)\n",
      "Requirement already satisfied: Send2Trash in /usr/local/lib/python3.7/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (1.8.0)\n",
      "Requirement already satisfied: prometheus-client in /usr/local/lib/python3.7/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.15.0)\n",
      "Requirement already satisfied: jupyter-core>=4.4.0 in /usr/local/lib/python3.7/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (4.11.2)\n",
      "Requirement already satisfied: nbconvert<6.0 in /usr/local/lib/python3.7/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (5.6.1)\n",
      "Requirement already satisfied: terminado>=0.8.1 in /usr/local/lib/python3.7/dist-packages (from notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.13.3)\n",
      "Requirement already satisfied: MarkupSafe>=0.23 in /usr/local/lib/python3.7/dist-packages (from jinja2<=3.0.0->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (2.0.1)\n",
      "Requirement already satisfied: python-dateutil>=2.1 in /usr/local/lib/python3.7/dist-packages (from jupyter-client->ipykernel>=4.5.1->ipywidgets) (2.8.2)\n",
      "Requirement already satisfied: testpath in /usr/local/lib/python3.7/dist-packages (from nbconvert<6.0->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.6.0)\n",
      "Requirement already satisfied: defusedxml in /usr/local/lib/python3.7/dist-packages (from nbconvert<6.0->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.7.1)\n",
      "Requirement already satisfied: bleach in /usr/local/lib/python3.7/dist-packages (from nbconvert<6.0->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (5.0.1)\n",
      "Requirement already satisfied: mistune<2,>=0.8.1 in /usr/local/lib/python3.7/dist-packages (from nbconvert<6.0->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.8.4)\n",
      "Requirement already satisfied: pandocfilters>=1.4.1 in /usr/local/lib/python3.7/dist-packages (from nbconvert<6.0->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (1.5.0)\n",
      "Requirement already satisfied: entrypoints>=0.2.2 in /usr/local/lib/python3.7/dist-packages (from nbconvert<6.0->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.4)\n",
      "Requirement already satisfied: importlib-metadata>=3.6 in /usr/local/lib/python3.7/dist-packages (from nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (4.13.0)\n",
      "Requirement already satisfied: fastjsonschema in /usr/local/lib/python3.7/dist-packages (from nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (2.16.2)\n",
      "Requirement already satisfied: jsonschema>=2.6 in /usr/local/lib/python3.7/dist-packages (from nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (4.3.3)\n",
      "Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.7/dist-packages (from importlib-metadata>=3.6->nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (3.10.0)\n",
      "Requirement already satisfied: typing-extensions>=3.6.4 in /usr/local/lib/python3.7/dist-packages (from importlib-metadata>=3.6->nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (4.1.1)\n",
      "Requirement already satisfied: attrs>=17.4.0 in /usr/local/lib/python3.7/dist-packages (from jsonschema>=2.6->nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (22.1.0)\n",
      "Requirement already satisfied: importlib-resources>=1.4.0 in /usr/local/lib/python3.7/dist-packages (from jsonschema>=2.6->nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (5.10.0)\n",
      "Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in /usr/local/lib/python3.7/dist-packages (from jsonschema>=2.6->nbformat->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.19.2)\n",
      "Requirement already satisfied: ptyprocess in /usr/local/lib/python3.7/dist-packages (from terminado>=0.8.1->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.7.0)\n",
      "Requirement already satisfied: webencodings in /usr/local/lib/python3.7/dist-packages (from bleach->nbconvert<6.0->notebook>=4.4.1->widgetsnbextension~=3.6.0->ipywidgets) (0.5.1)\n",
      "Installing collected packages: jedi\n",
      "Successfully installed jedi-0.18.2\n",
      "Looking in indexes: https://pypi.org/simple, https://us-python.pkg.dev/colab-wheels/public/simple/\n",
      "Collecting git+https://****@github.com/SKTBrain/KoBERT.git@master\n",
      "  Cloning https://****@github.com/SKTBrain/KoBERT.git (to revision master) to /tmp/pip-req-build-tx7llcuj\n",
      "  Running command git clone -q 'https://****@github.com/SKTBrain/KoBERT.git' /tmp/pip-req-build-tx7llcuj\n",
      "Collecting boto3<=1.15.18\n",
      "  Downloading boto3-1.15.18-py2.py3-none-any.whl (129 kB)\n",
      "\u001b[K     |████████████████████████████████| 129 kB 4.0 MB/s \n",
      "\u001b[?25hCollecting gluonnlp<=0.10.0,>=0.6.0\n",
      "  Downloading gluonnlp-0.10.0.tar.gz (344 kB)\n",
      "\u001b[K     |████████████████████████████████| 344 kB 25.7 MB/s \n",
      "\u001b[?25hCollecting mxnet<=1.7.0.post2,>=1.4.0\n",
      "  Downloading mxnet-1.7.0.post2-py2.py3-none-manylinux2014_x86_64.whl (54.7 MB)\n",
      "\u001b[K     |████████████████████████████████| 54.7 MB 88.5 MB/s \n",
      "\u001b[?25hCollecting onnxruntime<=1.8.0,==1.8.0\n",
      "  Downloading onnxruntime-1.8.0-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (4.5 MB)\n",
      "\u001b[K     |████████████████████████████████| 4.5 MB 84.8 MB/s \n",
      "\u001b[?25hCollecting sentencepiece<=0.1.96,>=0.1.6\n",
      "  Downloading sentencepiece-0.1.96-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (1.2 MB)\n",
      "\u001b[K     |████████████████████████████████| 1.2 MB 17.0 MB/s \n",
      "\u001b[?25hCollecting torch<=1.10.1,>=1.7.0\n",
      "  Downloading torch-1.10.1-cp37-cp37m-manylinux1_x86_64.whl (881.9 MB)\n",
      "\u001b[K     |██████████████████████████████▎ | 834.1 MB 1.1 MB/s eta 0:00:42tcmalloc: large alloc 1147494400 bytes == 0x2e56000 @  0x7f70b66f0615 0x58ead6 0x4f355e 0x4d222f 0x51041f 0x5b4ee6 0x58ff2e 0x510325 0x5b4ee6 0x58ff2e 0x50d482 0x4d00fb 0x50cb8d 0x4d00fb 0x50cb8d 0x4d00fb 0x50cb8d 0x4bac0a 0x538a76 0x590ae5 0x510280 0x5b4ee6 0x58ff2e 0x50d482 0x5b4ee6 0x58ff2e 0x50c4fc 0x58fd37 0x50ca37 0x5b4ee6 0x58ff2e\n",
      "\u001b[K     |████████████████████████████████| 881.9 MB 18 kB/s \n",
      "\u001b[?25hCollecting transformers<=4.8.1,>=4.8.1\n",
      "  Downloading transformers-4.8.1-py3-none-any.whl (2.5 MB)\n",
      "\u001b[K     |████████████████████████████████| 2.5 MB 69.0 MB/s \n",
      "\u001b[?25hRequirement already satisfied: protobuf in /usr/local/lib/python3.7/dist-packages (from onnxruntime<=1.8.0,==1.8.0->kobert==0.2.3) (3.19.6)\n",
      "Requirement already satisfied: flatbuffers in /usr/local/lib/python3.7/dist-packages (from onnxruntime<=1.8.0,==1.8.0->kobert==0.2.3) (1.12)\n",
      "Requirement already satisfied: numpy>=1.16.6 in /usr/local/lib/python3.7/dist-packages (from onnxruntime<=1.8.0,==1.8.0->kobert==0.2.3) (1.21.6)\n",
      "Collecting botocore<1.19.0,>=1.18.18\n",
      "  Downloading botocore-1.18.18-py2.py3-none-any.whl (6.7 MB)\n",
      "\u001b[K     |████████████████████████████████| 6.7 MB 45.2 MB/s \n",
      "\u001b[?25hCollecting s3transfer<0.4.0,>=0.3.0\n",
      "  Downloading s3transfer-0.3.7-py2.py3-none-any.whl (73 kB)\n",
      "\u001b[K     |████████████████████████████████| 73 kB 2.2 MB/s \n",
      "\u001b[?25hCollecting jmespath<1.0.0,>=0.7.1\n",
      "  Downloading jmespath-0.10.0-py2.py3-none-any.whl (24 kB)\n",
      "Requirement already satisfied: urllib3<1.26,>=1.20 in /usr/local/lib/python3.7/dist-packages (from botocore<1.19.0,>=1.18.18->boto3<=1.15.18->kobert==0.2.3) (1.24.3)\n",
      "Requirement already satisfied: python-dateutil<3.0.0,>=2.1 in /usr/local/lib/python3.7/dist-packages (from botocore<1.19.0,>=1.18.18->boto3<=1.15.18->kobert==0.2.3) (2.8.2)\n",
      "Requirement already satisfied: cython in /usr/local/lib/python3.7/dist-packages (from gluonnlp<=0.10.0,>=0.6.0->kobert==0.2.3) (0.29.32)\n",
      "Requirement already satisfied: packaging in /usr/local/lib/python3.7/dist-packages (from gluonnlp<=0.10.0,>=0.6.0->kobert==0.2.3) (21.3)\n",
      "Requirement already satisfied: requests<3,>=2.20.0 in /usr/local/lib/python3.7/dist-packages (from mxnet<=1.7.0.post2,>=1.4.0->kobert==0.2.3) (2.23.0)\n",
      "Collecting graphviz<0.9.0,>=0.8.1\n",
      "  Downloading graphviz-0.8.4-py2.py3-none-any.whl (16 kB)\n",
      "Requirement already satisfied: six>=1.5 in /usr/local/lib/python3.7/dist-packages (from python-dateutil<3.0.0,>=2.1->botocore<1.19.0,>=1.18.18->boto3<=1.15.18->kobert==0.2.3) (1.15.0)\n",
      "Requirement already satisfied: idna<3,>=2.5 in /usr/local/lib/python3.7/dist-packages (from requests<3,>=2.20.0->mxnet<=1.7.0.post2,>=1.4.0->kobert==0.2.3) (2.10)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in /usr/local/lib/python3.7/dist-packages (from requests<3,>=2.20.0->mxnet<=1.7.0.post2,>=1.4.0->kobert==0.2.3) (2022.9.24)\n",
      "Requirement already satisfied: chardet<4,>=3.0.2 in /usr/local/lib/python3.7/dist-packages (from requests<3,>=2.20.0->mxnet<=1.7.0.post2,>=1.4.0->kobert==0.2.3) (3.0.4)\n",
      "Requirement already satisfied: typing-extensions in /usr/local/lib/python3.7/dist-packages (from torch<=1.10.1,>=1.7.0->kobert==0.2.3) (4.1.1)\n",
      "Collecting huggingface-hub==0.0.12\n",
      "  Downloading huggingface_hub-0.0.12-py3-none-any.whl (37 kB)\n",
      "Requirement already satisfied: regex!=2019.12.17 in /usr/local/lib/python3.7/dist-packages (from transformers<=4.8.1,>=4.8.1->kobert==0.2.3) (2022.6.2)\n",
      "Requirement already satisfied: importlib-metadata in /usr/local/lib/python3.7/dist-packages (from transformers<=4.8.1,>=4.8.1->kobert==0.2.3) (4.13.0)\n",
      "Requirement already satisfied: tqdm>=4.27 in /usr/local/lib/python3.7/dist-packages (from transformers<=4.8.1,>=4.8.1->kobert==0.2.3) (4.64.1)\n",
      "Requirement already satisfied: filelock in /usr/local/lib/python3.7/dist-packages (from transformers<=4.8.1,>=4.8.1->kobert==0.2.3) (3.8.0)\n",
      "Collecting tokenizers<0.11,>=0.10.1\n",
      "  Downloading tokenizers-0.10.3-cp37-cp37m-manylinux_2_5_x86_64.manylinux1_x86_64.manylinux_2_12_x86_64.manylinux2010_x86_64.whl (3.3 MB)\n",
      "\u001b[K     |████████████████████████████████| 3.3 MB 46.1 MB/s \n",
      "\u001b[?25hCollecting sacremoses\n",
      "  Downloading sacremoses-0.0.53.tar.gz (880 kB)\n",
      "\u001b[K     |████████████████████████████████| 880 kB 49.5 MB/s \n",
      "\u001b[?25hRequirement already satisfied: pyyaml in /usr/local/lib/python3.7/dist-packages (from transformers<=4.8.1,>=4.8.1->kobert==0.2.3) (6.0)\n",
      "Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in /usr/local/lib/python3.7/dist-packages (from packaging->gluonnlp<=0.10.0,>=0.6.0->kobert==0.2.3) (3.0.9)\n",
      "Requirement already satisfied: zipp>=0.5 in /usr/local/lib/python3.7/dist-packages (from importlib-metadata->transformers<=4.8.1,>=4.8.1->kobert==0.2.3) (3.10.0)\n",
      "Requirement already satisfied: click in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers<=4.8.1,>=4.8.1->kobert==0.2.3) (7.1.2)\n",
      "Requirement already satisfied: joblib in /usr/local/lib/python3.7/dist-packages (from sacremoses->transformers<=4.8.1,>=4.8.1->kobert==0.2.3) (1.2.0)\n",
      "Building wheels for collected packages: kobert, gluonnlp, sacremoses\n",
      "  Building wheel for kobert (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
      "  Created wheel for kobert: filename=kobert-0.2.3-py3-none-any.whl size=15708 sha256=e9b2341351aaf6ea9b6dd636311005733263d161a21bfbf9d5ba52f2a7bcc160\n",
      "  Stored in directory: /tmp/pip-ephem-wheel-cache-61huuvx3/wheels/d3/68/ca/334747dfb038313b49cf71f84832a33372f3470d9ddfd051c0\n",
      "  Building wheel for gluonnlp (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
      "  Created wheel for gluonnlp: filename=gluonnlp-0.10.0-cp37-cp37m-linux_x86_64.whl size=595739 sha256=e5a931b5c6c87d35e2a6148f19455c0f1255b67fbe781b37870ffab026d9cc4b\n",
      "  Stored in directory: /root/.cache/pip/wheels/be/b4/06/7f3fdfaf707e6b5e98b79c041e023acffbe395d78a527eae00\n",
      "  Building wheel for sacremoses (setup.py) ... \u001b[?25l\u001b[?25hdone\n",
      "  Created wheel for sacremoses: filename=sacremoses-0.0.53-py3-none-any.whl size=895260 sha256=5342a7e7e475f8e5ac2f19d6bcd43881a97d8056b82f5c4946ce4dbd2a5f9881\n",
      "  Stored in directory: /root/.cache/pip/wheels/87/39/dd/a83eeef36d0bf98e7a4d1933a4ad2d660295a40613079bafc9\n",
      "Successfully built kobert gluonnlp sacremoses\n",
      "Installing collected packages: jmespath, botocore, tokenizers, sacremoses, s3transfer, huggingface-hub, graphviz, transformers, torch, sentencepiece, onnxruntime, mxnet, gluonnlp, boto3, kobert\n",
      "  Attempting uninstall: graphviz\n",
      "    Found existing installation: graphviz 0.10.1\n",
      "    Uninstalling graphviz-0.10.1:\n",
      "      Successfully uninstalled graphviz-0.10.1\n",
      "  Attempting uninstall: torch\n",
      "    Found existing installation: torch 1.12.1+cu113\n",
      "    Uninstalling torch-1.12.1+cu113:\n",
      "      Successfully uninstalled torch-1.12.1+cu113\n",
      "\u001b[31mERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.\n",
      "torchvision 0.13.1+cu113 requires torch==1.12.1, but you have torch 1.10.1 which is incompatible.\n",
      "torchtext 0.13.1 requires torch==1.12.1, but you have torch 1.10.1 which is incompatible.\n",
      "torchaudio 0.12.1+cu113 requires torch==1.12.1, but you have torch 1.10.1 which is incompatible.\u001b[0m\n",
      "Successfully installed boto3-1.15.18 botocore-1.18.18 gluonnlp-0.10.0 graphviz-0.8.4 huggingface-hub-0.0.12 jmespath-0.10.0 kobert-0.2.3 mxnet-1.7.0.post2 onnxruntime-1.8.0 s3transfer-0.3.7 sacremoses-0.0.53 sentencepiece-0.1.96 tokenizers-0.10.3 torch-1.10.1 transformers-4.8.1\n"
     ]
    }
   ],
   "source": [
    "!pip install ipywidgets  # for vscode\n",
    "!pip install git+https://git@github.com/SKTBrain/KoBERT.git@master"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {
    "executionInfo": {
     "elapsed": 5356,
     "status": "ok",
     "timestamp": 1669602062830,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "5mTNl7BKT2Fx"
   },
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "from tqdm.notebook import tqdm\n",
    "\n",
    "from mxnet.gluon import nn\n",
    "from mxnet import gluon\n",
    "import mxnet as mx\n",
    "import gluonnlp as nlp\n",
    "\n",
    "from tensorflow.keras.layers import Embedding, Dense, LSTM\n",
    "from tensorflow.keras.models import Sequential\n",
    "from tensorflow.keras.models import load_model\n",
    "from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint\n",
    "\n",
    "from kobert import get_mxnet_kobert_model\n",
    "from kobert import get_tokenizer"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "Cc-zco-ST2F_"
   },
   "source": [
    "### Loading KoBERT"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {
    "executionInfo": {
     "elapsed": 6,
     "status": "ok",
     "timestamp": 1669602062830,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "XSKQJoH8tSOD"
   },
   "outputs": [],
   "source": [
    "# CPU\n",
    "ctx = mx.cpu()\n",
    "\n",
    "# GPU\n",
    "# ctx = mx.gpu()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 7239,
     "status": "ok",
     "timestamp": 1669602070064,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "wI841Zb38XOn",
    "outputId": "51709b76-104d-4f30-82cb-d72a8ce6d6eb"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "/content/.cache/mxnet_kobert_45b6957552.params[██████████████████████████████████████████████████]\n",
      "/content/.cache/kobert_news_wiki_ko_cased-1087f8699e.spiece[██████████████████████████████████████████████████]\n"
     ]
    }
   ],
   "source": [
    "bert_base, vocab = get_mxnet_kobert_model(use_decoder=False, use_classifier=False, ctx=ctx, cachedir=\".cache\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 12,
     "status": "ok",
     "timestamp": 1669602070064,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "NijpWe8J8isZ",
    "outputId": "45b28959-6e7e-4a32-e4a4-dbde0cc84cd7"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "using cached model. /content/.cache/kobert_news_wiki_ko_cased-1087f8699e.spiece\n"
     ]
    }
   ],
   "source": [
    "tokenizer = get_tokenizer()\n",
    "tok = nlp.data.BERTSPTokenizer(tokenizer, vocab, lower=False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 10,
     "status": "ok",
     "timestamp": 1669602070064,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "i69AUj9gT2Gk",
    "outputId": "3f8344dd-837f-4e58-bde9-80829beacd11"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "[(array([   2, 1370, 2362, 5330, 3322,    3, 1316, 6607, 7028,    3],\n",
       "        dtype=int32),\n",
       "  array(10, dtype=int32),\n",
       "  array([0, 0, 0, 0, 0, 0, 1, 1, 1, 1], dtype=int32))]"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ds = gluon.data.SimpleDataset([['나 보기가 역겨워', '김소월']])\n",
    "trans = nlp.data.BERTSentenceTransform(tok, max_seq_length=10)\n",
    "\n",
    "list(ds.transform(trans))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "sSg-Mck9tSOF"
   },
   "source": [
    "### Loading Data"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "4qy9g_UMVtdj"
   },
   "outputs": [],
   "source": [
    "# !wget -O .cache/ratings_train.txt http://skt-lsl-nlp-model.s3.amazonaws.com/KoBERT/datasets/nsmc/ratings_train.txt\n",
    "# !wget -O .cache/ratings_test.txt http://skt-lsl-nlp-model.s3.amazonaws.com/KoBERT/datasets/nsmc/ratings_test.txt"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 19466,
     "status": "ok",
     "timestamp": 1669602247940,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "N02vIXFj58rG",
    "outputId": "73a5f6e1-af8a-41a3-ed2b-0898178ed0e9"
   },
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Mounted at /content/drive\n"
     ]
    }
   ],
   "source": [
    "from google.colab import drive\n",
    "drive.mount('/content/drive')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {
    "executionInfo": {
     "elapsed": 1741,
     "status": "ok",
     "timestamp": 1669602257036,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "4LfCTweqT2Gt"
   },
   "outputs": [],
   "source": [
    "dataset_train = nlp.data.TSVDataset(\"/content/drive/MyDrive/Colab Notebooks/train_tobert.tsv\", field_indices=[0,1], num_discard_samples=1)\n",
    "dataset_test = nlp.data.TSVDataset(\"/content/drive/MyDrive/Colab Notebooks/test_tobert.tsv\", field_indices=[0,1], num_discard_samples=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 5,
     "status": "ok",
     "timestamp": 1669602257036,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "8NbQ1FKAu4U2",
    "outputId": "39c6324e-2b95-43d3-8dc4-957ba4dd9c7f"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<gluonnlp.data.dataset.TSVDataset at 0x7f75de0a9850>"
      ]
     },
     "execution_count": 11,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dataset_train"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 3,
     "status": "ok",
     "timestamp": 1669602257036,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "U_oZbyRIu5kI",
    "outputId": "c95bacb4-f453-46e2-88d4-24b80c113e59"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<gluonnlp.data.dataset.TSVDataset at 0x7f7646869790>"
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "dataset_test"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {
    "executionInfo": {
     "elapsed": 457,
     "status": "ok",
     "timestamp": 1669602275887,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "pt0raV8uT2G2"
   },
   "outputs": [],
   "source": [
    "class BERTDataset(mx.gluon.data.Dataset):\n",
    "    def __init__(self, dataset, sent_idx, label_idx, bert_tokenizer, max_len,\n",
    "                 pad, pair):\n",
    "        transform = nlp.data.BERTSentenceTransform(\n",
    "            bert_tokenizer, max_seq_length=max_len, pad=pad, pair=pair)\n",
    "        sent_dataset = gluon.data.SimpleDataset([[\n",
    "            i[sent_idx],\n",
    "        ] for i in dataset])\n",
    "        self.sentences = sent_dataset.transform(transform)\n",
    "        self.labels = gluon.data.SimpleDataset(\n",
    "            [np.array(np.int32(i[label_idx])) for i in dataset])\n",
    "\n",
    "    def __getitem__(self, i):\n",
    "        return (self.sentences[i] + (self.labels[i], ))\n",
    "\n",
    "    def __len__(self):\n",
    "        return (len(self.labels))\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {
    "executionInfo": {
     "elapsed": 3,
     "status": "ok",
     "timestamp": 1669602278808,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "vtk-8pQST2G9"
   },
   "outputs": [],
   "source": [
    "max_len = 128"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {
    "id": "D8rB_sGV7JQU"
   },
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {
    "executionInfo": {
     "elapsed": 450,
     "status": "ok",
     "timestamp": 1669602292930,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "_K_BLZP_T2HF"
   },
   "outputs": [],
   "source": [
    "data_train = BERTDataset(dataset_train, 0, 1, tok, max_len, True, False)\n",
    "data_test = BERTDataset(dataset_test, 0, 1, tok, max_len, True, False)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 3,
     "status": "ok",
     "timestamp": 1669602294982,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "-K-AaSN1uxef",
    "outputId": "a091e0b5-0aa5-4fb3-8de9-c3d160646f78"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "<__main__.BERTDataset at 0x7f75de180450>"
      ]
     },
     "execution_count": 16,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "data_train"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "rhaw0H4ST2HM"
   },
   "outputs": [],
   "source": [
    "class BERTClassifier(nn.Block):\n",
    "    def __init__(self,\n",
    "                 bert,\n",
    "                 num_classes=2,\n",
    "                 dropout=None,\n",
    "                 prefix=None,\n",
    "                 params=None):\n",
    "        super(BERTClassifier, self).__init__(prefix=prefix, params=params)\n",
    "        self.bert = bert\n",
    "        with self.name_scope():\n",
    "            self.classifier = nn.HybridSequential(prefix=prefix)\n",
    "            if dropout:\n",
    "                self.classifier.add(nn.Dropout(rate=dropout))\n",
    "            self.classifier.add(nn.Dense(units=num_classes))\n",
    "\n",
    "    def forward(self, inputs, token_types, valid_length=None):\n",
    "        _, pooler = self.bert(inputs, token_types, valid_length)\n",
    "        return self.classifier(pooler)\n",
    "                                           "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "Y00BOPwST2HX"
   },
   "outputs": [],
   "source": [
    "model = BERTClassifier(bert_base, num_classes=2, dropout=0.1)\n",
    "# 분류 레이어만 초기화 한다. \n",
    "model.classifier.initialize(init=mx.init.Normal(0.02), ctx=ctx)\n",
    "model.hybridize()\n",
    "\n",
    "# softmax cross entropy loss for classification\n",
    "loss_function = gluon.loss.SoftmaxCELoss()\n",
    "\n",
    "metric = mx.metric.Accuracy()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "A2dLhnHkT2Hf"
   },
   "outputs": [],
   "source": [
    "batch_size = 32\n",
    "lr = 5e-5\n",
    "\n",
    "train_dataloader = mx.gluon.data.DataLoader(data_train, batch_size=batch_size, num_workers=5)\n",
    "test_dataloader = mx.gluon.data.DataLoader(data_test, batch_size=int(batch_size/2), num_workers=5)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "ESo76UH-T2Hr"
   },
   "outputs": [],
   "source": [
    "trainer = gluon.Trainer(model.collect_params(), 'bertadam',\n",
    "                        {'learning_rate': lr, 'epsilon': 1e-9, 'wd':0.01})\n",
    "\n",
    "log_interval = 4\n",
    "num_epochs = 5"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "wspMBDOAT2H0"
   },
   "outputs": [],
   "source": [
    "# LayerNorm과 Bias에는 Weight Decay를 적용하지 않는다. \n",
    "for _, v in model.collect_params('.*beta|.*gamma|.*bias').items():\n",
    "    v.wd_mult = 0.0\n",
    "params = [\n",
    "    p for p in model.collect_params().values() if p.grad_req != 'null'\n",
    "]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "NCR6AMKHT2H6"
   },
   "outputs": [],
   "source": [
    "def evaluate_accuracy(model, data_iter, ctx=ctx):\n",
    "    acc = mx.metric.Accuracy()\n",
    "    i = 0\n",
    "    for i, (t,v,s, label) in enumerate(data_iter):\n",
    "        token_ids = t.as_in_context(ctx)\n",
    "        valid_length = v.as_in_context(ctx)\n",
    "        segment_ids = s.as_in_context(ctx)\n",
    "        label = label.as_in_context(ctx)\n",
    "        output = model(token_ids, segment_ids, valid_length.astype('float32'))\n",
    "        acc.update(preds=output, labels=label)\n",
    "        if i > 1000:\n",
    "            break\n",
    "        i += 1\n",
    "    return(acc.get()[1])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "SkcW6GyeT2IA"
   },
   "outputs": [],
   "source": [
    "#learning rate warmup을 위한 준비 \n",
    "accumulate = 4\n",
    "step_size = batch_size * accumulate if accumulate else batch_size\n",
    "num_train_examples = len(data_train)\n",
    "num_train_steps = int(num_train_examples / step_size * num_epochs)\n",
    "warmup_ratio = 0.1\n",
    "num_warmup_steps = int(num_train_steps * warmup_ratio)\n",
    "step_num = 0\n",
    "all_model_params = model.collect_params()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "Yf_rpZTq6uES"
   },
   "outputs": [],
   "source": [
    "# Set grad_req if gradient accumulation is required\n",
    "if accumulate and accumulate > 1:\n",
    "    for p in params:\n",
    "        p.grad_req = 'add'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 722,
     "referenced_widgets": [
      "ea05be94e56245c19b4258cda60b7958",
      "3e103eead4444d1ca2a24dc1ee1ae376",
      "b7f345c0f18f45b39262fe0b22caa049",
      "d2b7270df9f54c4ea4236d294588f9dd",
      "6862dd166f6547abaf892ed8e493a173",
      "ab81519ca4554b0ba4995d6d2e441d3d",
      "ae2e750e956d499a88a15f8b1366a978",
      "731c6712f31240b2a65825d29e5fbff2",
      "87a608c2b3de4da79611b7f9577ba668",
      "ee1a4fdd7fb24db890c2405839862f4e",
      "07388772a1c847029559cedd658d603c",
      "bdda8d265e8d49feac2e601778fe763f",
      "5bd53c3e256d4206afae214cb6d65aaf",
      "b081230afd844298aca9294083f766c8",
      "3d9aef0573fe42bca049d38b04a87353",
      "88eb0276388548d58563f3eaa76cc5bd",
      "965cd099b07b4f2db46822204e7e694a",
      "bf3f3c9eefa348d4a5cfeffadac61678",
      "5fcb0eddd07b49539cb5debd375adc23",
      "4b6da813eddc42b199208b8b60aa1a26",
      "bfba2dc1a15148cb832c54436962244a",
      "1ce851d66c8340a1bb0ce4986c07681d",
      "4f91a2ad8c1d4ca18a5a3fa7cf817787",
      "bc19a9dc4c5448f4ba15ffb41e8b9f20",
      "d05c0f09f5824e1ebeaf701e534ceb33",
      "e2f6dea00a9c4dfa8665fc3215abd94f",
      "544a853e64c44059ac2f4dd30af3b765",
      "0474443973534cdda70e4c526cd2bb0a",
      "04cf5fad0f4e46ea877a537a72cc0f39",
      "3cc6f20fe3a64c0c8587823e7e38fc9a",
      "21a3404fc8e6470fb3dce891ba457766",
      "50af9db53f7a46cfaf0deae79129059b",
      "1fc6409616bf4d97afaa0995f283005e",
      "6080ed35204e458aa71a83c52afa5924",
      "4b37958a6a1544ff8443b5b8dfb39d4c",
      "98356958fb824f94adf1e2e14fb56999",
      "507743910e72424bac4c898a1d77b6f9",
      "a6d78954f73e4e02b5d183b4de9dcf18",
      "38a7b8d290e247a19a175e4fce7a82ed",
      "c3c41bb1a5f446a4862641c6ba578bbd",
      "613fce564ff54846b1c076764b5c100a",
      "a7d030b8d41e458d837185aae29e1f79",
      "bf9b13048c164079a15f685c67ae28fb",
      "d79303dd7e7c4559af16ace6379b7a3e",
      "919d1452812140899bb02a806b505c4a",
      "b1a2a0da6ebd47199bc980a63169df5f",
      "a481898e917e4e519cd1ae1b5c0bd146",
      "1addd4fca3714bbea1e19ac0d162712e",
      "8d85ec6ff654460f95aa868fbb5e9f59",
      "56ab5d81c5734428b41fba3b04f79c51",
      "39eaa4ae4c654fd99d83533ea0ab0692",
      "bfa5bbb2d8864db080f06a83b12ae83f",
      "03808a5c1497414dbabf6ddda06a5743",
      "f79cc7de540f4b86bd92a1d0f8da22a7",
      "791812521f5a47509838a1a37d4d3f07"
     ]
    },
    "executionInfo": {
     "elapsed": 75061441,
     "status": "ok",
     "timestamp": 1669256499150,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "0mJ3Pw_VT2IH",
    "outputId": "b7d3a0d2-4214-477f-e46f-e1e897bbe0bd"
   },
   "outputs": [
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "ea05be94e56245c19b4258cda60b7958",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "  0%|          | 0/281 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[Epoch 1 Batch 50/281] loss=8.2978, lr=0.0000171429, acc=0.582\n",
      "[Epoch 1 Batch 100/281] loss=8.4093, lr=0.0000342857, acc=0.603\n",
      "[Epoch 1 Batch 150/281] loss=6.7608, lr=0.0000496835, acc=0.650\n",
      "[Epoch 1 Batch 200/281] loss=8.7502, lr=0.0000477848, acc=0.619\n",
      "[Epoch 1 Batch 250/281] loss=8.7591, lr=0.0000457278, acc=0.597\n",
      "Test Acc : 0.5065065065065065\n"
     ]
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "bdda8d265e8d49feac2e601778fe763f",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "  0%|          | 0/281 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[Epoch 2 Batch 50/281] loss=8.5844, lr=0.0000425633, acc=0.537\n",
      "[Epoch 2 Batch 100/281] loss=7.2016, lr=0.0000406646, acc=0.640\n",
      "[Epoch 2 Batch 150/281] loss=8.2328, lr=0.0000386076, acc=0.664\n",
      "[Epoch 2 Batch 200/281] loss=6.8761, lr=0.0000367089, acc=0.689\n",
      "[Epoch 2 Batch 250/281] loss=6.9325, lr=0.0000346519, acc=0.702\n",
      "Test Acc : 0.7677677677677678\n"
     ]
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "4f91a2ad8c1d4ca18a5a3fa7cf817787",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "  0%|          | 0/281 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[Epoch 3 Batch 50/281] loss=6.5199, lr=0.0000314873, acc=0.787\n",
      "[Epoch 3 Batch 100/281] loss=5.8725, lr=0.0000295886, acc=0.799\n",
      "[Epoch 3 Batch 150/281] loss=5.9629, lr=0.0000275316, acc=0.801\n",
      "[Epoch 3 Batch 200/281] loss=5.8930, lr=0.0000256329, acc=0.805\n",
      "[Epoch 3 Batch 250/281] loss=6.2302, lr=0.0000235759, acc=0.802\n",
      "Test Acc : 0.7797797797797797\n"
     ]
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "6080ed35204e458aa71a83c52afa5924",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "  0%|          | 0/281 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[Epoch 4 Batch 50/281] loss=5.1969, lr=0.0000204114, acc=0.827\n",
      "[Epoch 4 Batch 100/281] loss=4.9010, lr=0.0000185127, acc=0.834\n",
      "[Epoch 4 Batch 150/281] loss=4.4682, lr=0.0000164557, acc=0.842\n",
      "[Epoch 4 Batch 200/281] loss=4.8611, lr=0.0000145570, acc=0.841\n",
      "[Epoch 4 Batch 250/281] loss=4.9694, lr=0.0000125000, acc=0.841\n",
      "Test Acc : 0.8048048048048048\n"
     ]
    },
    {
     "data": {
      "application/vnd.jupyter.widget-view+json": {
       "model_id": "919d1452812140899bb02a806b505c4a",
       "version_major": 2,
       "version_minor": 0
      },
      "text/plain": [
       "  0%|          | 0/281 [00:00<?, ?it/s]"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "[Epoch 5 Batch 50/281] loss=4.4577, lr=0.0000093354, acc=0.855\n",
      "[Epoch 5 Batch 100/281] loss=4.3008, lr=0.0000074367, acc=0.860\n",
      "[Epoch 5 Batch 150/281] loss=3.9578, lr=0.0000053797, acc=0.866\n",
      "[Epoch 5 Batch 200/281] loss=4.5105, lr=0.0000034810, acc=0.862\n",
      "[Epoch 5 Batch 250/281] loss=4.6422, lr=0.0000014241, acc=0.860\n",
      "Test Acc : 0.8138138138138138\n"
     ]
    }
   ],
   "source": [
    "for epoch_id in range(num_epochs):\n",
    "    metric.reset()\n",
    "    step_loss = 0\n",
    "    for batch_id, (token_ids, valid_length, segment_ids, label) in tqdm(enumerate(train_dataloader), total=len(train_dataloader)):\n",
    "        if step_num < num_warmup_steps:\n",
    "            new_lr = lr * step_num / num_warmup_steps\n",
    "        else:\n",
    "            non_warmup_steps = step_num - num_warmup_steps\n",
    "            offset = non_warmup_steps / (num_train_steps - num_warmup_steps)\n",
    "            new_lr = lr - offset * lr\n",
    "        trainer.set_learning_rate(new_lr)\n",
    "        with mx.autograd.record():\n",
    "            # load data to GPU\n",
    "            token_ids = token_ids.as_in_context(ctx)\n",
    "            valid_length = valid_length.as_in_context(ctx)\n",
    "            segment_ids = segment_ids.as_in_context(ctx)\n",
    "            label = label.as_in_context(ctx)\n",
    "\n",
    "            # forward computation\n",
    "            out = model(token_ids, segment_ids, valid_length.astype('float32'))\n",
    "            ls = loss_function(out, label).mean()\n",
    "\n",
    "        # backward computation\n",
    "        ls.backward()\n",
    "        if not accumulate or (batch_id + 1) % accumulate == 0:\n",
    "          trainer.allreduce_grads()\n",
    "          nlp.utils.clip_grad_global_norm(params, 1)\n",
    "          trainer.update(accumulate if accumulate else 1)\n",
    "          step_num += 1\n",
    "          if accumulate and accumulate > 1:\n",
    "              # set grad to zero for gradient accumulation\n",
    "              all_model_params.zero_grad()\n",
    "\n",
    "        step_loss += ls.asscalar()\n",
    "        metric.update([label], [out])\n",
    "        if (batch_id + 1) % (50) == 0:\n",
    "            print('[Epoch {} Batch {}/{}] loss={:.4f}, lr={:.10f}, acc={:.3f}'\n",
    "                         .format(epoch_id + 1, batch_id + 1, len(train_dataloader),\n",
    "                                 step_loss / log_interval,\n",
    "                                 trainer.learning_rate, metric.get()[1]))\n",
    "            step_loss = 0\n",
    "    test_acc = evaluate_accuracy(model, test_dataloader, ctx)\n",
    "    print('Test Acc : {}'.format(test_acc))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 333,
     "status": "ok",
     "timestamp": 1669260820974,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "4_jVU5B4815K",
    "outputId": "c89bcc9b-e4cf-4f75-fb32-674ab171207c"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "\n",
       "[[-1.1306487   0.8814099 ]\n",
       " [ 1.6422635  -1.2875552 ]\n",
       " [-1.1247705   1.0251942 ]\n",
       " [ 0.861518   -0.46553835]\n",
       " [ 1.591802   -1.2039665 ]\n",
       " [-1.3060573   1.1222783 ]\n",
       " [-0.60148484  0.29791567]\n",
       " [ 1.6769968  -1.1360091 ]\n",
       " [-1.3226825   1.1892363 ]\n",
       " [ 0.33767682  0.03917556]\n",
       " [-1.3854505   0.70540875]\n",
       " [ 1.6266195  -1.3273641 ]\n",
       " [-1.2182685   0.9169094 ]\n",
       " [-0.7477427   0.37561443]\n",
       " [-1.3368196   1.2708374 ]\n",
       " [-1.2155222   0.9562531 ]\n",
       " [ 1.6107718  -1.3316886 ]\n",
       " [-1.2951361   1.0058514 ]\n",
       " [-0.4651372   0.42999256]\n",
       " [ 1.5370193  -1.3280644 ]\n",
       " [ 0.94874007 -0.61277103]\n",
       " [-1.2278335   1.0333505 ]\n",
       " [-1.1383847   0.9914103 ]\n",
       " [ 1.6636866  -1.3745096 ]\n",
       " [-1.182825    0.8484537 ]\n",
       " [-1.3594638   1.1982249 ]\n",
       " [-1.1256633   1.108291  ]\n",
       " [-1.3109725   0.9071002 ]]\n",
       "<NDArray 28x2 @cpu(0)>"
      ]
     },
     "execution_count": 25,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "out"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "executionInfo": {
     "elapsed": 9,
     "status": "ok",
     "timestamp": 1669260832009,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "eNASCarZsr1H",
    "outputId": "873ca6ca-4bd0-4a55-8334-ce7f9a83de4a"
   },
   "outputs": [
    {
     "data": {
      "text/plain": [
       "BERTClassifier(\n",
       "  (bert): BERTModel(\n",
       "    (encoder): BERTEncoder(\n",
       "      (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "      (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "      (transformer_cells): HybridSequential(\n",
       "        (0): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (1): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (2): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (3): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (4): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (5): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (6): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (7): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (8): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (9): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (10): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "        (11): BERTEncoderCell(\n",
       "          (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          (attention_cell): DotProductSelfAttentionCell(\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "          )\n",
       "          (proj): Dense(768 -> 768, linear)\n",
       "          (ffn): PositionwiseFFN(\n",
       "            (ffn_1): Dense(768 -> 3072, linear)\n",
       "            (activation): GELU()\n",
       "            (ffn_2): Dense(3072 -> 768, linear)\n",
       "            (dropout_layer): Dropout(p = 0.1, axes=())\n",
       "            (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "          )\n",
       "          (layer_norm): LayerNorm(eps=1e-12, axis=-1, center=True, scale=True, in_channels=768)\n",
       "        )\n",
       "      )\n",
       "    )\n",
       "    (word_embed): HybridSequential(\n",
       "      (0): Embedding(8002 -> 768, float32)\n",
       "    )\n",
       "    (token_type_embed): HybridSequential(\n",
       "      (0): Embedding(2 -> 768, float32)\n",
       "    )\n",
       "    (pooler): Dense(768 -> 768, Activation(tanh))\n",
       "  )\n",
       "  (classifier): HybridSequential(\n",
       "    (0): Dropout(p = 0.1, axes=())\n",
       "    (1): Dense(768 -> 2, linear)\n",
       "  )\n",
       ")"
      ]
     },
     "execution_count": 26,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/",
     "height": 172
    },
    "executionInfo": {
     "elapsed": 1767,
     "status": "error",
     "timestamp": 1669261177688,
     "user": {
      "displayName": "전우진",
      "userId": "01920473921009871924"
     },
     "user_tz": -540
    },
    "id": "Kc_-MtLdsukZ",
    "outputId": "73bebe79-a5f2-4eb7-9c60-bd520010dadc"
   },
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "ignored",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-27-5820887a335f>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mload_model\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m: name 'load_model' is not defined"
     ]
    }
   ],
   "source": [
    "load_model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "8tyJjtg4uCgj"
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "accelerator": "GPU",
  "colab": {
   "machine_shape": "hm",
   "provenance": [
    {
     "file_id": "https://github.com/SKTBrain/KoBERT/blob/master/scripts/NSMC/naver_review_classifications_gluon_kobert.ipynb",
     "timestamp": 1669093216189
    }
   ]
  },
  "gpuClass": "premium",
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.0"
  },
  "toc": {
   "nav_menu": {},
   "number_sections": true,
   "sideBar": true,
   "skip_h1_title": false,
   "toc_cell": false,
   "toc_position": {},
   "toc_section_display": "block",
   "toc_window_display": false
  },
  "widgets": {
   "application/vnd.jupyter.widget-state+json": {
    "03808a5c1497414dbabf6ddda06a5743": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "ProgressStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "ProgressStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "bar_color": null,
      "description_width": ""
     }
    },
    "0474443973534cdda70e4c526cd2bb0a": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "04cf5fad0f4e46ea877a537a72cc0f39": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "07388772a1c847029559cedd658d603c": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "1addd4fca3714bbea1e19ac0d162712e": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_f79cc7de540f4b86bd92a1d0f8da22a7",
      "placeholder": "​",
      "style": "IPY_MODEL_791812521f5a47509838a1a37d4d3f07",
      "value": " 281/281 [4:01:57&lt;00:00, 46.47s/it]"
     }
    },
    "1ce851d66c8340a1bb0ce4986c07681d": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "1fc6409616bf4d97afaa0995f283005e": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "21a3404fc8e6470fb3dce891ba457766": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "ProgressStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "ProgressStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "bar_color": null,
      "description_width": ""
     }
    },
    "38a7b8d290e247a19a175e4fce7a82ed": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "39eaa4ae4c654fd99d83533ea0ab0692": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "3cc6f20fe3a64c0c8587823e7e38fc9a": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "3d9aef0573fe42bca049d38b04a87353": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_bfba2dc1a15148cb832c54436962244a",
      "placeholder": "​",
      "style": "IPY_MODEL_1ce851d66c8340a1bb0ce4986c07681d",
      "value": " 281/281 [3:55:35&lt;00:00, 45.98s/it]"
     }
    },
    "3e103eead4444d1ca2a24dc1ee1ae376": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_ab81519ca4554b0ba4995d6d2e441d3d",
      "placeholder": "​",
      "style": "IPY_MODEL_ae2e750e956d499a88a15f8b1366a978",
      "value": "100%"
     }
    },
    "4b37958a6a1544ff8443b5b8dfb39d4c": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_38a7b8d290e247a19a175e4fce7a82ed",
      "placeholder": "​",
      "style": "IPY_MODEL_c3c41bb1a5f446a4862641c6ba578bbd",
      "value": "100%"
     }
    },
    "4b6da813eddc42b199208b8b60aa1a26": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "ProgressStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "ProgressStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "bar_color": null,
      "description_width": ""
     }
    },
    "4f91a2ad8c1d4ca18a5a3fa7cf817787": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HBoxModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HBoxModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HBoxView",
      "box_style": "",
      "children": [
       "IPY_MODEL_bc19a9dc4c5448f4ba15ffb41e8b9f20",
       "IPY_MODEL_d05c0f09f5824e1ebeaf701e534ceb33",
       "IPY_MODEL_e2f6dea00a9c4dfa8665fc3215abd94f"
      ],
      "layout": "IPY_MODEL_544a853e64c44059ac2f4dd30af3b765"
     }
    },
    "507743910e72424bac4c898a1d77b6f9": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_bf9b13048c164079a15f685c67ae28fb",
      "placeholder": "​",
      "style": "IPY_MODEL_d79303dd7e7c4559af16ace6379b7a3e",
      "value": " 281/281 [4:12:56&lt;00:00, 50.34s/it]"
     }
    },
    "50af9db53f7a46cfaf0deae79129059b": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "544a853e64c44059ac2f4dd30af3b765": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "56ab5d81c5734428b41fba3b04f79c51": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "5bd53c3e256d4206afae214cb6d65aaf": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_965cd099b07b4f2db46822204e7e694a",
      "placeholder": "​",
      "style": "IPY_MODEL_bf3f3c9eefa348d4a5cfeffadac61678",
      "value": "100%"
     }
    },
    "5fcb0eddd07b49539cb5debd375adc23": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "6080ed35204e458aa71a83c52afa5924": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HBoxModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HBoxModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HBoxView",
      "box_style": "",
      "children": [
       "IPY_MODEL_4b37958a6a1544ff8443b5b8dfb39d4c",
       "IPY_MODEL_98356958fb824f94adf1e2e14fb56999",
       "IPY_MODEL_507743910e72424bac4c898a1d77b6f9"
      ],
      "layout": "IPY_MODEL_a6d78954f73e4e02b5d183b4de9dcf18"
     }
    },
    "613fce564ff54846b1c076764b5c100a": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "6862dd166f6547abaf892ed8e493a173": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "731c6712f31240b2a65825d29e5fbff2": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "791812521f5a47509838a1a37d4d3f07": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "87a608c2b3de4da79611b7f9577ba668": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "ProgressStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "ProgressStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "bar_color": null,
      "description_width": ""
     }
    },
    "88eb0276388548d58563f3eaa76cc5bd": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "8d85ec6ff654460f95aa868fbb5e9f59": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "919d1452812140899bb02a806b505c4a": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HBoxModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HBoxModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HBoxView",
      "box_style": "",
      "children": [
       "IPY_MODEL_b1a2a0da6ebd47199bc980a63169df5f",
       "IPY_MODEL_a481898e917e4e519cd1ae1b5c0bd146",
       "IPY_MODEL_1addd4fca3714bbea1e19ac0d162712e"
      ],
      "layout": "IPY_MODEL_8d85ec6ff654460f95aa868fbb5e9f59"
     }
    },
    "965cd099b07b4f2db46822204e7e694a": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "98356958fb824f94adf1e2e14fb56999": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "FloatProgressModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "FloatProgressModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "ProgressView",
      "bar_style": "success",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_613fce564ff54846b1c076764b5c100a",
      "max": 281,
      "min": 0,
      "orientation": "horizontal",
      "style": "IPY_MODEL_a7d030b8d41e458d837185aae29e1f79",
      "value": 281
     }
    },
    "a481898e917e4e519cd1ae1b5c0bd146": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "FloatProgressModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "FloatProgressModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "ProgressView",
      "bar_style": "success",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_bfa5bbb2d8864db080f06a83b12ae83f",
      "max": 281,
      "min": 0,
      "orientation": "horizontal",
      "style": "IPY_MODEL_03808a5c1497414dbabf6ddda06a5743",
      "value": 281
     }
    },
    "a6d78954f73e4e02b5d183b4de9dcf18": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "a7d030b8d41e458d837185aae29e1f79": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "ProgressStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "ProgressStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "bar_color": null,
      "description_width": ""
     }
    },
    "ab81519ca4554b0ba4995d6d2e441d3d": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "ae2e750e956d499a88a15f8b1366a978": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "b081230afd844298aca9294083f766c8": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "FloatProgressModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "FloatProgressModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "ProgressView",
      "bar_style": "success",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_5fcb0eddd07b49539cb5debd375adc23",
      "max": 281,
      "min": 0,
      "orientation": "horizontal",
      "style": "IPY_MODEL_4b6da813eddc42b199208b8b60aa1a26",
      "value": 281
     }
    },
    "b1a2a0da6ebd47199bc980a63169df5f": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_56ab5d81c5734428b41fba3b04f79c51",
      "placeholder": "​",
      "style": "IPY_MODEL_39eaa4ae4c654fd99d83533ea0ab0692",
      "value": "100%"
     }
    },
    "b7f345c0f18f45b39262fe0b22caa049": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "FloatProgressModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "FloatProgressModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "ProgressView",
      "bar_style": "success",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_731c6712f31240b2a65825d29e5fbff2",
      "max": 281,
      "min": 0,
      "orientation": "horizontal",
      "style": "IPY_MODEL_87a608c2b3de4da79611b7f9577ba668",
      "value": 281
     }
    },
    "bc19a9dc4c5448f4ba15ffb41e8b9f20": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_0474443973534cdda70e4c526cd2bb0a",
      "placeholder": "​",
      "style": "IPY_MODEL_04cf5fad0f4e46ea877a537a72cc0f39",
      "value": "100%"
     }
    },
    "bdda8d265e8d49feac2e601778fe763f": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HBoxModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HBoxModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HBoxView",
      "box_style": "",
      "children": [
       "IPY_MODEL_5bd53c3e256d4206afae214cb6d65aaf",
       "IPY_MODEL_b081230afd844298aca9294083f766c8",
       "IPY_MODEL_3d9aef0573fe42bca049d38b04a87353"
      ],
      "layout": "IPY_MODEL_88eb0276388548d58563f3eaa76cc5bd"
     }
    },
    "bf3f3c9eefa348d4a5cfeffadac61678": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "bf9b13048c164079a15f685c67ae28fb": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "bfa5bbb2d8864db080f06a83b12ae83f": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "bfba2dc1a15148cb832c54436962244a": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "c3c41bb1a5f446a4862641c6ba578bbd": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "d05c0f09f5824e1ebeaf701e534ceb33": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "FloatProgressModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "FloatProgressModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "ProgressView",
      "bar_style": "success",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_3cc6f20fe3a64c0c8587823e7e38fc9a",
      "max": 281,
      "min": 0,
      "orientation": "horizontal",
      "style": "IPY_MODEL_21a3404fc8e6470fb3dce891ba457766",
      "value": 281
     }
    },
    "d2b7270df9f54c4ea4236d294588f9dd": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_ee1a4fdd7fb24db890c2405839862f4e",
      "placeholder": "​",
      "style": "IPY_MODEL_07388772a1c847029559cedd658d603c",
      "value": " 281/281 [3:55:24&lt;00:00, 46.25s/it]"
     }
    },
    "d79303dd7e7c4559af16ace6379b7a3e": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "DescriptionStyleModel",
     "state": {
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "DescriptionStyleModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "StyleView",
      "description_width": ""
     }
    },
    "e2f6dea00a9c4dfa8665fc3215abd94f": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HTMLModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HTMLModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HTMLView",
      "description": "",
      "description_tooltip": null,
      "layout": "IPY_MODEL_50af9db53f7a46cfaf0deae79129059b",
      "placeholder": "​",
      "style": "IPY_MODEL_1fc6409616bf4d97afaa0995f283005e",
      "value": " 281/281 [4:04:07&lt;00:00, 48.72s/it]"
     }
    },
    "ea05be94e56245c19b4258cda60b7958": {
     "model_module": "@jupyter-widgets/controls",
     "model_module_version": "1.5.0",
     "model_name": "HBoxModel",
     "state": {
      "_dom_classes": [],
      "_model_module": "@jupyter-widgets/controls",
      "_model_module_version": "1.5.0",
      "_model_name": "HBoxModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/controls",
      "_view_module_version": "1.5.0",
      "_view_name": "HBoxView",
      "box_style": "",
      "children": [
       "IPY_MODEL_3e103eead4444d1ca2a24dc1ee1ae376",
       "IPY_MODEL_b7f345c0f18f45b39262fe0b22caa049",
       "IPY_MODEL_d2b7270df9f54c4ea4236d294588f9dd"
      ],
      "layout": "IPY_MODEL_6862dd166f6547abaf892ed8e493a173"
     }
    },
    "ee1a4fdd7fb24db890c2405839862f4e": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    },
    "f79cc7de540f4b86bd92a1d0f8da22a7": {
     "model_module": "@jupyter-widgets/base",
     "model_module_version": "1.2.0",
     "model_name": "LayoutModel",
     "state": {
      "_model_module": "@jupyter-widgets/base",
      "_model_module_version": "1.2.0",
      "_model_name": "LayoutModel",
      "_view_count": null,
      "_view_module": "@jupyter-widgets/base",
      "_view_module_version": "1.2.0",
      "_view_name": "LayoutView",
      "align_content": null,
      "align_items": null,
      "align_self": null,
      "border": null,
      "bottom": null,
      "display": null,
      "flex": null,
      "flex_flow": null,
      "grid_area": null,
      "grid_auto_columns": null,
      "grid_auto_flow": null,
      "grid_auto_rows": null,
      "grid_column": null,
      "grid_gap": null,
      "grid_row": null,
      "grid_template_areas": null,
      "grid_template_columns": null,
      "grid_template_rows": null,
      "height": null,
      "justify_content": null,
      "justify_items": null,
      "left": null,
      "margin": null,
      "max_height": null,
      "max_width": null,
      "min_height": null,
      "min_width": null,
      "object_fit": null,
      "object_position": null,
      "order": null,
      "overflow": null,
      "overflow_x": null,
      "overflow_y": null,
      "padding": null,
      "right": null,
      "top": null,
      "visibility": null,
      "width": null
     }
    }
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 0
}