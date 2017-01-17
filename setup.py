#!/usr/bin/env python

from setuptools import setup

setup(name='jobads-textminer',
      version='0.1',
      description='Job Ads Text Miner',
      url='https://github.com/tpucci/jobads-textminer',
      packages=['jobads', 'jobads.collector', 'jobads.collector.providers', 'jobads.processor'],
      install_requires=['pymongo>=3.4']
     )
