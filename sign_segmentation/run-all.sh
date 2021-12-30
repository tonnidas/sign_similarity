#!/bin/bash
# set -euxo pipefail

for entry in ../datasets/ira_alegria/processed_ira_alegria/videos/ira_*.mp4
do
  echo "$entry"
  python demo/demo.py --video_path "$entry" --save_path ../datasets/ira_alegria/processed_ira_alegria/vtt --generate_vtt
done

for entry in ../datasets/proteinas_porcentajes/processed_proteinas_porcentajes/videos/proteinas_*.mp4
do
  echo "$entry"
  python demo/demo.py --video_path "$entry" --save_path ../datasets/proteinas_porcentajes/processed_proteinas_porcentajes/vtt --generate_vtt
done

for entry in ../datasets/how2sign/processed_how2sign/videos/*.mp4
do
  echo "$entry"
  python demo/demo.py --video_path "$entry" --save_path ../datasets/how2sign/processed_how2sign/vtt --generate_vtt
done

for entry in ../datasets/how2sign2/processed_how2sign2/videos/*.mp4
do
  echo "$entry"
  python demo/demo.py --video_path "$entry" --save_path ../datasets/how2sign2/processed_how2sign2/vtt --generate_vtt
done
