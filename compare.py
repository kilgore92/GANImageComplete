#Author : Ishaan Bhat
#Email  : i.r.bhat@student.tue.nl

import argparse
import os
import tensorflow as tf

from model import DCGAN
import pickle
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--approach', type=str,
                    choices=['adam', 'hmc'],
                    default='adam')
parser.add_argument('--lr', type=float, default=0.01)
parser.add_argument('--beta1', type=float, default=0.9)
parser.add_argument('--beta2', type=float, default=0.999)
parser.add_argument('--eps', type=float, default=1e-8)
parser.add_argument('--hmcBeta', type=float, default=0.2)
parser.add_argument('--hmcEps', type=float, default=0.001)
parser.add_argument('--hmcL', type=int, default=100)
parser.add_argument('--hmcAnneal', type=float, default=1)
parser.add_argument('--nIter', type=int, default=1000)
parser.add_argument('--imgSize', type=int, default=64)
parser.add_argument('--lam', type=float, default=0.1)
parser.add_argument('--checkpointDir', type=str, default='checkpoint')
parser.add_argument('--outDir', type=str, default='completions')
parser.add_argument('--outInterval', type=int, default=50)
parser.add_argument('--maskType', type=str,
                    choices=['random', 'center', 'left', 'full', 'grid', 'lowres'],
                    default='center')
parser.add_argument('--centerScale', type=float, default=0.4)
parser.add_argument('--imgs', type=str, default='completions') # Directory with the test images
parser.add_argument('--numImages', type=int, default=1) # Directory with the test images

args = parser.parse_args()

assert(os.path.exists(args.checkpointDir))

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
print (args)
with tf.Session(config=config) as sess:
    dcgan = DCGAN(sess, image_size=args.imgSize,
                  batch_size=1,
                  checkpoint_dir=args.checkpointDir, lam=args.lam)
    simScoreList = dcgan.compare(args)
    # Save this list for later plotting
    fname = 'simScore.pkl'

    listFile = Path(fname)

    # Delete if already exists
    if listFile.is_file():
        os.remove(fname)

    with open(fname,'wb') as f:
        pickle.dump(simScoreList,f)


