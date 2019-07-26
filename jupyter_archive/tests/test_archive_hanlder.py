import io
import os
import logging
import tempfile
import json
from unicodedata import normalize

pjoin = os.path.join

import requests
import json

from nbformat import write
from nbformat.v4 import (new_notebook,
                              new_markdown_cell, new_code_cell,
                              new_output)

from notebook.utils import url_path_join
from notebook.tests.launchnotebook import NotebookTestBase
from ipython_genutils import py3compat


class ArchiveHandlerTest(NotebookTestBase):

    @classmethod
    def setup_class(cls):

        # Here I am trying to create a nb configuration that will
        # allow the Jupyter instance to discover the extension.
        # It doesn't seem to work.
        jupyter_config = {}
        jupyter_config['NotebookApp'] = {'nbserver_extensions': {}}
        jupyter_config['NotebookApp']['nbserver_extensions'] = {'jupyter_archive': True}
        tmp_dir_path = tempfile.mkdtemp()
        with open(pjoin(tmp_dir_path, 'jupyter_notebook_config.json'), 'w') as fp:
            json.dump(jupyter_config, fp)

        os.environ['JUPYTER_CONFIG_DIR'] = tmp_dir_path

        super().setup_class()

    def test_download(self):

        nbdir = self.notebook_dir

        # Create a dummy directory.
        archive_dir_path = pjoin(nbdir, 'archive-dir')
        os.makedirs(archive_dir_path)
        with open(pjoin(archive_dir_path, 'test1.txt'), 'w') as f:
            f.write('hello1')
        with open(pjoin(archive_dir_path, 'test2.txt'), 'w') as f:
            f.write('hello2')
        with open(pjoin(archive_dir_path, 'test3.md'), 'w') as f:
            f.write('hello3')

        # Try to download the created folder.
        archive_relative_path = os.path.basename(archive_dir_path)
        url = 'archive-download?archivePath={}&archiveToken=564646'.format(archive_relative_path)
        r = self.request('GET', url)
        print(r)
        print(r.headers['content-type'])

        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.headers['content-type'], 'application/octet-stream')
        self.assertEqual(r.headers['cache-control'], 'no-cache')