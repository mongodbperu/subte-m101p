# -*- coding: utf-8 -*-
import json
import logging
import os
import os.path
import re
import shutil
import sys

from datetime import datetime
from unicodedata import normalize

from tornado import gen, ioloop
from tornado.options import define, options, parse_command_line

define('mapping', type=str)
define('source_dir', type=str, help='Source directory')
define('destination_dir', type=str, help='Destination directory')
define('caption_extension', type=str, default='srt', help='Caption extension')
define('force', type=bool, help=('To force the creation of destination '
                                 'directory'))

__MAPPING_FORMAT = {
        'lecture': '%(number)02da-%(flat_concept)s-Lecture.%(extension)s',
        'answer': '%(number)02db-%(flat_concept)s-Answer.%(extension)s'
    }
__MAPPING_FORMAT2 = {
        True: '%(number)02d-%(flat_concept)s-Lecture.%(extension)s',
        False: '%(number)02d-%(flat_concept)s-Answer.%(extension)s'
    }
__RE_FLAT_CONCEPT = re.compile(r'[\t !"#%&\'*\:\;\-/<=>?@\[\\\]^_`{|},.]+')


loop = ioloop.IOLoop.current()


def validate_options():
    parse_command_line()
    required_options = ['mapping', 'source_dir', 'destination_dir']
    opts = [option for option in required_options
            if getattr(options, option) is None]
    if len(opts):
        print >> sys.stderr, (
            "Can't continue the process.\n\n"
            " The following options are required: " + ', '.join(opts)
        )
        sys.exit(1)
    if not os.path.exists(options.source_dir):
        print >> sys.stderr, (
            "Can't continue the process.\n\n"
            " The source directory doesn't exist."
        )
        sys.exit(1)
    if options.force and not os.path.exists(options.destination_dir):
        os.makedirs(options.destination_dir)
    elif not os.path.exists(options.destination_dir):
        print >> sys.stderr, (
            "Can't continue the process.\n\n"
            " The destination directory doesn't exist."
        )
        sys.exit(1)


def read_json_mapping():
    with open(options.mapping, 'r') as f:
        return json.loads(f.read())


@gen.engine
def get_flat_concept(concept, callback):
    concept = concept.replace('(', '')
    concept = concept.replace(')', '')
    result = []
    for word in __RE_FLAT_CONCEPT.split(concept):
        result.append(normalize('NFKD', word).encode('ascii', 'ignore'))
    callback(unicode('_'.join(result)))


@gen.engine
def get_filename(filename_format, number, flat_concept, callback):
    callback(filename_format % {
        'number': number,
        'flat_concept': flat_concept,
        'extension': options.caption_extension})


@gen.engine
def copy_file(source, filename_format, number, flat_concept, callback):
    filename = yield gen.Task(get_filename, filename_format, number,
        flat_concept)
    try:
        shutil.copy(os.path.join(options.source_dir, source),
            os.path.join(options.destination_dir, filename))
        logging.info('Copied %s to %s' % (source, filename))
    except Exception as e:
        logging.error(e)
    callback()


@gen.engine
def process_item(number, item, callback):
    has_lecture = 'lecture' in item
    has_answer = 'answer' in item
    if not has_lecture and not has_answer:
        logging.warning('"%s" has not lecture and answer.' % item['concept'])
    flat_concept = yield gen.Task(get_flat_concept, item['concept'])
    if has_lecture != has_answer:
        source = '%s.%s' % (
            item[{True: 'lecture', False: 'answer'}[has_lecture]],
            options.caption_extension)
        yield gen.Task(copy_file, source, __MAPPING_FORMAT2[has_lecture],
            number, flat_concept)
    else:
        if has_lecture:
            source = '%s.%s' % (item['lecture'], options.caption_extension)
            yield gen.Task(copy_file, source, __MAPPING_FORMAT['lecture'],
                number, flat_concept)
        if has_answer:
            source = '%s.%s' % (item['answer'], options.caption_extension)
            yield gen.Task(copy_file, source, __MAPPING_FORMAT['answer'],
                number, flat_concept)
    callback()


@gen.coroutine
def process(mapping):
    logging.info('Starting...')
    start = datetime.now()
    for i, item in enumerate(mapping):
        process_item(i + 1, item, callback=(yield gen.Callback(i)))
    yield gen.WaitAll(range(0, len(mapping)))
    end = datetime.now()
    logging.info('Terminating on: %s' % str(end - start))
    loop.stop()

if __name__ == '__main__':
    validate_options()
    process(read_json_mapping())
    loop.start()