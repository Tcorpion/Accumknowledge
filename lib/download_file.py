#encoding=utf-8
"""
This is used to download file from url

Created on : 20-12-10
Author     : Yulu Zhang
Version    : 1.0
"""


import time
import requests


def download_url_to_file(url_str, output_path, num_retries=5, timeout=20):
  """Download file from url

  Args:
    url_str: string, File URL to download
    output_path: string, Path to save
    num_retries : int, Number of times to retry before raising exception
    timeout : float, Duration to wait before interrupting request and retry

  """
  retries = 0
  while retries < num_retries:
    try:
      resp = requests.get(url_str, stream=True, timeout=timeout)
      resp.raise_for_status()
      if resp.status_code == 200:
        _bytes = bytearray(resp.raw.read())
        with open(output_path, 'wb') as f:
          f.write(_bytes)
        return True
    except Exception as e:
      print(f"failed: {url_str}", e)
      time.sleep(0.1 * (2 ** (retries - 1)))
      retries += 1
      continue
  print(f"failed: {url_str}")
  return False


def _download_url_to_file(args_tuple, num_retries=5, timeout=20):
  """Download file from url

  Args:
    args_tuple, (url_str, output_path)
      url_str: string, File URL to download
      output_path: string, Path to save
    num_retries : int, Number of times to retry before raising exception
    timeout : float, Duration to wait before interrupting request and retry

  """
  url_str, output_path = args_tuple
  return download_url_to_file(url_str, output_path, num_retries, timeout)

if __name__ == "__main__":

  import argparse
  import os
  import tqdm
  import multiprocessing
  from pathlib import Path
  from functools import partial

  parser = argparse.ArgumentParser(description='Download files with urls in txt file.')

  parser.add_argument(
    '-c', '--url_csv', type=str, required=True,
    help='The input csv files with urls, each line is:FILE_URL')

  parser.add_argument(
    '-o', '--out_dir', type=str, required=True,
    help='The directory to save downloaded files.')

  parser.add_argument(
    '-n', '--workers', type=int, default=8,
    help='The numbers of processors to downloaded files.')

  args = parser.parse_args()


  if not Path(args.url_csv).is_file():
    print(f'Wrong input: {args.url_csv}')
    exit(1)
  if not Path(args.out_dir).is_dir():
    Path(args.out_dir).mkdir(exist_ok=True, parents=True)

  existing_files = set(os.listdir(args.out_dir))


  # create the downloading task.
  tasks = []
  for url in Path(args.url_csv).open().readlines():
    url = url.strip()

    if len(url) < 10:
      continue

    filename = url.split('/')[-1]
    if filename in existing_files:
      continue

    filepath = Path(args.out_dir) / filename
    tasks.append((url, filepath))
  tasks.sort()


  print('Downloading {} files...'.format(len(tasks)))
  download_fun = partial(_download_url_to_file, num_retries=5, timeout=20)
  with multiprocessing.Pool(processes=args.workers) as pool:
    _ = list(
      tqdm.tqdm(
        pool.imap_unordered(
          download_fun,
          tasks
        ),
        total=len(tasks)
      )
    )
  print(f"Failed to download {_.count(False)} files")